import customtkinter as ctk


class Header(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(
            self,
            text="📘 Word Feladatrendező",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(pady=(15, 5))

        version = ctk.CTkLabel(
            self,
            text="v2.0.0-alpha",
            font=("Segoe UI", 12)
        )

        version.pack(pady=(0, 15))