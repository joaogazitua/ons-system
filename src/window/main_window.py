import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import Calendar

class MainWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Tabelas de Planejamento")
        self.root.geometry("600x400")
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Error.TEntry",
                        fieldbackground="white",
                        borderwidth=2,
                        relief="solid")
        style.map("Error.TEntry",
                  bordercolor=[("focus", "red"), ("!focus", "red")])

        style.configure("TEntry", fieldbackground="white")

        main_frame= ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)


        ttk.Label(main_frame, text="Quantidade de horas totais de desenvolvimento do Projeto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.total_dev_hours = ttk.Entry(main_frame)
        self.total_dev_hours.grid(row=0, column=1, pady=5)

        ttk.Label(main_frame, text="Quantidade de horas de desenvolvimento para cada Sprint:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.total_sprint_dev_hours = ttk.Entry(main_frame)
        self.total_sprint_dev_hours.grid(row=1, column=1, pady=5)

        ttk.Label(main_frame, text="Quantidade de dias por Sprint:").grid(row=2, column=0, sticky=tk.W,pady=5)
        self.days_per_sprint = ttk.Entry(main_frame)
        self.days_per_sprint.grid(row=2, column=1, pady=5)

        ttk.Label(main_frame, text="Data de início da primeira Sprint:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.first_sprint_date = ttk.Entry(main_frame)
        self.first_sprint_date.insert(0, 'dd/mm/yyyy')
        self.first_sprint_date.grid(row=3, column=1, pady=5)
        self.first_sprint_date.bind("<1>", self.pop_up_calendar)

        ttk.Label(main_frame, text="Percentual para testes:").grid(row=4, column=0, sticky=tk.W,pady=5)
        self.percent_for_tests = ttk.Entry(main_frame)
        self.percent_for_tests.grid(row=4, column=1, pady=5)

        ttk.Label(main_frame, text="Percentual para Planning:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.percent_for_planning = ttk.Entry(main_frame)
        self.percent_for_planning.grid(row=5, column=1, pady=5)

        ttk.Label(main_frame, text="Percentual para Review:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.percent_for_review = ttk.Entry(main_frame)
        self.percent_for_review.grid(row=6, column=1, pady=5)

        ttk.Label(main_frame, text="Percentual para Retrospectiva:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.percent_for_retrospective = ttk.Entry(main_frame)
        self.percent_for_retrospective.grid(row=7, column=1, pady=5)

        ttk.Label(main_frame, text="Alocação fixa de horas:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.fixed_alocation = ttk.Entry(main_frame)
        self.fixed_alocation.grid(row=8, column=1, pady=5)

        ttk.Label(main_frame, text="Valor por hora do time de desenvolvimento:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.dev_team_value = ttk.Entry(main_frame)
        self.dev_team_value.grid(row=9, column=1, pady=5)

        genetate_table_btn = ttk.Button(main_frame, text="Gerar Tabela", command=self.generate_table)
        genetate_table_btn.grid(row=20, column=2, columnspan=2, pady=20)

    def pop_up_calendar(self, event):
        global cal, delete_window
        date_window = tk.Toplevel()
        date_window.grab_set()
        date_window.title("Data de início")
        date_window.geometry("250x250+175+75")
        cal = Calendar(date_window, selectmode="day", date_pattern="dd/mm/yyyy")
        cal.grid(row=3, column=2, pady=5)

        submit_btn = ttk.Button(date_window, text="ok", command=self.grab_date)
        submit_btn.grid(row=4, column=2, pady=5)

        delete_window = date_window

    def grab_date(self):
        self.first_sprint_date.delete(0, tk.END)
        self.first_sprint_date.insert(0, cal.get_date())
        delete_window.destroy()

    def validate_input(self, input):
        try:
            return int(input) > 0
        except ValueError:
            return False

    def validate_all_inputs(self):
        entries = [
            self.total_dev_hours,
            self.total_sprint_dev_hours,
            self.days_per_sprint,
            self.percent_for_tests,
            self.percent_for_planning,
            self.percent_for_review,
            self.percent_for_retrospective,
            self.fixed_alocation,
            self.dev_team_value,
        ]
        all_valid = True
        for entry in entries:
            if self.validate_input(entry.get()):
                entry.config(style="TEntry")
            else:
                entry.config(style="Error.TEntry")
                all_valid = False
        if self.first_sprint_date.get() == 'dd/mm/yyyy':
            self.first_sprint_date.config(style="Error.TEntry")
            all_valid = False
        else:
            self.first_sprint_date.config(style="TEntry")
        return all_valid

    def generate_table(self):
        if not self.validate_all_inputs():
            return
        folder = filedialog.askdirectory(title="Escolha a pasta para salvar a tabela")
        if not folder:
            return
        file_path = f"{folder}/table.xlsx"

        print("Generando tabela para o path: ", file_path)