import hashlib

# File path to the Slovenian wordlist
file_path = 'slovenian.txt'

# Leave the code below as is!

def hash_file(filename, known_hash):
    """Generate SHA-256 hash of a file and compare it with a known hash."""
    sha256_hash = hashlib.sha256()  # Create a new SHA-256 hash object
    try:
        with open(filename, "rb") as f:  # Open the file in binary mode
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        file_hash = sha256_hash.hexdigest()  # Get the hexadecimal digest of the hash
        
        # Display the original (known) hash and the computed hash of the file
        print(f"Original (known) hash: {known_hash}")
        print(f"Computed file hash: {file_hash}")

        # Compare the computed hash with the known hash
        if file_hash == known_hash:
            return "\nAwesome! This wordlist is the original Slovenian wordlist"
        else:
            return "\nWARNING: This wordlist is not the same as the original Slovenian wordlist! \n\nTIP: Check if there's an extra line after the last word."
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {e}"

# DO NOT MODIFY THIS HASH! DO NOT MODIFY THIS HASH! DO NOT MODIFY THIS HASH!
known_hash = "a6bf75472276892bbad530c61b321324cf7e3705e7300a8e903c16c48750f4c1"
# DO NOT MODIFY THIS HASH! DO NOT MODIFY THIS HASH! DO NOT MODIFY THIS HASH!

# Get the result of the hash check
result = hash_file(file_path, known_hash)
print(result)