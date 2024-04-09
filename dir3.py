import requests
import argparse
import threading
from queue import Queue

# Worker function to send HTTP requests
def worker(url, wordlist, results):
    while True:
        directory = wordlist.get()
        if directory is None:
            break
        target_url = f"{url}/{directory}"
        response = requests.get(target_url)
        if response.status_code == 200:
            results.append(target_url)
        wordlist.task_done()

# Function to display progress
def display_progress(total, results):
    while True:
        progress = len(results) / total * 100
        print(f"\rProgress: {len(results)}/{total} ({progress:.2f}%)", end='', flush=True)
        if len(results) == total:
            break
        threading.Event().wait(0.1)  # Adjust the sleep time as needed

def enumerate_directories(url, wordlist):
    # Read wordlist into a queue
    with open(wordlist, 'r') as f:
        wordlist_queue = Queue()
        for line in f:
            wordlist_queue.put(line.strip())

    # Create a list to store results
    results = []

    # Create worker threads
    num_threads = min(20, wordlist_queue.qsize())  # Limit threads to prevent overwhelming the server
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(url, wordlist_queue, results))
        t.start()
        threads.append(t)

    # Display progress
    progress_thread = threading.Thread(target=display_progress, args=(wordlist_queue.qsize(), results))
    progress_thread.start()

    # Wait for all worker threads to finish
    for t in threads:
        t.join()

    # Signal progress display thread to finish
    wordlist_queue.join()
    wordlist_queue.put(None)  # Signal to terminate

    # Wait for progress display thread to finish
    progress_thread.join()

    # Print found directories
    print("\nFound directories:")
    for result in results:
        print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory enumeration tool similar to Gobuster")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file", required=True)
    args = parser.parse_args()

    enumerate_directories(args.url, args.wordlist)
