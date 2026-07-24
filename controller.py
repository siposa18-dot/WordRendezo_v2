from pathlib import Path
from multiprocessing import Process, Queue

from gui.worker import run_worker

class Controller:

    def __init__(self):
        pass

    # -------------------------------------------------

    def output_filename(self, input_file: str) -> str:

        path = Path(input_file)

        return str(
            path.with_name(
                path.stem + "_rendezett" + path.suffix
            )
        )

    # -------------------------------------------------

    def start_process(
        self,
        input_file,
        output_file,
    ):

        queue = Queue()

        process = Process(
            target=run_worker,
            args=(
                input_file,
                output_file,
                queue,
            ),
        )

        process.start()

        return process, queue