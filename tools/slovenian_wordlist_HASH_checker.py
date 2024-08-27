import hashlib

# File path to the slovenian wordlist
file_path = 'slovenian.txt'

# Leave the code down bellow as is! 

def hash_file(filename, known_hash):
    """Generate SHA-256 hash of a file and compare it with a known hash."""
    sha256_hash = hashlib.sha256()  # Create a new SHA-256 hash object
    try:
        with open(filename, "rb") as f:  # Open the file in binary mode
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        file_hash = sha256_hash.hexdigest()  # Get the hexadecimal digest of the hash
        # Compare the computed hash with the known hash
        if file_hash == known_hash:
            return "This wordlist is the original Slovenian wordlist"
        else:
            return "WARNING: This wordlist is not the same as the original wordlist!"
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {e}"

# DO NOT MODIFY THIS HASH! DO NOT MODIFY THIS HASH! DO NOT MODIFY THIS HASH!
known_hash = "dee8744a4faec765fd483695e3de9005fca29f0cdcf328ba0c9cce3a29e86056"
# DO NOT MODIFY THIS HASH! DO NOT MODIFY THIS HASH! DO NOT MODIFY THIS HASH!

# Get the result of the hash check
result = hash_file(file_path, known_hash)
print(result)
