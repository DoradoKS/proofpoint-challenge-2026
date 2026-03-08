import csv
from typing import List, Dict
from models import Episode
import cleaner
from reporter import QualityReporter

class CatalogProcessor:
    """
    Main class that orchestrates the reading, cleaning, deduplication, 
    and writing of the catalog.
    """
    def __init__(self, input_file: str, output_file: str, reporter: QualityReporter):
        self.input_file = input_file
        self.output_file = output_file
        self.reporter = reporter
        #We use a dictionary to group episodes by "Normalized Series".
        #This makes the duplicate search much faster (O(N) instead of O(N^2)).
        self.catalog: Dict[str, List[Episode]] = {}

    def process(self):
        """Executes the full processing pipeline."""
        self._read_and_clean()
        self._write_output()

    def _read_and_clean(self):
        """Reads the CSV, creates Episode objects, and resolves duplicates on the fly."""
        with open(self.input_file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            #Prevents processing the first row as data
            next(reader, None) 
            
            for row in reader:
                self.reporter.log_input()
                
                #Basic validation: Skip empty rows
                if not row:
                    self.reporter.log_discard()
                    continue

                #Extract Raw Data
                try:
                    raw_series = row[0]
                    #If Series Name is missing, discard the record
                    if not raw_series.strip():
                        self.reporter.log_discard()
                        continue
                        
                    raw_season = row[1] if len(row) > 1 else ""
                    raw_ep_num = row[2] if len(row) > 2 else ""
                    raw_title = row[3] if len(row) > 3 else ""
                    raw_date = row[4] if len(row) > 4 else ""
                except IndexError:
                    self.reporter.log_discard()
                    continue

                #Cleaning and Normalization
                clean_series = cleaner.clean_string(raw_series)
                clean_season = cleaner.clean_number(raw_season)
                clean_ep_num = cleaner.clean_number(raw_ep_num)
                clean_title = cleaner.clean_string(raw_title, default="Untitled Episode")
                clean_date_val = cleaner.clean_date(raw_date)

                #If the episode number, title, and air date are missing, it is discarded.
                if (clean_ep_num == 0 and 
                    clean_title == "Untitled Episode" and 
                    clean_date_val == "Unknown"):
                    self.reporter.log_discard()
                    continue

                #Create the DTO (Data Transfer Object)
                new_episode = Episode(
                    series_name=clean_series,
                    season_number=clean_season,
                    episode_number=clean_ep_num,
                    episode_title=clean_title,
                    air_date=clean_date_val
                )

                #Detect and resolve duplicates
                self._add_or_merge(new_episode)

    def _add_or_merge(self, new_ep: Episode):
        """
        Attempts to add the episode to the catalog. If a duplicate exists 
        (based on Identity Keys), it keeps the best record.
        """
        series_key = cleaner.normalize_for_comparison(new_ep.series_name)
        
        # Initialize the list for this series if it doesn't exist
        if series_key not in self.catalog:
            self.catalog[series_key] = []
            self.catalog[series_key].append(new_ep)
            return

        candidates = self.catalog[series_key]
        duplicate_found = False
        
        # Generate Identity Keys for the new episode
        new_keys = self._get_identity_keys(new_ep)

        for i, existing_ep in enumerate(candidates):
            existing_keys = self._get_identity_keys(existing_ep)
            
            # If they share any key, they are duplicates according to requirements
            if not new_keys.isdisjoint(existing_keys):
                self.reporter.log_duplicate()
                duplicate_found = True
                
                # Compare quality: Keep the record with more complete data
                if self._is_new_better(new_ep, existing_ep):
                    candidates[i] = new_ep # Replace old with new
                    self.reporter.log_correction()
                # If new is not better, we implicitly discard it (keep the old one)
                break
        
        if not duplicate_found:
            candidates.append(new_ep)

    def _get_identity_keys(self, ep: Episode) -> set:
        """
        Generates the 3 possible Identity Keys based on the PDF requirements.
        Allows matching records even if one has missing data (0).
        """
        s = cleaner.normalize_for_comparison(ep.series_name)
        t = cleaner.normalize_for_comparison(ep.episode_title)
        sn = ep.season_number
        en = ep.episode_number
        
        keys = set()
        
        # Rule 1: (Series, Season, Ep) - Only if numbers are valid (!= 0)
        if sn != 0 and en != 0:
            keys.add((s, sn, en))
        
        # Rule 2: (Series, 0, Ep, Title) - Uses Title as bridge when Season is missing
        if en != 0 and t != "untitled episode":
            keys.add((s, 0, en, t))
            
        # Rule 3: (Series, Season, 0, Title) - Uses Title as bridge when Episode is missing
        if sn != 0 and t != "untitled episode":
            keys.add((s, sn, 0, t))
            
        return keys

    def _are_duplicates(self, ep1: Episode, ep2: Episode) -> bool:
        """Checks if two episodes are duplicates by comparing their Identity Keys sets."""
        keys1 = self._get_identity_keys(ep1)
        keys2 = self._get_identity_keys(ep2)
        return not keys1.isdisjoint(keys2)

    def _is_new_better(self, new_ep: Episode, old_ep: Episode) -> bool:
        """
        Determines if the new episode is 'better' than the existing one based on priority.
        Returns True if the new episode should replace the old one.
        """
        # Priority 1: Valid Air Date wins over "Unknown"
        if new_ep.is_valid_air_date and not old_ep.is_valid_air_date:
            return True
        if not new_ep.is_valid_air_date and old_ep.is_valid_air_date:
            return False
            
        # Priority 2: Known Title wins over "Untitled Episode"
        if new_ep.is_known_title and not old_ep.is_known_title:
            return True
        if not new_ep.is_known_title and old_ep.is_known_title:
            return False
            
        # Priority 3: Valid Numbers win over 0 (missing info)
        if new_ep.has_valid_numbers and not old_ep.has_valid_numbers:
            return True
        if not new_ep.has_valid_numbers and old_ep.has_valid_numbers:
            return False

        # If tied, keep the existing one (First come, first served)
        return False

    def _write_output(self):
        """Writes the cleaned catalog to a new CSV file."""
        with open(self.output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write a clean header
            writer.writerow(["SeriesName", "Season", "Episode", "Title", "AirDate"])
            
            for series_episodes in self.catalog.values():
                for ep in series_episodes:
                    writer.writerow([
                        ep.series_name,
                        ep.season_number,
                        ep.episode_number,
                        ep.episode_title,
                        ep.air_date
                    ])
                    self.reporter.log_output()