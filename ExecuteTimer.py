from concurrent.futures.thread import ThreadPoolExecutor

import time
from Request import Request


def execute_delay(work_to_run, request: Request, server):
    # time.sleep(request.time) # TODO: debug, to be removed
    time.sleep(request.time * 60 * 60)
    work_to_run(server, request)


class ExecuteTimer:
    def __init__(self, pool=ThreadPoolExecutor()):
        self._pool = pool

    def schedule_count_down(self, work, request: Request, server):
        self._pool.submit(execute_delay, work, request, server)
