import customtkinter as ctk

class InfoWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        # Window Definition
        self.title("About the Team")
        self.geometry("500x400")
        self.configure(bg="#3B6255")

        # Label with the title of the Window
        title = ctk.CTkLabel(
            self,
            text="Readwise Information",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=(20, 10))

        # Text to display
        info_text = (
            "Readwise was built by:\n\n"
            "• Jasmine Qiang\n"
            "• Shen-Chun Huang\n"
            "• Gabriel Reynoso Romero\n"
            "\n"
            "\n"
            "ver: 1.0.0"
        )
        # Textbox information
        textbox = ctk.CTkTextbox(
            self,
            width=440,
            height=240,
            wrap="word"
        )
        textbox.pack(padx=20, pady=10)
        # Insert the text
        textbox.insert("1.0", info_text)
        textbox.configure(state="disabled")

        close_btn = ctk.CTkButton(self, text="Back", width=100, command=self.destroy)
        close_btn.pack(pady=15)