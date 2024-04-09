import requests
import argparse
import asyncio

# Worker function to send HTTP requests
async def worker(url, wordlist, results, lock):
    while True:
        async with lock:
            directory = await wordlist.get()
        if directory is None:
            break
        target_url = f"{url}/{directory}"
        response = requests.get(target_url)
        if response.status_code == 200:
            async with lock:
                results.append(target_url)
        await wordlist.task_done()

# Function to display progress
async def display_progress(total, results, lock):
    while True:
        async with lock:
            progress = len(results) / total * 100
        print(f"\rProgress: {len(results)}/{total} ({progress:.2f}%)", end='', flush=True)
        if len(results) == total:
            break
        await asyncio.sleep(0.1)  # Adjust the sleep time as needed

async def enumerate_directories(url, wordlist_path):
    # Create a lock for synchronization
    lock = asyncio.Lock()

    # Read wordlist into a queue
    with open(wordlist_path, 'r') as f:
        wordlist_queue = asyncio.Queue()
        for line in f:
            await wordlist_queue.put(line.strip())

    # Create a list to store results
    results = []

    # Create coroutines for worker and progress display
    coroutines = []
    num_workers = min(20, wordlist_queue.qsize())  # Limit workers to prevent overwhelming the server
    for _ in range(num_workers):
        coroutines.append(worker(url, wordlist_queue, results, lock))
    coroutines.append(display_progress(wordlist_queue.qsize(), results, lock))

    # Run coroutines concurrently
    await asyncio.gather(*coroutines)

    # Print found directories
    print("\nFound directories:")
    for result in results:
        print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory enumeration tool similar to Gobuster")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file", required=True)
    args = parser.parse_args()

    asyncio.run(enumerate_directories(args.url, args.wordlist))
