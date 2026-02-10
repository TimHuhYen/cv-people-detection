import time

class FPSCounter:
    def __init__(self):
        self.prev_time = time.time()
        self.fps = 0.0

    """
    I use a simple CV time tracking algorithm:
        change in time = current - previous
    """
    def update(self):
        curr_time = time.time()
        dt = curr_time - self.prev_time
        self.prev_time = curr_time
        if dt > 0:
            self.fps = 1.0 / dt

        """
        accumulator += dt
        while accumulator >= fixed_dt:
        tracker.update(fixed_dt)
        accumulator -= fixed_dt

        """

        return self.fps