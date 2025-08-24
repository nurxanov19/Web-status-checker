import aiohttp
import asyncio
from urllib.parse import urlsplit
import time 
from datetime import datetime


async def status_checker(url, session):

    result = urlsplit(url)
    try:
        start = time.perf_counter()
        async with session.get(url, timeout=5) as response:
            elapsed = time.perf_counter() - start
            return f"{result.netloc} -> status: {response.status} {response.reason} | Response time: {elapsed:.2f}s | \
Checked at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
        
    except aiohttp.ClientError as e:
        return f"Network error: {e}"
    except asyncio.TimeoutError as e:
        return "Request timed out"

async def main():
    coroutines_to_run = []

    async with aiohttp.ClientSession() as session:
        with open('web-pages.txt', "r") as file1:
            content = file1.read()
            for url in content.split('\n'):
                if url:
                    coroutines_to_run.append(status_checker(url, session))
                else: continue 
    
        results = await asyncio.gather(*coroutines_to_run)
    print('Here you can see the status code of websites you previously provided:')
    for res in results:
        print(res, end='\n')

t1 = time.perf_counter()

asyncio.run(main())

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")

