import hashlib
import itertools
import time


# Load wordlist for dictionary attack with utf-8 encoding
def load_wordlist(file):
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f"Wordlist file '{file}' not found.")
        return None


# Dictionary attack function
def dictionary_attack(hash_to_crack, wordlist_file, hash_type='md5'):
    wordlist = load_wordlist(wordlist_file)
    if not wordlist:
        return None

    for word in wordlist:
        hash_attempt = hash_password(word, hash_type)
        if hash_attempt == hash_to_crack:
            return word
    return None

# Brute-force attack function
def brute_force_attack(hash_to_crack, hash_type='md5', max_length=4):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for length in range(1, max_length + 1):
        for guess in itertools.product(characters, repeat=length):
            guess_word = ''.join(guess)
            hash_attempt = hash_password(guess_word, hash_type)
            if hash_attempt == hash_to_crack:
                return guess_word
    return None

# Helper function to hash a password
def hash_password(password, hash_type):
    if hash_type == 'md5':
        return hashlib.md5(password.encode()).hexdigest()
    elif hash_type == 'sha256':
        return hashlib.sha256(password.encode()).hexdigest()
    else:
        raise ValueError("Unsupported hash type. Use 'md5' or 'sha256'.")

# Main function to choose attack method and measure time
def main():
    hash_to_crack = input("Enter the hash to crack: ").strip()
    hash_type = input("Enter the hash type (md5/sha256): ").strip().lower()
    attack_type = input("Choose attack type (dictionary/bruteforce): ").strip().lower()
    
    start_time = time.time()
    
    if attack_type == 'dictionary':
        wordlist_file = input("Enter the path to your wordlist file: ").strip()
        result = dictionary_attack(hash_to_crack, wordlist_file, hash_type)
    elif attack_type == 'bruteforce':
        max_length = int(input("Enter maximum length for brute force (e.g., 4): "))
        result = brute_force_attack(hash_to_crack, hash_type, max_length)
    else:
        print("Invalid attack type selected.")
        return

    end_time = time.time()
    
    if result:
        print(f"Password found: {result}")
    else:
        print("Password not found.")
    
    print(f"Time taken: {end_time - start_time:.2f} seconds")

# Run the main function
if __name__ == "__main__":
    main()
