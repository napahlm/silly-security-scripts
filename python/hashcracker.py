import hashlib

wordlist_location = str(input('Enter wordlist location: '))
hash_input = str(input('Enter hash to be cracked: '))
hash_type = str(input('Specify hash type (SHA256, MD5):')).lower()

try:
    with open(wordlist_location, 'r') as file:
        for line in file.readlines():
            password = line.strip()
            if hash_type == "sha256":
                hashed_pass = hashlib.sha256(password.encode()).hexdigest()
            elif hash_type == "md5":
                hashed_pass = hashlib.md5(password.encode()).hexdigest()
            else:
                'Unsupported hash type.'
                exit(1)

            if hashed_pass == hash_input:
                print('Cleartext: ' + line.strip())
                exit(0)
except FileNotFoundError:
    print("Wordlist not found.")
    exit(1)

print("No match found.")