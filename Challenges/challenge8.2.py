import threading

def runner(id, sum_range, results):
    """ Thread running function. """
    start, end = sum_range
    total = sum(range(start, end+1))
    results[id] = total

ranges = [
    [10, 20],
    [1, 5],
    [70, 80],
    [27, 92],
    [0, 16]
]
THREAD_COUNT = len(ranges)

threads = []
results = [0] * THREAD_COUNT

for i in range(THREAD_COUNT):
    t = threading.Thread(target=runner, args=(i, ranges[i], results))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(results)
print(sum(results))