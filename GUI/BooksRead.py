import customtkinter as ctk
import tkinter as tk
from users_handler_functions import update_books_read
from tkinter import messagebox

class BooksRead(ctk.CTkToplevel):
    def __init__(self, master, query, books_df, current_user=None):
        super().__init__(master)

        # Create the recommendation window
        self.title("Book Search")
        self.geometry("1000x1200")
        # Variables to store the query and the books_df
        self.query = query
        self.books_df = books_df
        # User logged in
        self.current_user = current_user
        # Books that have being read
        self.check_items = []

        # Make it modal-like
        self.grab_set()

        # Title of frame containing the searched book
        title_label = ctk.CTkLabel(
            self,
            text=f"Search for: \"{query.title()}\"",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        # Selector element to visualize top 3, 5 or 10 results
        selector_frame = ctk.CTkFrame(self, fg_color="transparent")
        selector_frame.pack(pady=(0, 10))

        # Label as complement of the selector
        selector_label = ctk.CTkLabel(
            selector_frame,
            text="Show top:",
            font=ctk.CTkFont(size=14)
        )
        selector_label.pack(side="left", padx=(0, 5))

        # Variable to store the selection (Initialized in 5)
        self.top_n_var = tk.IntVar(value=5)
        # Option Menu of (3,5,10)
        self.top_n_menu = ctk.CTkOptionMenu(
            selector_frame,
            values=["3", "5", "10"],
            command=self.on_top_n_change
        )
        self.top_n_menu.set("5")
        self.top_n_menu.pack(side="left")

        # Container with the search results
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Save & Back Frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Save button, when the users clicks it, the read books are saved in the database
        save_button = ctk.CTkButton(
            buttons_frame,
            text="Save checked books",
            width=120,
            command=self.save_read_books
        )
        save_button.pack(side="left", padx=10)

        # Another close button for this window
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="Back",
            width=120,
            command=self.destroy
        )
        close_btn.pack(side="left", padx=10)

        # Initial render of top 5 recommendation
        self.render_search_results()

    def on_top_n_change(self, value):
        top_n = int(value)
        self.render_search_results(top_n)

    def render_search_results(self, top_n=5):
        """
        Function to render the top "n"search_results
        :param top_n: variable to render n number of search_results, default value of 5.
        :return:
        """
        # Clear all results from the results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        # Reset the check_items list
        self.check_items = []

        # Get the search_results from that books
        books_found = self.get_search_results(self.query, top_n)

        # For book recommended create a particular Frame
        for idx, row in books_found.iterrows():

            # Init the book frame
            book_frame = ctk.CTkFrame(self.results_frame, corner_radius=12, fg_color="#CBDED3")
            book_frame.pack(fill="x", pady=6)

            # Label for the title, if not found: ""
            title_text = row.get("title", "")
            title = ctk.CTkLabel(
                book_frame,
                text=title_text.title(),
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#18181A"
            )
            title.pack(anchor="w", padx=10, pady=(8, 2))

            # Label for the authors(s), if not found: ""
            authors = ctk.CTkLabel(
                book_frame,
                text=f'by {row.get("author(s)", "").title()}',
                font=ctk.CTkFont(size=13),
                text_color="#18181A"
            )
            authors.pack(anchor="w", padx=10)

            # Get the average rating and rating count
            rating = row.get("average_rating", None)
            ratings_count = row.get("ratings_count", None)
            # Create the message for the rating
            rating_text = []
            if rating is not None:
                rating_text.append(f"{rating:.2f}")
            if ratings_count is not None:
                rating_text.append(f"({int(ratings_count):,} ratings)")

            # Label for the average rating
            meta = ctk.CTkLabel(
                book_frame,
                text="  ".join(rating_text),
                font=ctk.CTkFont(size=12),
                text_color="#18181A"
            )
            meta.pack(anchor="w", padx=10, pady=(0, 8))

            # Checkbox to declare that I have read this book
            isbn_val = row.get("isbn13", "") or row.get("isbn", "") or ""
            isbn_str = str(isbn_val)

            var = tk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(
                book_frame,
                text="I have read this book",
                variable=var,
                onvalue=True,
                offvalue=False,
                text_color="#18181A"  # <-- make the label text clearly visible
            )
            chk.pack(anchor="w", padx=10, pady=(0, 8))

            # Store this checkbox + data
            self.check_items.append(
                {"var": var, "title": title_text, "isbn": isbn_str}
            )

    # Search results function
    def get_search_results(self, query, top_n=5):
        """
        Function for search the results from the books dataframe
        :param query:
        :param top_n:
        :return: returns the top n search results from books dataframe
        """
        df = self.books_df.copy()

        mask = (
            df["title"].str.contains(query, case=False, na=False) |
            df["author(s)"].str.contains(query, case=False, na=False)
        )
        df_matches = df[mask].copy()

        if df_matches.empty:
            df_matches = df.copy()

        df_matches = df_matches.sort_values(
            by=["average_rating", "ratings_count"],
            ascending=[False, False]
        )

        return df_matches.head(top_n)

    def save_read_books(self):
        """
        This method saves the books that are checked in the frame to the database as tuples: (title,isbn)
        """
        # Get the books that are checked from the user logged in
        books_read = self.current_user.get("books_read")
        if not isinstance(books_read, set):
            # If is not initialized yet, initialize it
            books_read = set()

        added = 0
        for item in self.check_items:
            if item["var"].get():
                key = (item["title"], item["isbn"])
                if key not in books_read:
                    books_read.add(key)
                    added += 1

        self.current_user["books_read"] = books_read

        # Save the user books read in the database
        username = self.current_user["username"]
        if username:
            update_books_read(username, books_read)

        messagebox.showinfo("Books saved", f"Saved {added} books as read.")