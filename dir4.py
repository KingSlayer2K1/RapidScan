import aiohttp
import argparse
import asyncio
import threading

async def worker(session, url, wordlist, results, total, lock):
    while True:
        directory = await wordlist.get()
        if directory is None:
            break
        target_url = f"{url}/{directory}"
        async with session.get(target_url) as response:
            if response.status == 200:
                async with lock:
                    results.append(target_url)
                progress = len(results) / total * 100
                print(f"\rProgress: {len(results)}/{total} ({progress:.2f}%)", end='', flush=True)
        wordlist.task_done()

async def enumerate_directories(url, wordlist):
    async with aiohttp.ClientSession() as session:
        # Create a list to store results
        results = []
        total = wordlist.qsize()
        lock = threading.Lock()

        # Create worker coroutines
        coroutines = []
        for _ in range(20):  # Limit concurrent requests
            coroutine = worker(session, url, wordlist, results, total, lock)
            coroutines.append(coroutine)

        # Start worker coroutines
        await asyncio.gather(*coroutines)

        # Wait for all tasks to complete
        await wordlist.join()

        # Print found directories
        print("\nFound directories:")
        for result in results:
            print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory enumeration tool similar to Gobuster")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file", required=True)
    args = parser.parse_args()

    wordlist = asyncio.Queue()
    with open(args.wordlist, 'r') as f:
        for line in f:
            wordlist.put_nowait(line.strip())

    asyncio.run(enumerate_directories(args.url, wordlist))
