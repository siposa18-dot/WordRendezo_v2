import customtkinter as ctk

from tkinter import filedialog
from queue import Empty
from controller import Controller


class MainWindow(ctk.CTk):

    POLL_INTERVAL = 100

    def __init__(self):
        super().__init__()

        self.controller = Controller()

        self.process = None
        self.queue = None

        self.title("📘 Word Feladatrendező")
        self.geometry("900x650")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # ===========================
        # Cím
        # ===========================

        title = ctk.CTkLabel(
            self,
            text="📘 Word Feladatrendező",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=(20, 5))

        version = ctk.CTkLabel(
            self,
            text="v2.1.0",
            font=("Segoe UI", 12)
        )
        version.pack(pady=(0, 20))

        # ===========================
        # Input
        # ===========================

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

        browse_button.pack(
            pady=(0, 20)
        )

        # ===========================
        # Output
        # ===========================

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

        # ===========================
        # Állapot
        # ===========================

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

        # ===========================
        # Progress
        # ===========================

        self.progress = ctk.CTkProgressBar(self)

        self.progress.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        self.progress.set(0)

        # ===========================
        # Napló
        # ===========================

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

        # ===========================
        # Gomb
        # ===========================

        self.button = ctk.CTkButton(
            self,
            text="🚀 RENDEZÉS",
            command=self.start_process,
            height=40
        )

        self.button.pack(pady=10)

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close,
        )

    # ==========================================================
    # Napló
    # ==========================================================

    def log(self, text):

        self._log(text)

    def _log(self, text):

        self.status_label.configure(
            text=text
        )

        self.log_box.configure(
            state="normal"
        )

        self.log_box.insert(
            "end",
            text + "\n"
        )

        self.log_box.see("end")

        self.log_box.configure(
            state="disabled"
        )

    # ==========================================================
    # Progress
    # ==========================================================

    def update_progress(self, value):

        self.progress.set(
            value / 100
        )

    # ==========================================================
    # Fájlválasztás
    # ==========================================================

    def select_file(self):

        filename = filedialog.askopenfilename(
            title="Word dokumentum kiválasztása",
            filetypes=[
                (
                    "Word dokumentum",
                    "*.docx",
                ),
                (
                    "Minden fájl",
                    "*.*",
                ),
            ],
        )

        if not filename:
            return

        self.input_entry.delete(
            0,
            "end",
        )

        self.input_entry.insert(
            0,
            filename,
        )

        output = self.controller.output_filename(
            filename
        )

        self.output_entry.delete(
            0,
            "end",
        )

        self.output_entry.insert(
            0,
            output,
        )

            # ==========================================================
    # Feldolgozás indítása
    # ==========================================================

    def start_process(self):

        self.progress.set(0)

        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

        filename = self.input_entry.get().strip()
        output = self.output_entry.get().strip()

        if not filename:
            self.log("❌ Nincs kiválasztott fájl.")
            return

        self.button.configure(state="disabled")

        self.log("🚀 Feldolgozás elindult...")

        self.process, self.queue = self.controller.start_process(
            filename,
            output,
        )

        self.after(
            self.POLL_INTERVAL,
            self.check_queue,
        )

        # ==========================================================
    # Queue figyelése
    # ==========================================================

    def check_queue(self):

        try:

            while True:

                msg_type, data = self.queue.get_nowait()

                if msg_type == "log":

                    self.log(data)

                elif msg_type == "progress":

                    self.update_progress(data)

                elif msg_type == "done":

                    self.update_progress(100)

                    self.log("✅ Kész!")

                    self.button.configure(state="normal")

                    self.process = None
                    self.queue = None

                    return

                elif msg_type == "error":

                    self.log("❌ Hiba történt!")
                    self.log(data)

                    self.button.configure(state="normal")

                    self.process = None
                    self.queue = None

                    return

        except Empty:

            pass

        except Exception as e:

            self.log(f"❌ Váratlan hiba: {e}")

        if self.process is not None:

            if self.process.is_alive():

                self.after(
                    self.POLL_INTERVAL,
                    self.check_queue,
                )

            else:

                self.button.configure(state="normal")

                self.process = None
                self.queue = None

    # ==========================================================
    # Ablak bezárása
    # ==========================================================

    def on_close(self):

        if self.process is not None and self.process.is_alive():

            self.log("⚠️ A feldolgozás még folyamatban van.")
            return

        self.destroy()