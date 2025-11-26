import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext, messagebox, ttk

# Main Chat Application
class ChatApp(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color="#1e1e2e")

        # Fonts and colors to use during the chat
        self.user_color = "#93c5fd"
        self.bot_color = "#a5b4fc"
        self.bg_color = "#E2DFDA"
        self.text_color = "#18181A"

        # From the toplevel configure the window
        toplevel = self.winfo_toplevel()
        # Window title
        toplevel.title("Readwise Chat")
        # Window size
        toplevel.geometry("1000x650")
        # Window background
        toplevel.configure(bg="#CBDED3")

        # Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, fg_color="#8DA49A", width=150)
        self.sidebar.pack(side="left", fill="y")
        # Prevent sidebar from shrinking
        self.sidebar.pack_propagate(False)

        # Sidebar label
        sidebar_label = ctk.CTkLabel(
            self.sidebar,
            text="Readwise Chat",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#18181A"
        )
        sidebar_label.pack(pady=15)

        # Main container from the section (Chat)
        self.main_container = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.main_container.pack(side="left", fill="both", expand=True)

        # Label to put the title of the chat
        title_label = ctk.CTkLabel(
            self.main_container,
            text= "Chat and get a book recommendation",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#18181A"
        )
        title_label.pack(pady=10)

        # Chat Display Box
        self.chat_box = ctk.CTkTextbox(
            self.main_container,
            font=ctk.CTkFont(size=13),
            fg_color="#D2C49E",
            text_color=self.text_color,
            wrap="word",
            border_width=0
        )
        self.chat_box.pack(padx=15, pady=10, fill="both", expand=True)
        self.chat_box.insert("end", "Hello! Hello!\n Maybe we could start by telling me what book you just read.\n\n")
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
            fg_color="#3a3a4a",
            text_color=self.text_color,
            border_width=0,
            placeholder_text="Type the title, author or ISBN here..."
        )
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)
        self.user_input.bind("<Return>", self.on_enter)

        # Send Button
        send_button = ctk.CTkButton(
            input_frame,
            text="Send",
            width=80,
            command=self.on_send
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
        # Mock keywords
        keywords = ["harry potter", "hobbit", "mystery","to kill a mockingbird"]
        if any(k in user_msg.lower() for k in keywords):
            return "May you would like:\n• The Hobbit\n• Lord of the Rings\n• Percy Jackson"
        else:
            return "Sorry, I don't know that one. Try mentioning a title or an author!"
