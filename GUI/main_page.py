import tkinter as tk
from tkinter import ttk
from Chat import ChatApp

# Main Page with Sidebar + Buttons
class MainPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Recommender System - Main Page")
        self.geometry("1000x650")
        self.configure(bg="#1e1e2e")

        # Sidebar
        self.sidebar = tk.Frame(self, bg="#141421", width=150)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Main Area
        self.main_frame = tk.Frame(self, bg="#1e1e2e")
        self.main_frame.pack(side="left", fill="both", expand=True)

        title_label = tk.Label(self.main_frame,
                               text="Book Recommendation System",
                               font=("Helvetica", 22, "bold"),
                               fg="#c084fc", bg="#1e1e2e")
        title_label.pack(pady=30)

        # Button Canvas Area
        self.button_canvas = tk.Frame(self.main_frame, bg="#1e1e2e")
        self.button_canvas.pack(expand=True)

        # 6 main section buttons
        button_names = [
            "Chat Assistant",
            "Reading Trend",
            "Book Search",
            "User Ratings",
            "ML Model Info",
            "Settings"
        ]

        # Layout 2x3 grid
        rows, cols = 2, 3
        for i in range(rows):
            self.button_canvas.rowconfigure(i, weight=1, pad=20)
        for j in range(cols):
            self.button_canvas.columnconfigure(j, weight=1, pad=20)

        # Create and place buttons
        for idx, name in enumerate(button_names):
            r, c = divmod(idx, 3)
            btn = tk.Button(
                self.button_canvas,
                text=name,
                font=("Helvetica", 15, "bold"),
                fg="white",
                bg="#2a2a3a",
                activebackground="#3b3b4f",
                activeforeground="#c084fc",
                relief="flat",
                width=18,
                height=5,
                command=(self.open_chat if idx == 0 else self.placeholder)
            )
            btn.grid(row=r, column=c, padx=20, pady=20, sticky="nsew")

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


    # Placeholder for other buttons
    def placeholder(self):
        tk.messagebox.showinfo("Coming Soon", "This feature is not implemented yet!")

# Run Main Page
if __name__ == "__main__":
    app = MainPage()
    app.mainloop()

