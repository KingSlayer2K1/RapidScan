import aiohttp
import argparse
import asyncio

async def worker(session, url, wordlist, results):
    while True:
        directory = await wordlist.get()
        if directory is None:
            break
        target_url = f"{url}/{directory}"
        async with session.get(target_url) as response:
            if response.status == 200:
                results.append(target_url)
        wordlist.task_done()

async def enumerate_directories(url, wordlist):
    async with aiohttp.ClientSession() as session:
        # Create a list to store results
        results = []

        # Create worker coroutines
        coroutines = []
        for _ in range(20):  # Limit concurrent requests
            coroutine = worker(session, url, wordlist, results)
            coroutines.append(coroutine)

        # Start worker coroutines
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

    wordlist = asyncio.Queue()
    with open(args.wordlist, 'r') as f:
        for line in f:
            wordlist.put_nowait(line.strip())

    asyncio.run(enumerate_directories(args.url, wordlist))
