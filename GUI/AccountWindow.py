import customtkinter as ctk

class AccountWindow(ctk.CTkToplevel):

    def __init__(self, master, user_data):
        super().__init__(master)

        self.title("Account Information")
        self.geometry("500x400")
        self.grab_set()

        # Title label
        title = ctk.CTkLabel(
            self,
            text="Account Information",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title.pack(pady=(20, 10))

        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(padx=20, pady=10, fill="x")

        def add_row(label, value):
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=f"{label}:", width=100, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value, anchor="w").pack(side="left")

        add_row("Username", user_data.get("username", ""))
        add_row("First name", user_data.get("first_name", ""))
        add_row("Last name", user_data.get("last_name", ""))
        add_row("Birthdate", user_data.get("birthdate", ""))
        add_row("Books read", user_data.get("books_read", ""))

        close_btn = ctk.CTkButton(self, text="Close", width=100, command=self.destroy)
        close_btn.pack(pady=15)