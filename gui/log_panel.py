import customtkinter as ctk


class LogPanel(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="Napló"
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.textbox = ctk.CTkTextbox(
            self,
            height=180
        )

        self.textbox.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.textbox.configure(state="disabled")

    def add(self, text):

        self.textbox.configure(state="normal")

        self.textbox.insert("end", text + "\n")

        self.textbox.see("end")

        self.textbox.configure(state="disabled")

    def clear(self):

        self.textbox.configure(state="normal")

        self.textbox.delete("1.0", "end")

        self.textbox.configure(state="disabled")