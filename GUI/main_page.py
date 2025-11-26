import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import random
from Chat import ChatApp
from Rating import RatingWindow
from Info import InfoWindow
from Recommendation import RecommendationWindow
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
            placeholder_text = "Get your next book recommendation. Please enter a book title, author, or ISBN...",
            placeholder_text_color = "#8e8e8e",
        )
        # Padding for the search bar
        self.search_entry_bar.pack(side="left", padx=(0,10))

        # Search button
        self.search_button = ctk.CTkButton(
            master = self.search_frame,
            text = "Discover",
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
        button_names = ["Chat Assistant","Top 500 by Avg Rating","Info"]

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

            # Nested if else for assigning the correct helper function to the button
            if name == "Chat Assistant":
                 helper_func= self.open_chat
            elif name == "Top 500 by Avg Rating":
                 helper_func= self.open_rating
            elif name == "Info":
                 helper_func= self.open_info

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
                command=helper_func
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

    # End of the Main Page
    # Helper function aka handlers
    def close_window(self):
        """
        Close main window helper function
        :return: None
        """
        self.destroy()

    # Event to define when the user clicks the search button or presses enter in the search box
    def on_button_search_clicked(self):
        """
        Helper function when the search box is triggered, it searches the input in the dataframe and
        :return: None
        """
        # Get the value from the search box and process it
        query = self.search_entry_bar.get().strip()
        # If the entry is null
        if not query:
            messagebox.showwarning("Empty search", "Please type a book title, author or ISBN.")
            return
        # Declare a variable data for easy manage
        data = self.books_df
        # Check if the title, author or isbn exists
        search_mask = (
                data["title"].str.contains(query, case=False, na=False) |
                data["author(s)"].str.contains(query, case=False, na=False) |
                data["isbn13"].astype(str).str.contains(query, na=False)
        )

        # If the search mask applied to the data is 0, then no match is found
        if data[search_mask].shape[0] == 0:
            messagebox.showwarning(
                "No matched results",
                "No books found matching your search.\n\n"
                "Please try another title, author, or ISBN."
            )
            return

        # Open recommendation window with the information from the search box
        RecommendationWindow(self, query, self.books_df)

        print(f"Search requested for {query}")

    # Switch to Chat Window
    def open_chat(self):
        """
        Helper Function to open the chat window
        :return: None
        """
        # New Toplevel window
        chat_window = tk.Toplevel(self)
        chat_window.title("Readwise Chat")
        chat_window.geometry("1000x650")
        chat_window.configure(bg="#3B6255")

        # ChatApp frame inside this new Toplevel window
        chat_app = ChatApp(master=chat_window)
        chat_app.pack(fill="both", expand=True)

    def open_rating(self):
        """
        Helper Function to open the top 500 window
        :return: None
        """
        RatingWindow(self, self.books_df)

    def open_info(self):
        """
        Helper function to open the Info Window
        :return:
        """
        InfoWindow(self)


# Main Execution
if __name__ == "__main__":
    app = MainPage()
    app.mainloop()

