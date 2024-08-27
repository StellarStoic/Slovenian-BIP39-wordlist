# group words that share same n characters. Set the number of characters in the suffix_length variable

from collections import defaultdict

# Define file names
input_filename = 'slovenian.txt'
output_filename = 'tools/words_sorted_by_last_character.txt'
    
    
def load_words(filename):
    """Load words from a file into a list."""
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def group_words_by_suffix(words, suffix_length):
    """
    Group words by their suffix of a specified length.

    :param words: List of words to be grouped
    :param suffix_length: Length of the suffix to consider for grouping
    :return: Dictionary with suffixes as keys and lists of words as values
    """
    grouped_words = defaultdict(list)

    for word in words:
        # Only group by the specified suffix length
        if len(word) >= suffix_length:
            suffix = word[-suffix_length:]
            grouped_words[suffix].append(word)

    return grouped_words

def filter_suffixes(grouped_words, suffix_length):
    """
    Filter out suffix groups that do not have exactly the specified number of words.

    :param grouped_words: Dictionary with suffixes as keys and lists of words as values
    :param suffix_length: Length of the suffix to filter by
    :return: Dictionary with only suffixes that have the specified length and at least one word
    """
    filtered_words = {suffix: words for suffix, words in grouped_words.items() if len(words) > 1}
    return filtered_words

def write_grouped_words(filename, grouped_words):
    """
    Write the grouped words to a file, sorted by suffix and then by words.

    :param filename: Name of the file to write the grouped words
    :param grouped_words: Dictionary with suffixes as keys and lists of words as values
    """
    with open(filename, 'w', encoding='utf-8') as file:
        for suffix in sorted(grouped_words.keys()):
            words = grouped_words[suffix]
            file.write(f"Suffix: {suffix}\n")
            for word in sorted(words):
                file.write(f"  {word}\n")
            file.write("\n")
        print("Done.")
        
def main():
    # Load words from the file
    words = load_words(input_filename)
    
    # Group words by their suffixes of a specified length
    suffix_length = 6  # Adjust this value as needed
    grouped_words = group_words_by_suffix(words, suffix_length)
    
    # Filter to include only suffixes with more than one word
    filtered_words = filter_suffixes(grouped_words, suffix_length)
    
    # Write the filtered and grouped words to the output file
    write_grouped_words(output_filename, filtered_words)
    


if __name__ == "__main__":
    main()
