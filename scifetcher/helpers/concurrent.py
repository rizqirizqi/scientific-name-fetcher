from concurrent.futures import ThreadPoolExecutor, Future, as_completed


def run_concurrently(fn_list):
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for item in fn_list:
        if not item or not isinstance(item, tuple):
            futures.append(pool.submit(lambda x: x, None))
            continue
        (fn, payload) = item
        if isinstance(payload, tuple):
            futures.append(pool.submit(fn, *payload))
        else:
            futures.append(pool.submit(fn, payload))
    results = list(map(lambda x: x.result(60), futures))
    return results
