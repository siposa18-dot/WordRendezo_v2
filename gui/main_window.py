import customtkinter as ctk
from tkinter import filedialog

from controller import Controller


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.controller = Controller()

        self.title("📘 Word Feladatrendező")
        self.geometry("900x650")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # ===== Cím =====

        title = ctk.CTkLabel(
            self,
            text="📘 Word Feladatrendező",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=(20, 5))

        version = ctk.CTkLabel(
            self,
            text="v2.0.0-alpha",
            font=("Segoe UI", 12)
        )
        version.pack(pady=(0, 20))

        # ===== Dokumentum =====

        ctk.CTkLabel(
            self,
            text="Word dokumentum"
        ).pack(anchor="w", padx=20)

        self.input_entry = ctk.CTkEntry(
            self,
            width=650
        )
        self.input_entry.pack(
            padx=20,
            pady=(5, 10)
        )

        # ===== Tallózás =====

        browse_button = ctk.CTkButton(
            self,
            text="📂 Tallózás...",
            command=self.select_file
        )
        browse_button.pack(pady=(0, 20))

        # ===== Rendezés =====

        self.button = ctk.CTkButton(
            self,
            text="🚀 RENDEZÉS",
            command=self.start_process
        )
        self.button.pack(pady=20)

    # ==================================================

    def select_file(self):

        filename = filedialog.askopenfilename(
            title="Word dokumentum kiválasztása",
            filetypes=[
                ("Word dokumentum", "*.docx"),
                ("Minden fájl", "*.*")
            ]
        )

        if filename:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, filename)

    # ==================================================

    def start_process(self):

        filename = self.input_entry.get()

        if not filename:
            return

        output = self.controller.process_document(filename)

        print()
        print("=" * 40)
        print("KÉSZ!")
        print(output)