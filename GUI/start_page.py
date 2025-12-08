import customtkinter as ctk
from tkinter import messagebox

from users_handler_functions import *
from main_page import MainPage
from RegistrationWindow import RegistrationWindow
from palette import COLORS, FONTS


class StartPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLORS["bg_root"])

        # Title
        self.master = master
        self.master.title("Readwise - Login Page")
        self.master.geometry("600x500")
        self.master.configure(bg=COLORS["bg_root"])

        # Title Label
        title = ctk.CTkLabel(
            self,
            text="Welcome to Readwise!",
            font=ctk.CTkFont(**FONTS["title"]),
            text_color=COLORS["text_light"],
        )
        title.pack(pady=(30, 20))

        # Card for card-like effect and centering
        card = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel"],
            corner_radius=16,
        )
        card.pack(padx=40, pady=10)

        # Login login_form
        login_form = ctk.CTkFrame(card, fg_color="transparent")
        login_form.pack(pady=20, padx=40, fill="x")

        # Username and password variables
        self.username = ctk.StringVar()
        self.password = ctk.StringVar()

        # Username row to align the label and the entry
        user_row = ctk.CTkFrame(login_form, fg_color="transparent")
        user_row.pack(fill="x", pady=(0, 10))
        # Make column 1 expand so entry moves toward center
        user_row.grid_columnconfigure(0, weight=0)
        user_row.grid_columnconfigure(1, weight=1)

        # Username space
        username_label = ctk.CTkLabel(
            user_row,
            text="Username:",
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(**FONTS["body"])
        )
        username_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        username_entry = ctk.CTkEntry(
            user_row,
            textvariable=self.username,
            width=250,
            fg_color=COLORS["entry_bg"],
            border_color=COLORS["entry_border"],
            text_color=COLORS["text_light"],
        )
        username_entry.grid(row=0, column=1, sticky="w")

        # Password frame to align the label and the entry
        pass_row = ctk.CTkFrame(login_form, fg_color="transparent")
        pass_row.pack(fill="x", pady=(0, 10))
        pass_row.grid_columnconfigure(0, weight=0)
        pass_row.grid_columnconfigure(1, weight=1)

        # Password space
        password_label = ctk.CTkLabel(
            pass_row,
            text="Password:",
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(**FONTS["body"])
        )
        password_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        password_entry = ctk.CTkEntry(
            pass_row,
            textvariable=self.password,
            show="*",
            width=250,
            fg_color=COLORS["entry_bg"],
            border_color=COLORS["entry_border"],
            text_color=COLORS["text_light"],
        )
        password_entry.grid(row=0, column=1, sticky="w")

        # Login Button
        login_btn = ctk.CTkButton(
            login_form,
            text="Login",
            command=self.login,
            fg_color=COLORS["primary_btn"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["text_light"],
            font=ctk.CTkFont(**FONTS["button"])
        )
        login_btn.pack(pady=10)

        # Create account
        link_frame = ctk.CTkFrame(self, fg_color="transparent")
        link_frame.pack(pady=(10, 0))

        link_label = ctk.CTkLabel(
            link_frame,
            text="Don't have an account?",
            text_color=COLORS["text_light"],
            font=ctk.CTkFont(**FONTS["body"])
        )
        link_label.pack(side="left", padx=(0, 5))

        # Create account button
        create_btn = ctk.CTkButton(
            link_frame,
            text="Create account",
            fg_color="transparent",
            text_color=COLORS["panel"],
            hover_color=COLORS["secondary_hover"],
            command=self.open_registration,
            font=ctk.CTkFont(**FONTS["button"])
        )
        create_btn.pack(side="left")

    # Login action
    def login(self):
        """
        Function for handling login action
        """
        user_name = self.username.get().strip()
        password = self.password.get().strip()

        if not user_name or not password:
            messagebox.showwarning("Empty input", "Please enter your username and password.")
            return

        user = get_user(user_name)
        if not user or user['password'] != password:
            messagebox.showwarning("Invalid credentials", "Invalid username or password.")
            return

        # Successful login, then we destroy this window and open the MainPage
        self.pack_forget()

        main_page = MainPage(self.master, current_user=user)
        main_page.pack(expand=True, fill="both")

    def open_registration(self):
        RegistrationWindow(self)