from service.message import create_message
from endpoint import api_management_endpoint
import asyncio
import uuid
import random
from datetime import date
import schedule 
import time 


today = date.today()
    
str_date = date.isoformat(today)


async def send_multi_requests():
    tasks = []
    num_requests = 10
    start = time.time()
    for _ in range(0, num_requests):
        data = {
            "factory_id": uuid.uuid1().hex,
            "org_id":  uuid.uuid1().hex,
            "country": "VN",
            "execution_date": str_date,
            "fail_rate": round(random.uniform(0, 0.8), 2),
            "defect_rate": round(random.uniform(0, 0.8), 2)
        }
        tasks.append(create_message(api_management_endpoint, data=data))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end = time.time()
    print(f"Result after sending {num_requests}: {results} in {(end-start) * 10**3} ms")
    return results

def handle_send_data():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_multi_requests())

if __name__ == '__main__':
    print("Start sending requests .....")
    schedule.every(5).seconds.do(handle_send_data)
    while True:
        schedule.run_pending()
        time.sleep(1)