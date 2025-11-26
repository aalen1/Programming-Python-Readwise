import customtkinter as ctk
import tkinter as tk

class RecommendationWindow(ctk.CTkToplevel):
    def __init__(self, master, query, books_df):
        super().__init__(master)

        # Create the recommendation window
        self.title("Book Recommendations")
        self.geometry("750x500")
        self.query = query
        self.books_df = books_df

        # Make it modal-like
        self.grab_set()

        # Title of frame containing the searched book
        title_label = ctk.CTkLabel(
            self,
            text=f"Recommendations for: \"{query}\"",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        # Selector element to visualize top 3, 5 or 10 recommendations
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

        # Container with the recommendations
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Another close button for this window
        close_btn = ctk.CTkButton(self, text="Back", width=100, command=self.destroy)
        close_btn.pack(pady=10)

        # Initial render of top 5 recommendation
        self.render_recommendations()

    def on_top_n_change(self, value):
        top_n = int(value)
        self.render_recommendations(top_n)

    def render_recommendations(self, top_n=5):
        """
        Function to render the top "n" recommendations
        :param top_n: variable to render n number of recommendations, default value of 5.
        :return:
        """
        # Clear all results from the results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Get the recommendations from that books
        books_recommended = self.get_recommendations(self.query, top_n)

        # For book recommended create a particular Frame
        for idx, row in books_recommended.iterrows():
            # Init the book frame
            book_frame = ctk.CTkFrame(self.results_frame, corner_radius=12, fg_color="#CBDED3")
            book_frame.pack(fill="x", pady=6)
            # Label for the title, if not found: ""
            title = ctk.CTkLabel(
                book_frame,
                text=row.get("title", ""),
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#18181A"
            )
            title.pack(anchor="w", padx=10, pady=(8, 2))
            # Label for the authors(s), if not found: ""
            authors = ctk.CTkLabel(
                book_frame,
                text=f'by {row.get("author(s)", "")}',
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
            # Label for the average rating and
            meta = ctk.CTkLabel(
                book_frame,
                text="  ".join(rating_text),
                font=ctk.CTkFont(size=12),
                text_color="#18181A"
            )
            meta.pack(anchor="w", padx=10, pady=(0, 8))

    # recommendations function
    def get_recommendations(self, query, top_n=5):
        """
        Function for recommendations
        :param query:
        :param top_n:
        :return:
        """
        # Placeholder code
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

