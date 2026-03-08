import re
import os
from collections import Counter

def get_word_frequency(file_path, top_n=10):
    """
    Reads a text file, cleans punctuation, and returns the top N frequent words.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' not found."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            #Convert to lowercase for case-insensitive counting
            text = f.read().lower()

        #Regex: \b[a-zñáéíóú]+\b matches words only, ignoring numbers/punctuation
        words = re.findall(r'\b[a-zñáéíóú]+\b', text)
        
        #Count frequencies using an efficient hash map (Counter)
        counts = Counter(words)
        
        return counts.most_common(top_n)

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    #Setup paths relative to this script's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "input.txt")

    print("--- Word Frequency Analysis Tool ---")
    print(f"Reading from: {input_file}\n")

    top_words = get_word_frequency(input_file)

    if isinstance(top_words, list):
        print(f"{'WORD':<15} | {'FREQUENCY':<10}")
        print("-" * 30)
        for word, count in top_words:
            print(f"{word:<15} | {count:<10}")
    else:
        print(top_words)