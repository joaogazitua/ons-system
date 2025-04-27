from src.window.main_window import MainWindow
import customtkinter as ctk
if __name__ == "__main__":
    app = ctk.CTk()
    window = MainWindow(app)
    app.mainloop()