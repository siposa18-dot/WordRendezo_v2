import pythoncom
import traceback

from word_engine import WordEngine


def run_worker(
    input_file,
    output_file,
    queue,
):
    """
    Külön processben fut.
    A WordEngine callbackjeit Queue üzenetekké alakítja.
    """

    pythoncom.CoInitialize()

    try:

        engine = WordEngine()

        def logger(text):
            queue.put(("log", text))

        def progress(value):
            queue.put(("progress", value))

        engine.process(
            input_file=input_file,
            output_file=output_file,
            logger=logger,
            progress=progress,
        )

        queue.put(
            (
                "done",
                output_file,
            )
        )

    except Exception:

        queue.put(
            (
                "error",
                traceback.format_exc(),
            )
        )

    finally:

        pythoncom.CoUninitialize()