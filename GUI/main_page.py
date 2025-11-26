import tkinter as tk
import customtkinter as ctk
import random
from tkinter import ttk
from Chat import ChatApp
from Rating import RatingWindow
from Info import InfoWindow
import pandas as pd

# Main Page with Sidebar + Buttons
class MainPage(tk.Tk):
    def __init__(self):
        # Custom Tkinter Theme
        super().__init__()
        # ----------- Main window setup
        # Window title and size
        self.title("Readwise your Personal Book Recommendation Assistant")
        self.geometry("1200x600")
        # General background color
        self.configure(bg="#3B6255")
        # Data of the books
        self.books_df = pd.read_csv("./data/final_df.csv")

        # Sidebar Customization
        self.sidebar = tk.Frame(self, bg="#D2C49E", width=120)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Main Area
        self.main_frame = tk.Frame(self, bg="#CBDED3")
        self.main_frame.pack(side="left", fill="both", expand=True)

        # Randomize the welcome message
        if random.random() < 0.5:
            title_text = "Welcome to Readwise!"
        else:
            title_text = "It's time to start reading!"

        title_label = ctk.CTkLabel(
            self.main_frame,
            text=title_text,
            font=ctk.CTkFont(family="Georgia Italic", size=38, weight="bold"),
            text_color = '#18181A',
            fg_color='transparent'
        )
        # Padding after the title
        title_label.pack(pady=60)

        # ----------- Search bar container
        self.search_frame = ctk.CTkFrame(self.main_frame, corner_radius=20, fg_color = "transparent")
        self.search_frame.pack(pady=(0,30))


        # Same height for the search bar and the search button
        height_search_bar = 46

        # Search entry
        self.search_entry_bar = ctk.CTkEntry(
            master = self.search_frame,
            width = 800,
            corner_radius = 20,
            border_width = 3,
            border_color = "#8e8e8e",
            height = height_search_bar,
            placeholder_text = "Search by title, author, or ISBN...",
            placeholder_text_color = "#8e8e8e",
        )
        # Padding for the search bar
        self.search_entry_bar.pack(side="left", padx=(0,10))

        # Search button
        self.search_button = ctk.CTkButton(
            master = self.search_frame,
            text = "Search",
            width = 30,
            height = height_search_bar,
            command = self.on_button_search_clicked
        )
        self.search_button.pack(side="left")

        # Also, press enter to trigger search
        self.search_entry_bar.bind("<Return>", lambda event: self.on_button_search_clicked())

        # ------------ Buttons Canvas Area
        # Button Canvas Area
        self.button_canvas = ctk.CTkFrame(self.main_frame, corner_radius=20, fg_color = "#CBDED3")
        self.button_canvas.pack(expand=True, pady=10)

        # 3 main section buttons
        button_names = ["Chat Assistant","Top 500","Info"]

        # Another grid frame (to center everything)
        buttons_frame = ctk.CTkFrame(self.button_canvas, fg_color = "#CBDED3")
        buttons_frame.pack(pady=10)

        # Layout 2x3 grid
        rows, cols = 1, 3
        for i in range(rows):
            self.button_canvas.rowconfigure(i, weight=1, pad=20)
        for j in range(cols):
            self.button_canvas.columnconfigure(j, weight=1, pad=20)

        # Build the 3 buttons in one row
        for i, name in enumerate(button_names):

            if name == "Chat Assistant":
                cmd = self.open_chat
            elif name == "Top 500":
                cmd = self.open_rating
            elif name == "Info":
                cmd = self.open_info

            btn = ctk.CTkButton(
                master=buttons_frame,
                text=name,
                width=200,
                height=80,
                corner_radius=15,
                font=ctk.CTkFont(size=18, weight="bold"),
                fg_color="#1F1F33",
                hover_color="#2A2A44",
                text_color="white",
                command=cmd
            )
            btn.grid(row=0, column=i, padx=25, pady=20)

        # Extra padding at the bottom
        self.button_canvas.pack(pady=10)

        # ------------ (Close button)
        self.close_canvas = ctk.CTkFrame(self.main_frame, corner_radius=20, fg_color="transparent")
        self.close_canvas.pack(expand=True, pady=10)

        close_button = ctk.CTkButton(
            master = self.close_canvas,
            text="Close",
            width = 120,
            height = 35,
            corner_radius = 8,
            fg_color="#8B1E3F",
            hover_color="#A22A50",
            command=self.close_window
        )
        close_button.pack(side="bottom",pady=10)

    # ------------- End of Main Page
    # ------------- Event Handlers
    def close_window(self):
        self.destroy()

    # Event to define when the user clicks the search button
    def on_button_search_clicked(self):
        query = self.search_entry_bar.get().strip()
        if not query:
            return

        print(f"Search requested for {query}")

    # Switch to Chat Window
    def open_chat(self):
        # Hide the main page content
        self.main_frame.pack_forget()
        self.sidebar.pack_forget()

        # Create a new frame to hold the chat page within the same window
        self.chat_frame = tk.Frame(self, bg="#1e1e2e")
        self.chat_frame.pack(fill="both", expand=True)

        # Initialize the ChatApp interface inside this new frame
        chat_app = ChatApp()
        chat_app.master = self.chat_frame   # Reassign the container
        chat_app.pack(fill="both", expand=True)

    def open_rating(self):
        RatingWindow(self, self.books_df)

    def open_info(self):
        InfoWindow(self)


# Run Main Page
if __name__ == "__main__":
    app = MainPage()
    app.mainloop()

