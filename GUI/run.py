from start_page import StartPage
import customtkinter as ctk

if __name__ == "__main__":
    # Set appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Start page
    root = ctk.CTk()
    start = StartPage(master=root)
    start.pack(expand=True, fill="both")
    root.mainloop()