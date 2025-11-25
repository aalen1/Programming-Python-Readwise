import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class ReadingBoard(tk.Tk):
    """
    A modern dark-theme leaderboard page similar to WeChat Reading.
    Left sidebar is fixed; the right panel shows a scrollable list of books.
    """
    def __init__(self):
        super().__init__()
        self.title("Book Leaderboard")
        self.geometry("1100x700")
        self.configure(bg="#1e1e2e")

        # --- Sidebar (fixed) ---
        self.sidebar = tk.Frame(self, bg="#141421", width=160)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="Top Lists",
            bg="#141421",
            fg="#c084fc",
            font=("Helvetica", 18, "bold")
        ).pack(pady=30)

        btn1 = tk.Button(
            self.sidebar,
            text="📚 Literature",
            font=("Helvetica", 14),
            fg="white",
            bg="#2a2a3a",
            activebackground="#3a3a4a",
            relief="flat",
            command=lambda: self.load_list("Literature")
        )
        btn1.pack(fill="x", padx=20, pady=10)

        btn2 = tk.Button(
            self.sidebar,
            text="📖 History",
            font=("Helvetica", 14),
            fg="white",
            bg="#2a2a3a",
            activebackground="#3a3a4a",
            relief="flat",
            command=lambda: self.load_list("History")
        )
        btn2.pack(fill="x", padx=20, pady=10)

        # --- Scrollable Main Area ---
        container = tk.Frame(self, bg="#1e1e2e")
        container.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg="#1e1e2e", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1e1e2e")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Default list
        self.load_list("Literature")

    # -----------------------------------------------------------------
    # Load leaderboard list (category = Literature / History / etc.)
    # -----------------------------------------------------------------
    def load_list(self, category):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        header = tk.Label(
            self.scrollable_frame,
            text=f"{category} Ranking",
            font=("Helvetica", 20, "bold"),
            fg="#c084fc",
            bg="#1e1e2e"
        )
        header.pack(pady=20)

        # Example dataset (you can later load real data from CSV or API)
        books = [
            {
                "rank": 1,
                "title": "Dream of the Red Chamber",
                "reads": "8,281 readers today",
                "recommend": "Recommendation score 91.3%",
                "desc": (
                    "A Chinese literary classic following the rise and fall of a noble family. "
                    "Rich in character portrayal and cultural reflection."
                )
            },
            {
                "rank": 2,
                "title": "The Temple and the Earth",
                "reads": "7,437 readers today",
                "recommend": "Recommendation score 91.5%",
                "desc": (
                    "A philosophical memoir exploring life, faith, and suffering. "
                    "Profoundly moving and thought-provoking."
                )
            },
            {
                "rank": 3,
                "title": "Ordinary World (Complete Trilogy)",
                "reads": "5,886 readers today",
                "recommend": "Recommendation score 91.0%",
                "desc": (
                    "A modern Chinese epic about ordinary people striving amid social change. "
                    "Inspiring and deeply humanistic."
                )
            },
        ]

        for book in books:
            self.create_book_card(book)

    # -----------------------------------------------------------------
    # Create a single book card (rank + title + stats + description)
    # -----------------------------------------------------------------
    def create_book_card(self, book):
        frame = tk.Frame(self.scrollable_frame, bg="#2a2a3a", bd=0, relief="flat")
        frame.pack(fill="x", padx=40, pady=15, ipady=10)

        # Rank label
        rank_label = tk.Label(
            frame,
            text=str(book["rank"]),
            font=("Helvetica", 22, "bold"),
            fg="#c084fc",
            bg="#2a2a3a"
        )
        rank_label.grid(row=0, column=0, rowspan=2, padx=15, sticky="n")

        # Placeholder for book cover
        cover = tk.Frame(frame, bg="#444455", width=70, height=100)
        cover.grid(row=0, column=1, rowspan=2, padx=15, pady=10)
        cover.pack_propagate(False)
        tk.Label(cover, text="Cover", fg="white", bg="#555566").pack(expand=True)

        # Title
        title = tk.Label(
            frame,
            text=book["title"],
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg="#2a2a3a"
        )
        title.grid(row=0, column=2, sticky="w", pady=(10, 0))

        # Info line
        info = tk.Label(
            frame,
            text=f"{book['reads']} | {book['recommend']}",
            font=("Helvetica", 11),
            fg="#a5b4fc",
            bg="#2a2a3a"
        )
        info.grid(row=1, column=2, sticky="w")

        # Description
        desc = tk.Label(
            frame,
            text=book["desc"],
            wraplength=650,
            justify="left",
            fg="#e5e7eb",
            bg="#2a2a3a",
            font=("Helvetica", 11)
        )
        desc.grid(row=2, column=2, sticky="w", pady=(5, 10))

        frame.columnconfigure(2, weight=1)


# ----------------------------------------------------------
# Run demo standalone
# ----------------------------------------------------------
if __name__ == "__main__":
    app = ReadingBoard()
    app.mainloop()
