# Proofpoint Technical Challenge 2026 - Streaming Catalog

This project is an automated data pipeline designed to clean, deduplicate, and generate quality reports for a streaming media catalog. It was developed as part of the technical assessment for Proofpoint.

## Project Structure
- `src/`: Source code including the main entry point, processing logic, and data models.
- `data/`: Directory for input datasets and generated clean catalogs.
- `report.md`: Automatically generated report with data quality metrics.

## Deduplication Strategy
The core of this solution relies on a **Multi-Key Identity Approach**. Instead of simple field-to-field equality, the system generates three distinct "Identity Keys" for each record based on the PDF requirements:
1. `Series` + `Season` + `Episode`
2. `Series` + `0` + `Episode` + `Title`
3. `Series` + `Season` + `0` + `Title`

If two records share at least one common key, they are considered duplicates. This allows the system to merge records even when some data is missing or corrupted (represented by `0` or `Unknown`).

### Priority Rules
When a duplicate is detected, the system retains the record with higher data density following this hierarchy:
- Valid Air Date > "Unknown"
- Known Title > "Untitled Episode"
- Valid Numbers > 0

## Technical Observations and Suggested Improvements

During development, it was observed that the provided rules do not capture cases where two records have disjoint missing data (e.g., one is missing a SeasonNumber and the other is missing an EpisodeNumber, but they share a SeriesName and EpisodeTitle).
Due to strict adherence to the challenge requirements, a merge rule by Global Title was not implemented to avoid false positives, but this has been identified as an opportunity to improve catalog integrity.