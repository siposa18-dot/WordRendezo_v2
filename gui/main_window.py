import customtkinter as ctk

from settings import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    THEME,
    COLOR_THEME,
)


ctk.set_appearance_mode(THEME)
ctk.set_default_color_theme(COLOR_THEME)


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(APP_NAME)

        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.resizable(False, False)

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="📘 Word Feladatrendező",
            font=("Segoe UI", 28, "bold"),
        )

        title.pack(pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="v2.0",
            font=("Segoe UI", 14),
            text_color="gray",
        )

        subtitle.pack()