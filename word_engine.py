import os
import win32com.client as win32

from parser import read_blocks


ORDER = {
    "felvételi": 0,
    "pótfelvételi": 1,
    "pótfelvételiúj": 2,
    "pótfelvételi2": 3,
}


class WordEngine:

    def __init__(self):

        self.word = None
        self.src = None
        self.dst = None

    # -------------------------------------------------

    def process(
        self,
        input_file,
        output_file,
        logger=None,
        progress=None,
    ):

        self.open_word()

        try:

            self.log(logger, "Forrás megnyitása...")
            self.open_document(input_file)

            self.log(logger, "Blokkok beolvasása...")
            blocks = self.read_blocks()

            self.log(logger, f"{len(blocks)} blokk beolvasva.")

            self.log(logger, "Rendezés...")
            self.sort_blocks(blocks)

            self.log(logger, "Új dokumentum létrehozása...")
            self.create_document()

            self.copy_blocks(
                blocks,
                logger,
                progress,
            )

            self.log(logger, "Mentés...")
            self.save_document(output_file)

            if progress:
                progress(100)

        finally:

            self.close_word()

    # -------------------------------------------------

    def log(self, callback, text):

        if callback:
            callback(text)
        else:
            print(text)

    # -------------------------------------------------

    def open_word(self):

        self.word = win32.gencache.EnsureDispatch(
            "Word.Application"
        )

        self.word.Visible = False

    # -------------------------------------------------

    def open_document(self, filename):

        self.src = self.word.Documents.Open(
            os.path.abspath(filename)
        )

    # -------------------------------------------------

    def create_document(self):

        self.dst = self.word.Documents.Add()

    # -------------------------------------------------

    def read_blocks(self):

        return read_blocks(self.src)

    # -------------------------------------------------

    def sort_blocks(self, blocks):

        blocks.sort(
            key=lambda b: (
                -b.year,
                ORDER.get(b.kind, 99),
            )
        )

    # -------------------------------------------------

    def copy_blocks(
        self,
        blocks,
        logger=None,
        progress=None,
    ):

        total = len(blocks)

        for i, block in enumerate(blocks, start=1):

            self.log(
                logger,
                f"{i}/{total}  {block.year} {block.kind}"
            )

            src_range = self.src.Range(
                Start=block.start_char,
                End=block.end_char,
            )

            insert = self.dst.Range(
                self.dst.Content.End - 1,
                self.dst.Content.End - 1,
            )

            insert.FormattedText = src_range.FormattedText

            if progress:
                progress(int(i / total * 100))

    # -------------------------------------------------

    def save_document(self, filename):

        self.dst.SaveAs(
            os.path.abspath(filename)
        )

    # -------------------------------------------------

    def close_word(self):

        if self.src:
            self.src.Close(False)

        if self.dst:
            self.dst.Close(False)

        if self.word:
            self.word.Quit()