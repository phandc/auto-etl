import httpx

async def create_message(url, data):
    async with httpx.AsyncClient() as client:
        print(f"Sending data {data}")
        response = await client.post(url=url, json=data)
        return response