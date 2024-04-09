import requests
import argparse
import threading

def enumerate_directories(url, wordlist):
    try:
        with open(wordlist, 'r') as f:
            total_lines = sum(1 for _ in f)  # Count total lines in the wordlist
            f.seek(0)  # Reset file pointer to beginning
            count = 0  # Initialize counter
            for line in f:
                count += 1
                directory = line.strip()
                target_url = f"{url}/{directory}"
                response = requests.get(target_url)
                if response.status_code == 200:
                    print(f"\n[+] Found directory: {target_url}")
                else:
                    print(f"\rProgress: {count}/{total_lines} ", end='', flush=True)
                # Calculate progress percentage
                progress = count / total_lines * 100
                print(f"({progress:.2f}%)", end='', flush=True)
    except FileNotFoundError:
        print("Wordlist file not found!")

def display_progress():
    while True:
        for i in range(101):
            print(f"\rProgress: {i}%", end='', flush=True)
            threading.Event().wait(0.1)  # Adjust the sleep time as needed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory enumeration tool similar to Gobuster")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file", required=True)
    args = parser.parse_args()

    progress_thread = threading.Thread(target=display_progress)
    progress_thread.start()

    enumerate_directories(args.url, args.wordlist)
    progress_thread.join()
