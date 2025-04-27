import customtkinter as ctk
from tkinter import filedialog
from tkcalendar import Calendar
from table_generator.table_generator import TableGenerator

ctk.set_appearance_mode("Dark")  # "Dark", "Light", or "System"
ctk.set_default_color_theme("blue")

MAIN_WIDTH = 600
MAIN_HEIGHT = 500
POP_UP_CALENDAR_WIDTH = 250
POP_UP_CALENDAR_HEIGHT = 250
POP_UP_WIDTH = 250
POP_UP_HEIGHT = 150
DATE_PATTERN = "dd/mm/yyyy"

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Tabelas de Planejamento")
        self.centralize_window(self.root, MAIN_WIDTH, MAIN_HEIGHT)
        self.setup_ui()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Entradas
        labels_texts = [
            "Quantidade de horas totais de desenvolvimento do Projeto:",
            "Quantidade de horas de desenvolvimento para cada Sprint:",
            "Quantidade de dias por Sprint:",
            "Data de início da primeira Sprint:",
            "Percentual para testes:",
            "Percentual para Planning:",
            "Percentual para Review:",
            "Percentual para Retrospectiva:",
            "Alocação fixa de horas:",
            "Valor por hora do time de desenvolvimento:"
        ]

        self.entries = []

        for idx, text in enumerate(labels_texts):
            label = ctk.CTkLabel(main_frame, text=text)
            label.grid(row=idx, column=0, sticky="w", pady=5)

            entry = ctk.CTkEntry(main_frame, width=200)
            entry.grid(row=idx, column=1, pady=5)

            if "Data" in text:
                entry.insert(0, DATE_PATTERN)
                entry.bind("<Button-1>", self.pop_up_calendar)
                self.first_sprint_date = entry
            else:
                self.entries.append(entry)

        # Botão gerar tabela
        generate_btn = ctk.CTkButton(main_frame, text="Gerar Tabela", command=self.generate_table)
        generate_btn.grid(row=20, column=0, columnspan=2, pady=20)

    def centralize_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def pop_up_calendar(self, event):
        global cal, delete_window
        date_window = ctk.CTkToplevel()
        date_window.grab_set()
        date_window.title("Data de início")
        self.centralize_window(date_window, POP_UP_CALENDAR_WIDTH, POP_UP_CALENDAR_HEIGHT)
        cal = Calendar(date_window, selectmode="day", date_pattern=DATE_PATTERN)
        cal.pack(pady=10)
        submit_btn = ctk.CTkButton(date_window, text="OK", command=self.grab_date)
        submit_btn.pack(pady=10)
        delete_window = date_window

    def grab_date(self):
        self.first_sprint_date.delete(0, "end")
        self.first_sprint_date.insert(0, cal.get_date())
        delete_window.destroy()

    def safe_float(self, entry_widget):
        try:
            text = entry_widget.get().replace(",", ".")
            return float(text)
        except ValueError:
            raise ValueError(f"Valor inválido no campo: {entry_widget}")

    def validate_float(self, value):
        try:
            value = value.replace(",", ".")
            return float(value) > 0
        except ValueError:
            return False

    def validate_all_inputs(self):
        for entry in self.entries:
            entry.configure(border_color="gray")
        self.first_sprint_date.configure(border_color="gray")

        for entry in self.entries:
            if not self.validate_float(entry.get()):
                entry.configure(border_color="red")
                return False
            entry.configure(border_color="gray")

        if self.safe_float(self.entries[1]) > self.safe_float(self.entries[0]):
            self.entries[1].configure(border_color="red")
            return False

        self.entries[1].configure(border_color="gray")

        if self.first_sprint_date.get() == DATE_PATTERN:
            self.first_sprint_date.configure(border_color="red")
            return False

        self.first_sprint_date.configure(border_color="gray")
        return True

    def pop_up_message(self, title, message):
        popup = ctk.CTkToplevel()
        popup.title(title)
        self.centralize_window(popup, POP_UP_WIDTH, POP_UP_HEIGHT)
        label = ctk.CTkLabel(popup, text=message)
        label.pack(pady=20)
        ok_button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)
        popup.grab_set()

    def generate_table(self):
        if not self.validate_all_inputs():
            self.pop_up_message("Erro", "Dados inválidos. Corrija os campos.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Escolha onde salvar a tabela",
            defaultextension=".xlsx",
            filetypes=[("Planilhas Excel", "*.xlsx")],
            initialfile="table.xlsx"
        )
        if not file_path:
            return

        generator = TableGenerator(
            self.safe_float(self.entries[0]),
            self.safe_float(self.entries[1]),
            self.safe_float(self.entries[2]),
            self.first_sprint_date.get(),
            self.safe_float(self.entries[3]),
            self.safe_float(self.entries[4]),
            self.safe_float(self.entries[5]),
            self.safe_float(self.entries[6]),
            self.safe_float(self.entries[7]),
            self.safe_float(self.entries[8])
        )

        if generator.generate_table(file_path):
            self.pop_up_message("Sucesso", "Tabela criada com sucesso.")
        else:
            self.pop_up_message("Erro", "Erro ao gerar a tabela.")
