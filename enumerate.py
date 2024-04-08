import requests
import argparse

def enumerate_directories(url, wordlist):
    try:
        with open(wordlist, 'r') as f:
            for line in f:
                directory = line.strip()
                target_url = f"{url}/{directory}"
                response = requests.get(target_url)
                if response.status_code == 200:
                    print(f"[+] Found directory: {target_url}")
    except FileNotFoundError:
        print("Wordlist file not found!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory enumeration tool similar to Gobuster")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file", required=True)
    args = parser.parse_args()

    enumerate_directories(args.url, args.wordlist)
