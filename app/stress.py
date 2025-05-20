import asyncio
import time
from statistics import mean
from aiohttp import ClientSession
from datetime import datetime
import os

class StressResult:
    def __init__(self, total: int, success: int, fail: int, avg_latency: float, throughput: float):
        self.total = total
        self.success = success
        self.failed = fail
        self.avg_latency = avg_latency
        self.throughput = throughput

async def _worker(session: ClientSession, url: str, results: list, log_file):
    start = time.perf_counter()
    try:
        async with session.get(url) as resp:
            elapsed = (time.perf_counter() - start) * 1000
            results.append((resp.status, elapsed))
            message = f"[INFO] {resp.status} - {url} - {elapsed:.2f} ms"
            print(message)
            log_file.write(message + "")
    except Exception as e:
        results.append((None, None))
        message = f"[ERROR] Request failed to {url}: {e}"
        print(message)
        log_file.write(message + "")
async def run_stress_test(url: str, duration: int, concurrency: int) -> StressResult:
    url = str(url)
    results = []
    deadline = time.time() + duration

    os.makedirs("logs", exist_ok=True)
    log_file_path = f"logs/stress_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_file_path, "w") as log_file:
        async with ClientSession() as session:
            # Define a worker that runs until the deadline
            async def worker_loop():
                while time.time() < deadline:
                    await _worker(session, url, results, log_file)

            # Launch N concurrent workers
            tasks = [asyncio.create_task(worker_loop()) for _ in range(concurrency)]

            # Wait for all to complete
            await asyncio.gather(*tasks)

        # Compute metrics
        statuses = [s for s, _ in results]
        latencies = [l for _, l in results if l is not None]
        total = len(results)
        success = statuses.count(200)
        failed = total - success
        avg_latency = mean(latencies) if latencies else 0
        throughput = total / duration if duration > 0 else 0

        summary = (
            "=== Summary ===\n"
            f"Total Requests: {total}\n"
            f"Successful: {success}\n"
            f"Failed: {failed}\n"
            f"Average Latency (ms): {avg_latency:.2f}\n"
            f"Throughput (rps): {throughput:.2f}\n"
        )
        print(summary)
        log_file.write(summary)

    return StressResult(total, success, failed, avg_latency, throughput)
