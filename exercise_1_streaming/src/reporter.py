class QualityReporter:
    """
    Class responsible for collecting metrics on data quality and generating the final report.
    """
    def __init__(self):
        self.total_input_records = 0
        self.total_output_records = 0
        self.discarded_entries = 0
        self.corrected_entries = 0
        self.duplicates_detected = 0
        
        # Estrategia con formato Markdown mejorado
        self.deduplication_strategy = (
            "1. **Grouping**: Episodes were grouped by normalized series names to optimize processing.\n"
            "2. **Identity Keys**: A multi-key approach (Sets) was used to detect matches using the three required combinations:\n"
            "   - `Series` + `Season` + `Episode` (Standard match)\n"
            "   - `Series` + `0` + `Episode` + `Title` (Matches missing Season)\n"
            "   - `Series` + `Season` + `0` + `Title` (Matches missing Episode)\n"
            "3. **Priority Rules**: When a duplicate is found, the best record is retained based on the following hierarchy:\n"
            "   - **Valid Air Date** wins over 'Unknown'.\n"
            "   - **Known Episode Title** wins over 'Untitled Episode'.\n"
            "   - **Valid Season/Episode Numbers** win over zeros.\n"
            "   - **Tie-breaker**: The first entry encountered in the file is kept."
        )

    def log_input(self):
        self.total_input_records += 1

    def log_output(self):
        self.total_output_records += 1

    def log_discard(self):
        self.discarded_entries += 1

    def log_correction(self):
        self.corrected_entries += 1
    
    def log_duplicate(self):
        self.duplicates_detected += 1

    def generate_report(self, filepath: str):
        """Generate the report.md file with the statistics."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# Data Quality Report\n\n")
            f.write(f"- **Total Input Records**: {self.total_input_records}\n")
            f.write(f"- **Total Output Records**: {self.total_output_records}\n")
            f.write(f"- **Discarded Entries**: {self.discarded_entries}\n")
            f.write(f"- **Corrected Entries**: {self.corrected_entries}\n")
            f.write(f"- **Duplicates Detected**: {self.duplicates_detected}\n\n")
            f.write("## Deduplication Strategy\n")
            f.write(f"{self.deduplication_strategy}\n")