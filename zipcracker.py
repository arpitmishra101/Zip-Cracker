import argparse

def crack_zip(zip_file, min_length=1, max_length=8, wordlist=None):
    if wordlist:
        try:
            with open(wordlist, 'r') as f:
                words = [word.strip() for word in f.readlines()]
        except Exception as e:
            print(f"Error: {e}")
            return
    else:
        words = []
        for i in range(min_length, max_length + 1):
            words.extend(["".join(candidate) for candidate in itertools.product(string.ascii_letters + string.digits, repeat=i)])

    for word in words:
        try:
            zip_file.extractall(pwd=word.encode())
            print(f"Password found: {word}")
            return
        except zipfile.BadZipfile:
            continue

    print("Password not found in the given wordlist or within the specified length range.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract a ZIP file using a brute-force attack.")
    parser.add_argument("-zip", help="The path to the ZIP file.", required=True)
    parser.add_argument("-min", help="The starting length of the password to try.", type=int, default=1)
    parser.add_argument("-max", help="The maximum length of the password to try.", type=int, default=8)
    parser.add_argument("-wordlist", help="The path to a file containing a list of possible passwords.")

    args = parser.parse_args()

    zip_file = zipfile.ZipFile(args.zip, 'r')
    crack_zip(zip_file, args.min, args.max, args.wordlist)