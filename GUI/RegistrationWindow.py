import customtkinter as ctk
from tkinter import messagebox
from users_handler_functions import *
from palette import COLORS, FONTS


class RegistrationWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Create Account")
        self.geometry("500x450")
        self.grab_set()
        self.configure(fg_color=COLORS["bg_root"])

        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.first_name_var = ctk.StringVar()
        self.last_name_var = ctk.StringVar()
        self.birthdate_var = ctk.StringVar()

        title = ctk.CTkLabel(
            self,
            text="Create your Readwise account",
            font=ctk.CTkFont(**FONTS["section"]),
            text_color=COLORS["text_light"],
        )
        title.pack(pady=(20, 10))

        form = ctk.CTkFrame(self, fg_color=COLORS["panel"])
        form.pack(pady=10, padx=40, fill="x")

        # First name
        ctk.CTkLabel(
            form,
            text="First name:",
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(**FONTS["body"]),
        ).pack(anchor="w", pady=(10, 0))
        ctk.CTkEntry(
            form,
            textvariable=self.first_name_var,
            fg_color=COLORS["entry_bg"],
            border_color=COLORS["entry_border"],
            text_color=COLORS["text_light"],
        ).pack(pady=(0, 10), fill="x")

        # Last name
        ctk.CTkLabel(
            form,
            text="Last name:",
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(**FONTS["body"]),
        ).pack(anchor="w")
        ctk.CTkEntry(
            form,
            textvariable=self.last_name_var,
            fg_color=COLORS["entry_bg"],
            border_color=COLORS["entry_border"],
            text_color=COLORS["text_light"],
        ).pack(pady=(0, 10), fill="x")

        # Username
        ctk.CTkLabel(
            form,
            text="Username:",
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(**FONTS["body"]),
        ).pack(anchor="w")
        ctk.CTkEntry(
            form,
            textvariable=self.username_var,
            fg_color=COLORS["entry_bg"],
            border_color=COLORS["entry_border"],
            text_color=COLORS["text_light"],
        ).pack(pady=(0, 10), fill="x")

        # Password
        ctk.CTkLabel(
            form,
            text="Password:",
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(**FONTS["body"]),
        ).pack(anchor="w")
        ctk.CTkEntry(
            form,
            textvariable=self.password_var,
            show="*",
            fg_color=COLORS["entry_bg"],
            border_color=COLORS["entry_border"],
            text_color=COLORS["text_light"],
        ).pack(pady=(0, 10), fill="x")

        # Birthdate
        ctk.CTkLabel(
            form,
            text="Birthdate (MM-DD-YYYY):",
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(**FONTS["body"]),
        ).pack(anchor="w")
        ctk.CTkEntry(
            form,
            textvariable=self.birthdate_var,
            fg_color=COLORS["entry_bg"],
            border_color=COLORS["entry_border"],
            text_color=COLORS["text_light"],
        ).pack(pady=(0, 10), fill="x")

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15)

        create_btn = ctk.CTkButton(
            btn_frame,
            text="Create account",
            command=self.create_account,
            fg_color=COLORS["primary_btn"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["text_light"],
            font=ctk.CTkFont(**FONTS["button"]),
        )
        create_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color=COLORS["secondary_btn"],
            hover_color=COLORS["secondary_hover"],
            text_color=COLORS["text_light"],
            font=ctk.CTkFont(**FONTS["button"]),
            command=self.destroy,
        )
        cancel_btn.pack(side="left", padx=10)

    def create_account(self):

        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        first = self.first_name_var.get().strip()
        last = self.last_name_var.get().strip()
        birthdate = self.birthdate_var.get().strip()

        # Check if all fields are filled
        if not all([username, password, first, last, birthdate]):
            messagebox.showwarning("Missing data", "Please fill in all fields.")
            return

        # Check if username is taken
        if get_user(username):
            messagebox.showerror("Username taken", "That username is already in use.")
            return

        # User data dictionary, the books read column is empty for now
        user_data = {
            "username": username,
            "password": password,
            "first_name": first,
            "last_name": last,
            "birthdate": birthdate,
            "books_read": ""
        }

        add_user(user_data)
        messagebox.showinfo("Success", "Account Created! You can now log in.")
        self.destroy()