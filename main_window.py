import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

class MainWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Tabelas de Planejamento")
        self.root.geometry("600x400")
        self.setup_ui()

    def setup_ui(self):
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

        ttk.Label(main_frame, text="Data de inicio da primeira Sprint:").grid(row=3, column=0, sticky=tk.W, pady=5)
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

        ttk.Label(main_frame, text="Alocacao fixa de horas:").grid(row=8, column=0, sticky=tk.W, pady=5)
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
        date_window.title("Data de inicio")
        date_window.geometry("250x230+175+85")
        cal = Calendar(date_window, selectmode="day", date_pattern="dd/mm/yyyy")
        cal.grid(row=3, column=2, pady=5)

        submit_btn = ttk.Button(date_window, text="ok", command=self.grab_date)
        submit_btn.grid(row=4, column=2, pady=5)

        delete_window = date_window

    def grab_date(self):
        self.first_sprint_date.delete(0, tk.END)
        self.first_sprint_date.insert(0, cal.get_date())
        delete_window.destroy()



    def generate_table(self):
        project_dev_hours = self.total_dev_hours.get()
        sprint_dev_hours = self.total_sprint_dev_hours.get()
        print(f"Horas totais de desenvolvimento do Projeto: {project_dev_hours}")
        print(f"Horas de desenvolvimento por Sprint: {sprint_dev_hours}")