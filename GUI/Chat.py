# ==========================================
# ChatGPT-like Book Recommender Frontend
# Author: Your Name
# Date: YYYY-MM-DD
# ==========================================

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

# -----------------------------
# Main Chat Application Class
# -----------------------------
class ChatApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,bg="#1e1e2e")

        # Window setup
        self.master.title("Book Recommender Chat")
        self.master.geometry("1000x650")
        self.master.configure(bg="#1e1e2e")

        # Fonts & colors
        self.user_color = "#93c5fd"    # light blue
        self.bot_color = "#a5b4fc"     # lavender
        self.bg_color = "#1e1e2e"
        self.text_color = "#ffffff"
        # Sidebar Frame
        self.sidebar = tk.Frame(self, bg="#141421", width=150)
        self.sidebar.pack(side="left", fill="y")
        # Prevent sidebar from shrinking
        self.sidebar.pack_propagate(False)

        # Title Bar
        title_label = tk.Label(self, text="Book Recommender Chat",
                               font=("Helvetica", 18, "bold"),
                               bg=self.bg_color, fg="#c084fc")
        title_label.pack(pady=10)

        # Chat Display Box
        self.chat_box = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, font=("Helvetica", 13),
            bg="#2a2a3a", fg=self.text_color, relief="flat"
        )
        self.chat_box.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
        self.chat_box.insert(tk.END, "Hello! Tell me what book you just read.\n\n")
        self.chat_box.tag_configure("user", foreground=self.user_color)
        self.chat_box.tag_configure("bot", foreground=self.bot_color)
        self.chat_box.configure(state="disabled")

        # Input Frame
        input_frame = tk.Frame(self, bg=self.bg_color)
        input_frame.pack(fill=tk.X, padx=15, pady=10)

        # Entry Box
        self.user_input = tk.Entry(
            input_frame, font=("Helvetica", 13),
            bg="#3a3a4a", fg=self.text_color, insertbackground="white",
            relief="flat"
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=5)
        self.user_input.bind("<Return>", self.on_enter)

        # Send Button
        send_button = ttk.Button(input_frame, text="Send", command=self.on_send)
        send_button.pack(side=tk.RIGHT)

    # ---------------------------------
    # Event when user presses Send
    # ---------------------------------
    def on_send(self):
        user_msg = self.user_input.get().strip()
        if not user_msg:
            messagebox.showwarning("Empty message", "Please type a message first!")
            return
        self.display_message(f"You: {user_msg}\n", "user")
        self.user_input.delete(0, tk.END)

        # Process / respond (mock logic)
        bot_response = self.generate_response(user_msg)
        self.display_message(f"Bot: {bot_response}\n\n", "bot")

    def on_enter(self, event):
        self.on_send()

    # ---------------------------------
    # Display message in chat box
    # ---------------------------------
    def display_message(self, msg, tag):
        self.chat_box.configure(state="normal")
        self.chat_box.insert(tk.END, msg + "\n", tag)
        self.chat_box.configure(state="disabled")
        self.chat_box.yview(tk.END)

    # ---------------------------------
    # Dummy logic for now (replace later)
    # ---------------------------------
    def generate_response(self, user_msg):
        """Mock response, replace this with real backend call"""
        # Simple keyword-based recommendation mock
        keywords = ["harry potter", "hobbit", "mystery", "romance", "science"]
        if any(k in user_msg.lower() for k in keywords):
            return "Here are some books you might like:\n• The Hobbit\n• Lord of the Rings\n• Percy Jackson"
        else:
            return "Hmm, I don't know that one. Try mentioning a title or genre!"

# -----------------------------
# Main Entry Point
# -----------------------------
if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
