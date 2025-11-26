import customtkinter as ctk

class InfoWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("About the Team")
        self.geometry("500x400")
        self.configure(bg="#3B6255")

        title = ctk.CTkLabel(
            self,
            text="Readwise Information",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=(20, 10))

        # Text area
        info_text = (
            "Readwise is built by:\n\n"
            "• Jasmine Qiang\n"
            "• Shen-Chun Huang\n"
            "• Gabriel Reynoso Romero\n"
        )

        textbox = ctk.CTkTextbox(
            self,
            width=440,
            height=240,
            wrap="word"
        )
        textbox.pack(padx=20, pady=10)
        textbox.insert("1.0", info_text)
        textbox.configure(state="disabled")

        close_btn = ctk.CTkButton(self, text="Close", width=100, command=self.destroy)
        close_btn.pack(pady=15)