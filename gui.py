import os
import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("📘 Word Feladatrendező")
        self.geometry("760x420")
        self.resizable(False, False)

        self.filename = ""

        # ---------- Cím ----------

        title = ctk.CTkLabel(
            self,
            text="📘 Word Feladatrendező",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(pady=(20, 10))

        # ---------- Dokumentum ----------

        frame = ctk.CTkFrame(self)

        frame.pack(fill="x", padx=25)

        ctk.CTkLabel(
            frame,
            text="Word dokumentum",
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(0, 15))

        self.path_entry = ctk.CTkEntry(
            row,
            width=520
        )

        self.path_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        browse = ctk.CTkButton(
            row,
            text="Tallózás",
            width=120,
            command=self.select_file
        )

        browse.pack(side="right")

        # ---------- Kimenet ----------

        self.output_label = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            justify="left",
            font=("Consolas", 12)
        )

        self.output_label.pack(fill="x", padx=30, pady=(20, 10))

        # ---------- Rendezés gomb ----------

        self.run_button = ctk.CTkButton(
            self,
            text="🚀 RENDEZÉS",
            width=260,
            height=45,
            state="disabled"
        )

        self.run_button.pack(pady=15)

        # ---------- Állapot ----------

        self.status = ctk.CTkLabel(
            self,
            text="Válassz egy Word dokumentumot.",
            font=("Segoe UI", 13)
        )

        self.status.pack(pady=10)

    def select_file(self):

        filename = filedialog.askopenfilename(

            title="Word dokumentum kiválasztása",

            filetypes=[
                ("Word dokumentum", "*.docx")
            ]
        )

        if not filename:
            return

        self.filename = filename

        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, filename)

        name, ext = os.path.splitext(filename)

        out = name + "_rendezett" + ext

        self.output_label.configure(
            text="Kimenet:\n" + out
        )

        self.run_button.configure(state="normal")

        self.status.configure(
            text="Készen áll a rendezésre."
        )