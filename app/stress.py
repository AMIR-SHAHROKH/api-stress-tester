import asyncio
import time
from statistics import mean
from aiohttp import ClientSession

class StressResult:
    def __init__(self, total, success, fail, avg_latency, throughput):
        self.total = total
        self.success = success
        self.failed = fail
        self.avg_latency = avg_latency
        self.throughput = throughput

async def _worker(session: ClientSession, url: str, results: list):
    start = time.perf_counter()
    try:
        async with session.get(url) as resp:
            elapsed = (time.perf_counter() - start) * 1000
            results.append((resp.status, elapsed))
    except Exception:
        results.append((None, None))

async def run_stress_test(url: str, duration: int, concurrency: int) -> StressResult:
    """
    Run concurrent GET requests to `url` for `duration` seconds with `concurrency` workers.
    """
    results = []
    deadline = time.time() + duration
    async with ClientSession() as session:
        sem = asyncio.Semaphore(concurrency)
        tasks = []

        async def bound_worker():
            async with sem:
                await _worker(session, url, results)

        # schedule tasks until deadline
        while time.time() < deadline:
            tasks.append(asyncio.create_task(bound_worker()))
        await asyncio.gather(*tasks)

    statuses = [s for s, _ in results]
    latencies = [l for _, l in results if l is not None]
    total = len(results)
    success = statuses.count(200)
    failed = total - success
    avg_latency = mean(latencies) if latencies else 0
    throughput = total / duration if duration > 0 else 0

    return StressResult(total, success, failed, avg_latency, throughput)