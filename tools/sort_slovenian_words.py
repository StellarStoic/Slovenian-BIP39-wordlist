# Python script to sort Slovenian words in a text file, check for duplicates, invalid characters, and word length,
# ensure no two words share the same first four letters, convert all to lowercase, and provide comprehensive statistics.

INPUT_FILE = "slovenian.txt"
OUTPUT_FILE = "tools/slovenian_wordlist_checked_and_sorted.txt"

def custom_slovenian_sort_and_check():
    # Define the custom Slovenian alphabetical order.
    slovenian_order = "abcčdefghijklmnoprsštuvzž"
    # Characters valid in Slovenian words.
    valid_characters = set(slovenian_order)

    # Dictionary for sorting based on Slovenian order.
    order_index = {char: index for index, char in enumerate(slovenian_order)}

    # Function to determine the sorting key of each word.
    def sort_key(word):
        return [order_index.get(char, -1) for char in word]

    # Read the words from the file, convert them to lowercase and strip whitespace.
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        words = [word.strip().lower() for word in file.read().split() if len(word.strip()) >= 3]

    # Initial count of words before any filtering.
    initial_word_count = len(words)

    # Track duplicates and issues with invalid characters.
    seen_words = set()
    first_four_characters = {}
    length_count = {}
    issues = []

    # List for valid and unique words.
    valid_words = []

    # Check each word for validity, unique first four characters, and appropriate length.
    for word in words:
        # Check for invalid characters.
        if not all(char in valid_characters for char in word):
            issues.append(f"Invalid characters found in word: {word}")
        
        # Check for duplicates in full words.
        if word in seen_words:
            issues.append(f"Duplicate word found: {word}")
        else:
            seen_words.add(word)

        # Extract the first four characters.
        first_four = word[:4]
        if first_four in first_four_characters:
            issues.append(f"Words '{first_four_characters[first_four]}' and '{word}' start with the same four characters: {first_four}")
        else:
            first_four_characters[first_four] = word
            valid_words.append(word)

        # Update length statistics.
        word_length = len(word)
        if word_length not in length_count:
            length_count[word_length] = 0
        length_count[word_length] += 1

    # Sort the valid words using the custom Slovenian order.
    words_sorted = sorted(valid_words, key=sort_key)

    # Final count of valid and unique words.
    final_word_count = len(valid_words)

    # Calculate statistics for the first letters.
    first_letter_count = {char: 0 for char in slovenian_order}
    for word in valid_words:
        first_letter_count[word[0]] += 1

    total_valid_words = len(valid_words)
    letter_stats = {char: f"{(first_letter_count[char] / total_valid_words * 100):.2f}% = {first_letter_count[char]} words" for char in first_letter_count if first_letter_count[char] > 0}

    # Prepare length statistics.
    length_stats = {length: f"{(count / total_valid_words * 100):.2f}% = {count} words" for length, count in sorted(length_count.items())}

    # Report issues or write the sorted words and stats.
    if issues:
        print("Issues found:")
        for issue in issues:
            print(issue)
    else:
        print("No issues found. The list is clean and sorted.")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            for word in words_sorted:
                file.write(word + "\n")

    # Display total word counts and statistics.
    print(f"Total words initially: {initial_word_count}")
    print(f"Total valid and unique words: {final_word_count}")
    print("Statistics for each first letter:")
    for char, stat in letter_stats.items():
        print(f"Words starting with {char.upper()} = {stat}")
    
    print("Word length distribution:")
    for length, stat in length_stats.items():
        print(f"{length}-letter words = {stat}")

# Run the sorting and checking function with additional checks.
if __name__ == "__main__":
    custom_slovenian_sort_and_check()