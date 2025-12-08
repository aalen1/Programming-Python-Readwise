import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from palette import COLORS, FONTS

class RatingWindow(ctk.CTkToplevel):
    def __init__(self, master, books_df):
        super().__init__(master)

        self.title("Top 500 Books by Average Rating")
        self.geometry("1000x600")
        self.configure(fg_color=COLORS["bg_root"])
        self.grab_set()  # modal-like

        self.books_df = books_df

        # Title Label
        title_label = ctk.CTkLabel(
            self,
            text="Top 500 Books by Average Rating",
            font=ctk.CTkFont(**FONTS["section"]),
            text_color=COLORS["text_light"]
        )
        title_label.pack(pady=(20, 10))

        # Table Frame
        outer_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel"],
            corner_radius=10
        )
        outer_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Table Container
        table_container = ctk.CTkFrame(
            outer_frame,
            fg_color="transparent"
        )
        table_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview Style
        style = ttk.Style(self)
        style.theme_use("clam")

        # First Element configuration
        style.configure(
            "Readwise.Treeview",
            background=COLORS["bg_main"],
            fieldbackground=COLORS["bg_main"],
            foreground=COLORS["text_main"],
            rowheight=24,
        )
        # Second Element configuration
        style.configure(
            "Readwise.Treeview.Heading",
            background=COLORS["primary_btn"],
            foreground="white",
            font=("Helvetica", 11, "bold")
        )
        style.map(
            "Readwise.Treeview",
            background=[("selected", COLORS["primary_hover"])],
            foreground=[("selected", "white")]
        )

        # Create the Treeview columns
        columns = ("avg_rating", "ratings_count", "title", "author", "isbn")

        # Define the Treeview
        tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            style="Readwise.Treeview"
        )

        # Headings
        tree.heading("avg_rating", text="Avg Rating")
        tree.heading("ratings_count", text="Ratings Count")
        tree.heading("title", text="Title")
        tree.heading("author", text="Author(s)")
        tree.heading("isbn", text="ISBN13")

        # Column widths
        tree.column("avg_rating", width=70, anchor="center")
        tree.column("ratings_count", width=70, anchor="center")
        tree.column("title", width=400, anchor="w")
        tree.column("author", width=220, anchor="w")
        tree.column("isbn", width=70, anchor="center")

        # Scrollbars
        y_scroll = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=tree.yview
        )
        x_scroll = ttk.Scrollbar(
            table_container,
            orient="horizontal",
            command=tree.xview
        )
        # Add the scrollbars to the Treeview
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Spaces for the visualization of the tree
        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

        # Fill the data
        books_top = self.books_df.copy()
        books_top = books_top[books_top["ratings_count"] > 100]
        books_top = books_top.sort_values(["average_rating", "ratings_count"], ascending=[False, False])
        # Get the top 500 books
        top500 = books_top.head(500)[["title", "author(s)","isbn13", "average_rating", "ratings_count"]]
        # For each row of the dataframe
        for _, row in top500.iterrows():
            title = str(row.get("title", ""))
            author = str(row.get("author(s)", ""))
            isbn = str(row.get("isbn13", ""))
            avg = row.get("average_rating", "")
            count = row.get("ratings_count", "")

            # Format the average rating and count
            avg_str = f"{avg:.2f}"
            cnt_str = f"{int(count):,}"

            tree.insert(
                "",
                "end",
                values=(avg_str, cnt_str, title, author, isbn)
            )

        # -------- Back button ----------
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        back_btn = ctk.CTkButton(
            btn_frame,
            text="Back",
            width=120,
            fg_color=COLORS["primary_btn"],
            hover_color=COLORS["primary_hover"],
            font=ctk.CTkFont(**FONTS["button"]),
            text_color="white",
            command=self.destroy,
        )
        back_btn.pack()