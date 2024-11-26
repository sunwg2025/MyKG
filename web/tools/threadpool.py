from concurrent.futures import ThreadPoolExecutor
from threading import Lock


class TrackedThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(self, max_workers=1):
        super().__init__(max_workers=max_workers)
        self._lock = Lock()
        self._pending_tasks = {}

    def submit(self, fn, *args, **kwargs):
        with self._lock:
            future = super().submit(fn, *args, **kwargs)
            self._pending_tasks[id(future)] = {'future': future, 'args': args[0]}
        future.add_done_callback(self._task_done)
        return future

    def _task_done(self, future):
        with self._lock:
            del self._pending_tasks[id(future)]

    def get_pending_tasks(self):
        with self._lock:
            return self._pending_tasks
