import tkinter as tk
import customtkinter as ctk
from ttkbootstrap.widgets.tableview import Tableview

class RatingWindow(ctk.CTkToplevel):
    def __init__(self,master,books_df):
        super().__init__(master)
        # Define the window title
        self.title("Book Ratings")
        self.geometry("900x800")

        # Columns of interest
        cols = ["average_rating", "ratings_count","title", "author(s)"]

        # Filter the columns of interest
        view_df = books_df[cols].copy()

        # Only keep the ratings with more than 100 views
        view_df = view_df[view_df["ratings_count"] > 100]
        view_df = view_df.sort_values(by=["average_rating"],ascending=False)

        view_df = view_df.head(500).reset_index(drop=True)

        # Table frame
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # Create the tableview with ttkbootstrap
        self.table = Tableview(
            master=table_frame,
            coldata=list(view_df.columns),
            rowdata=view_df.values.tolist(),
            paginated=True,
            pagesize=25,
            searchable=True,
            bootstyle="info",
            stripecolor=("#F8F9Fa", "#E9ECEF"),
        )
        self.table.pack(fill="both", expand=True)

        # Autofit columns
        self.table.autofit_columns()

        # Close button at the bottom
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(0, 15))

        close_btn = ctk.CTkButton(
            master=button_frame,
            text="Back",
            width=100,
            command=self.destroy,
        )
        close_btn.pack()



