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

        # ===== Bemeneti fájl =====

        ctk.CTkLabel(
            self,
            text="Word dokumentum"
        ).pack(anchor="w", padx=20)

        self.input_entry = ctk.CTkEntry(
            self,
            width=700
        )
        self.input_entry.pack(
            padx=20,
            pady=(5, 10)
        )

        browse_button = ctk.CTkButton(
            self,
            text="📂 Tallózás...",
            command=self.select_file
        )
        browse_button.pack(pady=(0, 20))

        # ===== Kimeneti fájl =====

        ctk.CTkLabel(
            self,
            text="Kimeneti fájl"
        ).pack(anchor="w", padx=20)

        self.output_entry = ctk.CTkEntry(
            self,
            width=700
        )
        self.output_entry.pack(
            padx=20,
            pady=(5, 20)
        )

        # ===== Állapot =====

        self.status_label = ctk.CTkLabel(
            self,
            text="Készen áll",
            anchor="w"
        )
        self.status_label.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        # ===== Progress =====

        self.progress = ctk.CTkProgressBar(self)

        self.progress.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        self.progress.set(0)

        # ===== Napló =====

        ctk.CTkLabel(
            self,
            text="Napló"
        ).pack(anchor="w", padx=20)

        self.log_box = ctk.CTkTextbox(
            self,
            height=180
        )

        self.log_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 20)
        )

        self.log_box.configure(state="disabled")

        # ===== Rendezés gomb =====

        self.button = ctk.CTkButton(
            self,
            text="🚀 RENDEZÉS",
            command=self.start_process,
            height=40
        )

        self.button.pack(pady=10)

    # ==================================================

    def log(self, text):

        self.status_label.configure(text=text)

        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

        self.update_idletasks()
    def update_progress(self, value):

        self.progress.set(value / 100)

        self.update_idletasks()

    # ==================================================

    def select_file(self):

        filename = filedialog.askopenfilename(
            title="Word dokumentum kiválasztása",
            filetypes=[
                ("Word dokumentum", "*.docx"),
                ("Minden fájl", "*.*")
            ]
        )

        if not filename:
            return

        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, filename)

        output = self.controller.output_filename(filename)

        self.output_entry.delete(0, "end")
        self.output_entry.insert(0, output)

    # ==================================================

    def start_process(self):

        self.update_progress(0)
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

        filename = self.input_entry.get()
        output = self.output_entry.get()

        if not filename:
            self.log("Nincs kiválasztott fájl.")
            return

        self.log("Rendezés elindult...")

        try:

            self.controller.process_document(
                filename,
                output,
                logger=self.log,
                progress=self.update_progress
            )

            self.log("✅ Kész!")

            print("=" * 40)
            print("KÉSZ!")
            print(output)

            

        except Exception:

            import traceback

            self.log("❌ Hiba történt!")

            traceback.print_exc()