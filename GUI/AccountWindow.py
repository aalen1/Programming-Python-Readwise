import customtkinter as ctk
import ast
from tkinter import messagebox
from users_handler_functions import update_books_read
from palette import COLORS


class AccountWindow(ctk.CTkToplevel):

    def __init__(self, master, user_data):
        super().__init__(master)

        self.user_data = user_data

        self.title("Account Information")
        self.geometry("800x450")
        self.grab_set()
        self.configure(fg_color=COLORS["bg_root"])

        # Title label
        title = ctk.CTkLabel(
            self,
            text="Account Information",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#F9FAFB"
        )
        title.pack(pady=(20, 10))

        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(padx=20, pady=10, fill="x")

        def add_row(label, value):
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=f"{label}:", width=100, anchor="w", text_color="#F9FAFB").pack(side="left")
            ctk.CTkLabel(row, text=value, anchor="w", text_color="#F9FAFB").pack(side="left")

        add_row("Username", user_data.get("username", ""))
        add_row("First name", user_data.get("first_name", ""))
        add_row("Last name", user_data.get("last_name", ""))
        add_row("Birthdate", user_data.get("birth_date", ""))

        # Special section for the books read
        books_read_label = ctk.CTkLabel(
            self,
            text="Books read:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#F9FAFB"
        )
        books_read_label.pack(anchor="w", padx=40, pady=(20, 5))

        # Create a scrollable frame
        self.books_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["primary_btn"],
            width=620,
            height=180,
            corner_radius=8
        )
        self.books_frame.pack(padx=40, pady=(0, 15), fill="x")

        # Render the books list
        self.render_books_list()

        close_btn = ctk.CTkButton(
            self,
            text="Close",
            width=100,
            fg_color=COLORS["primary_btn"],
            hover_color=COLORS["primary_hover"],
            text_color="white",
            command=self.destroy
        )
        close_btn.pack(pady=15)

    def render_books_list(self):
        # Clear previous children frames
        for widget in self.books_frame.winfo_children():
            widget.destroy()

        # Get the books read by the user
        books_read = self.user_data.get("books_read", set())
        if books_read is None or (isinstance(books_read, float)):
            books_read = set()

        # If books_read is a string, try to parse it
        if isinstance(books_read, str):
            try:
                # Library to literal evaluate a string
                books_read = ast.literal_eval(books_read)
            except Exception:
                books_read = set()

        # If the books read set is empty, show a message
        if not books_read:
            empty_label = ctk.CTkLabel(
                self.books_frame,
                text="No books marked as read yet.",
                font=ctk.CTkFont(size=13),
                text_color="#E5E7EB"
            )
            empty_label.pack(pady=10, padx=10, anchor="w")
            return

        # Two columns title and isbn
        header = ctk.CTkFrame(self.books_frame, fg_color="transparent")
        header.pack(fill="x", pady=(4, 2))

        # Title header
        h_title = ctk.CTkLabel(
            header,
            text="Title",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#F9FAFB"
        )
        h_title.pack(side="left", padx=(8, 0))

        # A frame for the right side of the header
        right_header = ctk.CTkFrame(header, fg_color="transparent")
        right_header.pack(side="right", padx=(8, 8))

        # ISBN header
        h_isbn = ctk.CTkLabel(
            right_header,
            text="ISBN",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#F9FAFB"
        )
        h_isbn.pack(side="left", padx=(10, 120))

        # Spacer for the button
        h_action = ctk.CTkLabel(
            right_header,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#F9FAFB"
        )
        h_action.pack(side="left", padx=(0, 0))

        # Sort by title (case insensitive)
        for title, isbn in sorted(list(books_read), key=lambda x: x[0].lower()):
            row = ctk.CTkFrame(self.books_frame, fg_color=COLORS["secondary_btn"], corner_radius=6)
            row.pack(fill="x", pady=3, padx=4)

            # Title label
            title_label = ctk.CTkLabel(
                row,
                text=title,
                font=ctk.CTkFont(size=13),
                text_color="#F9FAFB",
                anchor="w"
            )
            title_label.pack(side="left", padx=(8, 4), pady=4)

            # Right Frame for isbn and remove button
            right_frame = ctk.CTkFrame(row, fg_color="transparent")
            right_frame.pack(side="right", padx=(8, 8), pady=4)

            # ISBN Label
            isbn_label = ctk.CTkLabel(
                right_frame,
                text=isbn,
                font=ctk.CTkFont(size=12),
                text_color="#E5E7EB",
                anchor="e"
            )
            isbn_label.pack(side="left", padx=(10, 16))

            # Remove button
            remove_button = ctk.CTkButton(
                right_frame,
                text="Remove",
                width=80,
                height=26,
                font=ctk.CTkFont(size=12),
                fg_color=COLORS["danger"],
                hover_color=COLORS["danger_hover"],
                text_color="white",
                # Lambda function to remove the book from the user's books read set
                command=lambda t=title, i=isbn: self.remove_book(t, i)
            )
            remove_button.pack(side="left", padx=(0, 0))

    def remove_book(self, title, isbn):
        """
        Method to remove a book from the user's books read set
        :param title: title of the book
        :param isbn: isbn of the book
        """

        books_read = self.user_data.get("books_read", set())
        # In case the book read is empty or Nan
        if not isinstance(books_read, set):
            books_read = set()

        book = (title, isbn)
        if book in books_read:
            books_read.remove(book)

            # Update the in memory variable
            self.user_data["books_read"] = books_read

            # Update the DB
            username = self.user_data.get("username")
            update_books_read(username, books_read)

            # Re-render the books list
            self.render_books_list()

        else:
            messagebox.showinfo("Remove Update", "This book is no longer in your list")