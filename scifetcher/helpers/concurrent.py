from concurrent.futures import ThreadPoolExecutor

thread_pool = ThreadPoolExecutor(max_workers=20)

def run_concurrently(fn_list):
    futures = []
    for item in fn_list:
        if not item or not isinstance(item, tuple):
            futures.append(thread_pool.submit(lambda x: x, None))
            continue
        (fn, payload) = item
        if not payload:
            futures.append(thread_pool.submit(fn))
        elif isinstance(payload, tuple):
            futures.append(thread_pool.submit(fn, *payload))
        else:
            futures.append(thread_pool.submit(fn, payload))
    results = list(map(lambda x: x.result(60), futures))
    return results
