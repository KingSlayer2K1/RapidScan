import aiohttp
import asyncio
import argparse
import sys

async def fetch(session, url, semaphore):
    async with semaphore:
        async with session.get(url) as response:
            if response.status == 200:
                print(f"\r[+] Found directory: {url}", end="")
                sys.stdout.flush()

async def enumerate_directories(url, wordlist):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            semaphore = asyncio.Semaphore(100)  # Limit concurrent requests to 100
            with open(wordlist, 'r') as f:
                total_lines = sum(1 for _ in f)
                f.seek(0)
                count = 0
                for line in f:
                    count += 1
                    directory = line.strip()
                    target_url = f"{url}/{directory}"
                    task = asyncio.ensure_future(fetch(session, target_url, semaphore))
                    tasks.append(task)
                    progress = count / total_lines * 100
                    print(f"\rProgress: {count}/{total_lines} ({progress:.2f}%) {'-' * int(progress / 2)}", end="")
                    sys.stdout.flush()
            await asyncio.gather(*tasks)
    except FileNotFoundError:
        print("Wordlist file not found!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory enumeration tool similar to Gobuster")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file", required=True)
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(enumerate_directories(args.url, args.wordlist))
