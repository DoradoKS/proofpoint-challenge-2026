from dataclasses import dataclass

@dataclass
class Episode:
    """This class represents an episode. It stores the data that has been cleaned and is ready to be processed."""
    series_name: str
    season_number: int
    episode_number: int
    episode_title: str
    air_date: str

    @property
    def is_valid_air_date(self) -> bool:
        """Check if the episode has a valid date for 'Unknown'."""
        return self.air_date != "Unknown"

    @property
    def is_known_title(self) -> bool:
        """Check if the episode has a familiar title."""
        return self.episode_title != "Untitled Episode"

    @property
    def has_valid_numbers(self) -> bool:
        """Check if it has a season and episode number higher than 0."""
        return self.season_number > 0 and self.episode_number > 0