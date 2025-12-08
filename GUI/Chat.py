import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from recommender_funcs import recommend
from palette import COLORS

# Main Chat Application
class ChatApp(ctk.CTkFrame):
    def __init__(self, master=None, books_df=None, clustered_df=None, current_user=None):
        super().__init__(master, fg_color=COLORS["bg_main"])

        # References
        self.books_df = books_df
        self.current_user = current_user
        self.clustered_df = clustered_df

        # Fonts and colors to use during the chat
        self.user_color = "#040E18"
        self.bot_color = COLORS["text_main"]
        self.bg_color = COLORS["bg_main"]
        self.text_color = COLORS["text_main"]

        # From the toplevel configure the window
        toplevel = self.winfo_toplevel()
        # Window title
        toplevel.title("Readwise Chat")
        # Window size
        toplevel.geometry("1000x650")
        # Window background
        toplevel.configure(fg_color=COLORS["bg_main"])

        # Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, fg_color=COLORS["bg_sidebar"], width=150)
        self.sidebar.pack(side="left", fill="y")
        # Prevent sidebar from shrinking
        self.sidebar.pack_propagate(False)

        # Sidebar label
        sidebar_label = ctk.CTkLabel(
            self.sidebar,
            text="Readwise Chat",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_main"],
        )
        sidebar_label.pack(pady=15)

        # Main container from the section (Chat)
        self.main_container = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.main_container.pack(side="left", fill="both", expand=True)

        # Label to put the title of the chat
        title_label = ctk.CTkLabel(
            self.main_container,
            text="Chat and get a book recommendation",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_main"],
        )
        title_label.pack(pady=10)

        # Chat Display Box
        self.chat_box = ctk.CTkTextbox(
            self.main_container,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["panel"],
            text_color=self.bot_color,
            wrap="word",
            border_width=0,
        )
        self.chat_box.pack(padx=15, pady=10, fill="both", expand=True)
        # Initial message from the bot
        self.chat_box.insert(
            "end",
            "Hello! Hello!\n "
            "I'm here to help you find the next book to read.\n\n"
            "Please enter ONE of the following:\n"
            " - An ISBN-13 (only digits)\n"
            " - A book title\n"
            " - An author's name\n\n"
            "I will try to find a book that matches your request.\n\n",
        )
        self.chat_box.tag_config("user", foreground=self.user_color)
        self.chat_box.tag_config("bot", foreground=self.bot_color)
        self.chat_box.configure(state="disabled")

        # Input Frame
        input_frame = ctk.CTkFrame(self.main_container, fg_color=self.bg_color)
        input_frame.pack(fill="x", padx=15, pady=10)

        # Input Box
        self.user_input = ctk.CTkEntry(
            input_frame,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["entry_bg"],
            text_color="#F9FAFB",
            border_width=0,
            placeholder_text="Type the title, author or ISBN here...",
        )
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)
        self.user_input.bind("<Return>", self.on_enter)

        # Send Button
        send_button = ctk.CTkButton(
            input_frame,
            text="Send",
            width=80,
            fg_color=COLORS["primary_btn"],
            hover_color=COLORS["primary_hover"],
            text_color="white",
            command=self.on_send,
        )
        send_button.pack(side="right")

        # Close button at the bottom
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(pady=(0, 15))

        # Close button with helper function to destroy the top level.
        close_btn = ctk.CTkButton(
            master=button_frame,
            text="Back",
            width=100,
            fg_color=COLORS["primary_btn"],
            hover_color=COLORS["primary_hover"],
            text_color="white",
            command=self.close_window,
        )
        close_btn.pack()

    def close_window(self):
        # Destroy the top-level window that contains this frame
        self.winfo_toplevel().destroy()

    # Event when the button "send" is clicked
    def on_send(self):
        """
        Helper function when the button "send" is clicked
        :return:
        """
        user_msg = self.user_input.get().strip()
        # If the input message is empty
        if not user_msg:
            messagebox.showwarning("Empty input", "Please type a message.")
            return
        # Display message from the user
        self.display_message(f"You: {user_msg}", "user")
        self.user_input.delete(0, tk.END)

        # Bot Response
        bot_response = self.generate_response(user_msg)
        self.display_message(f"Bot: {bot_response}\n", "bot")

    # Event when the button send is clicked
    def on_enter(self, event):
        self.on_send()

    # Display Message
    def display_message(self, message, tag):
        """
        Helper function for the display message
        :param message:
        :param tag:
        :return:
        """
        self.chat_box.configure(state="normal")
        self.chat_box.insert(tk.END, message + "\n", tag)
        self.chat_box.configure(state="disabled")
        self.chat_box.yview(tk.END)

    # [Dummy logic]
    def generate_response(self, user_msg):

        # Base case when the books df does not exist.
        if self.books_df is None:
            return "Sorry, I'm not able to provide recommendations now."

        # Store the books in a variable
        books = self.books_df.copy()
        clustered = self.clustered_df.copy()

        # Ensure isbn13 is a string
        if "isbn13" in books.columns:
            books["isbn13"] = books["isbn13"].astype(str)
        if "isbn13" in clustered.columns:
            clustered["isbn13"] = clustered["isbn13"].astype(str)

        # Validate the input from the user:
        if not any(ch.isalnum() for ch in user_msg):
            return (
                "I couldn't understand your request.\n\n"
                "Please enter ONE of the following:"
                " - An ISBN-13 (only digits)\n"
                " - A book title\n"
                " - An author's name\n\n"
            )

        # ISBN detection
        isbn = None
        isbn_candidate = "".join(charac for charac in user_msg if charac.isdigit())

        # Check the length of the candidate
        if len(isbn_candidate) == 13:
            # Check that this isbn exists in BOTH the book df and the clustered df
            if (books["isbn13"] == isbn_candidate).any() and (
                clustered["isbn13"] == isbn_candidate
            ).any():
                isbn = isbn_candidate

        # If no ISBN is found, we search for book titles and authors
        if isbn is None:
            # Mask for the search of title or author
            mask = (
                books["title"].str.contains(user_msg, case=False, na=False)
                | books["author(s)"].str.contains(user_msg, case=False, na=False)
            )
            # Get the books that match the mask
            matches = books[mask]

            # If the matches are empty
            if matches.empty:
                return (
                    "I couldn't find any book matching your request.\n\n"
                    "Please enter ONE of the following:"
                    " - An ISBN-13 (only digits)\n"
                    " - A book title\n"
                    " - An author's name\n\n"
                )
            isbn = None
            for _, row in matches.iterrows():
                isbn_candidate = str(row["isbn13"])
                if (clustered["isbn13"] == isbn_candidate).any():
                    isbn = isbn_candidate
                    break

        # Get the recommendations
        rec_idx = recommend(isbn, clustered, n=3)

        # If the recommendations are empty
        if not rec_idx:
            return "Sorry, I couldn't find similar books for the input provided."

        # Format recommendations
        # Get the book title
        book_title = books.loc[books["isbn13"] == str(isbn)]["title"].iloc[0]
        # Capitalize
        book_title = book_title.capitalize()

        msg = [f"Here are the books recommended for {book_title.title()}:"]

        for idx in rec_idx:
            cluster_row = clustered.iloc[idx]
            rec_isbn = str(cluster_row["isbn13"])

            # Find this ISBN in the books df
            book_rows = books[books["isbn13"] == rec_isbn]
            if book_rows.empty:
                continue
            book = book_rows.iloc[0]
            title = str(book.get("title", "<No Title>"))
            author = str(book.get("author(s)", "<No Author>"))
            msg.append(f"- {title.title()} by {author.title()}")

        helper_txt = (
            "\n\nAsk for another recommendation! Please enter ONE of the following:\n"
            " - An ISBN-13 (only digits)\n"
            " - A book title\n"
            " - An author's name\n\n"
        )

        return "\n".join(msg) + helper_txt