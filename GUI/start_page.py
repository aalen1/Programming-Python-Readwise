import customtkinter as ctk
from tkinter import messagebox

from users_handler_functions import *
from main_page import MainPage
from RegistrationWindow import RegistrationWindow


class StartPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Title
        self.title("Readwise - Login Page")
        self.geometry("600x500")

        # Title Label
        title = ctk.CTkLabel(
            self,
            text = "Welcome to Readwise!",
            font = ctk.CTkFont(size = 32, weight="bold")
        )
        title.pack(pady = (30,10))

        # Login login_form
        login_form = ctk.CTkFrame(self, fg_color="transparent")
        login_form.pack(pady = 20, padx = 40, fill = "x")

        # Username and password variables
        self.username = ctk.StringVar()
        self.password = ctk.StringVar()

        # Username space
        username_label = ctk.CTkLabel(login_form, text = "Username:")
        username_label = ctk.CTkLabel(login_form, text="Username:")
        username_label.pack(anchor="w")
        username_entry = ctk.CTkEntry(login_form, textvariable=self.username, width=250)
        username_entry.pack(pady=(0, 10))

        # Password space
        password_label = ctk.CTkLabel(login_form, text="Password:")
        password_label.pack(anchor="w")
        password_entry = ctk.CTkEntry(login_form, textvariable=self.password, show="*", width=250)
        password_entry.pack(pady=(0, 10))

        # Login Button
        login_btn = ctk.CTkButton(login_form, text="Login", command=self.login)
        login_btn.pack(pady=10)

        # Create account
        link_frame = ctk.CTkFrame(self, fg_color="transparent")
        link_frame.pack(pady=(10, 0))

        link_label = ctk.CTkLabel(link_frame, text="Don't have an account?")
        link_label.pack(side="left", padx=(0, 5))

        # Create account button
        create_btn = ctk.CTkButton(
            link_frame,
            text="Create account",
            fg_color="transparent",
            text_color=("lightblue", "lightblue"),
            hover_color=("gray20", "gray20"),
            command=self.open_registration
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
        self.destroy()
        app = MainPage(current_user=user)
        app.mainloop()

    def open_registration(self):
        RegistrationWindow(self)
