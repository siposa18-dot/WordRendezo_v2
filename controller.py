from pathlib import Path

from word_engine import WordEngine


class Controller:

    def __init__(self):

        self.engine = WordEngine()

    def output_filename(self, input_file: str) -> str:
        """
        Meghatározza a kimeneti fájl nevét.
        """

        path = Path(input_file)

        return str(
            path.with_name(
                path.stem + "_rendezett" + path.suffix
            )
        )

    def process_document(self, input_file: str):

        output = self.output_filename(input_file)

        self.engine.process(
            input_file,
            output
        )

        return output