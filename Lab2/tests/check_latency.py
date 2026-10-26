"""Run while the API is listening on localhost:5000."""
import statistics
import time
from urllib.request import urlopen

samples = []
for _ in range(100):
    start = time.perf_counter()
    with urlopen('http://127.0.0.1:5000/api/message', timeout=5) as response:
        assert response.status == 200
        response.read()
    samples.append((time.perf_counter() - start) * 1000)
samples.sort()
p95 = samples[94]
print(f'100 requests: median={statistics.median(samples):.1f}ms, p95={p95:.1f}ms; target p95 < 500ms: {p95 < 500}')
