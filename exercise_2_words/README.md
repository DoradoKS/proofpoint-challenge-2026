# Proofpoint Technical Challenge 2026 - Word Frequency Analysis

This tool is a standalone script designed to parse plain text files and generate a statistical ranking of the most frequently used words.

## Technical Implementation

The solution follows a three-step pipeline to ensure accuracy and efficiency:

### 1. Normalization and Tokenization
The script reads the raw input text and performs the following transformations:
- **Case Normalization**: All text is converted to lowercase to ensure that words like "The" and "the" are counted as the same token.
- **Noise Reduction**: Regular Expressions (`\b[a-zñáéíóú]+\b`) are used to strictly identify valid words, filtering out punctuation, numbers, and special characters.

### 2. Frequency Counting
The system utilizes a Hash Map structure to calculate the occurrence of each unique token with **O(N)** time complexity, where N is the number of words in the text.

### 3. Ranking and Output
Finally, the script sorts the dictionary of counts in descending order and extracts the top 10 entries to display the most frequent terms alongside their occurrence count.