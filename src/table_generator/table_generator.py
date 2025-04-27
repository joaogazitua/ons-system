import math
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd

DATE_FORMAT = "%d/%m/%Y"

class TableGenerator:
    def __init__(self, net_dev_hours, net_sprint_dev_hours, days_per_sprint,
                 first_sprint_date, percent_for_tests, percent_for_planning, percent_for_review,
                 percent_for_retrospective, fixed_alocation, dev_team_value):

        self.net_dev_hours = net_dev_hours
        self.net_sprint_dev_hours = net_sprint_dev_hours
        self.days_per_sprint = days_per_sprint
        self.first_sprint_date = first_sprint_date
        self.percent_for_tests = percent_for_tests
        self.percent_for_planning = percent_for_planning
        self.percent_for_review = percent_for_review
        self.percent_for_retrospective = percent_for_retrospective
        self.fixed_alocation = fixed_alocation
        self.dev_team_value = dev_team_value
        self.number_of_sprints = math.ceil(net_dev_hours/net_sprint_dev_hours)

    def generate_table(self, path):
        data = []
        start_date = self.first_sprint_date
        end_date = self.calculate_ending_date(start_date)
        remaining_dev_hours = self.net_dev_hours
        total_hours_sprint = 0
        try:
            for i in range(self.number_of_sprints):
                record = [f"Sprint {i + 1}"]
                if i != 0:
                    start_date = self.calculate_starting_date(end_date)
                    end_date = self.calculate_ending_date(start_date)

                record.append(start_date)
                record.append(end_date)
                record.append(self.calculate_billing_date(end_date))

                if remaining_dev_hours == 0: raise ValueError("Something went wrong")

                sprint_hours = self.calculate_sprint_hours(remaining_dev_hours)
                total_hours_sprint += sprint_hours
                record.append(sprint_hours)

                if remaining_dev_hours > self.net_sprint_dev_hours:
                    remaining_dev_hours -= self.net_sprint_dev_hours
                else:
                    remaining_dev_hours = 0

                record.append(float(self.calculate_sprint_cost(sprint_hours)))
                record.append(0.00) #Real cost -> will be added manually by user
                record.append(self.get_month(end_date))
                record.append(self.get_year(end_date))
                record.append(self.get_quarter(end_date))

                data.append(record)

            if total_hours_sprint != self.calculate_total_project_hours():
                raise ValueError("Something went wrong")

            columns = ["Sprint", "Data de início", "Data de término", "Data de Faturamento",
                       "Capacidade da Sprint", "Custo Planejado", "Custo Real", "Mês", "Ano", "Trimestre"]

            df = pd.DataFrame(data, columns=columns)
            df.to_excel(path, index=False)
            return True

        except ValueError:
            return False


    def calculate_total_project_hours(self):
        test = self.net_dev_hours * (1.0 + (float (self.percent_for_tests / 100.0)))
        return (self.net_dev_hours +
                test +
                (test * (1.0 + (float (self.percent_for_planning / 100.0)))) +
                (test * (1.0 + (float (self.percent_for_review / 100.0)))) +
                (test * (1.0 + (float (self.percent_for_retrospective / 100.0)))) +
                (self.fixed_alocation*self.number_of_sprints))

    def calculate_sprint_hours(self, remaining_dev_hours):
        sprint_hours = self.net_sprint_dev_hours
        if sprint_hours > remaining_dev_hours:
            sprint_hours = remaining_dev_hours

        test = sprint_hours * (1.0 + (float (self.percent_for_tests / 100.0)))
        sprint_hours = ((sprint_hours + test + (test * (1.0 + (float (self.percent_for_planning / 100.0)))) +
                        (test * (1.0 + (float (self.percent_for_review / 100.0))))) +
                        (test * (1.0 + (float (self.percent_for_retrospective / 100.0))))) + self.fixed_alocation

        return sprint_hours

    def calculate_starting_date(self, previous_end_date):
        if previous_end_date == "":
            return self.first_sprint_date

        start_date = datetime.strptime(previous_end_date, DATE_FORMAT) + timedelta(days=1)
        while start_date.weekday() >= 5:
            start_date -= timedelta(days=1)

        return start_date.strftime(DATE_FORMAT)

    def calculate_ending_date(self, starting_date):
        end_date = datetime.strptime(starting_date, DATE_FORMAT)
        count_days_added = 0

        while count_days_added < self.days_per_sprint:
            end_date = end_date + timedelta(days=1)
            if end_date.weekday() <= 5:
                count_days_added += 1

        return end_date.strftime(DATE_FORMAT)

    def calculate_billing_date(self, end_date):
        billing_date = datetime.strptime(end_date, DATE_FORMAT)
        if billing_date.day <= 20:
            billing_date = billing_date.replace(day=20)
        else:
            billing_date = (billing_date + relativedelta(months=1)).replace(day=20)

        return billing_date.strftime(DATE_FORMAT)


    def calculate_sprint_cost(self, hours):
        return round(hours * self.dev_team_value,2)

    def get_year(self, date):
        _date = datetime.strptime(date, DATE_FORMAT)
        return str(_date.year)

    def get_quarter(self, date):
        _date = datetime.strptime(date, DATE_FORMAT)
        if _date.month <= 3 : return "Trimestre 1"
        if _date.month <= 6 : return "Trimestre 2"
        if _date.month <= 9 : return "Trimestre 3"
        return "Trimestre 4"

    def get_month(self, date):
        months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio",
                  "Junho", "Julho", "Agosto", "Setembro", "Outubro","Novembro", "Dezembro"]
        _date = datetime.strptime(date, DATE_FORMAT)
        return months[_date.month - 1]



