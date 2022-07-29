from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep


class Loader:
    def __init__(self, start_msg="Loading...", end_msg="Done!", timeout=0.1, style="rotate"):
        """Loading animation wrapper.

        A wrapper for functions that provides three different loading animations.

        :param start_msg: Message to dispalay while the animation cycles.
        :param end_msg: Message to display after the animation ends.
        :param timeout: Sleep timout between animation steps.
        :param style:

            * rotate
                A counter clockwise rotating square.
            * build
                A constructing square (bottom to top).
            * destroy
                A deconstructing square (top to bottom).
            * shuffle
                A square with shuffling columns.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        if style == "rotate":
            self.steps = ["⠚", "⠓", "⠋", "⠙"]
        if style == "build":        
            self.steps = ["⡀", "⠄", "⠂", "⠁", "⢁", "⠡", "⠑", "⠉", "⡉", "⠍","⠋", "⢋", "⠫", "⠛"]
        if style == "destroy":
            self.steps = ["⠛", "⠫", "⢋", "⠋", "⠍", "⡉", "⠉", "⠑", "⠡", "⢁", "⠁","⠂", "⠄", "⡀"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c} ", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()
