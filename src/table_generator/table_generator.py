
class TableGenerator:
    def __init__(self, total_dev_hours, total_sprint_dev_hours, days_per_sprint,
                 first_sprint_date, percent_for_tests, percent_for_planning, percent_for_review,
                 percent_for_retrospective, fixed_alocation, dev_team_value):

        self.total_dev_hours = total_dev_hours
        self.total_sprint_dev_hours = total_sprint_dev_hours
        self.days_per_sprint = days_per_sprint
        self.first_sprint_date = first_sprint_date
        self.percent_for_tests = percent_for_tests
        self.percent_for_planning = percent_for_planning
        self.percent_for_review = percent_for_review
        self.percent_for_retrospective = percent_for_retrospective
        self.fixed_alocation = fixed_alocation
        self.dev_team_value = dev_team_value

    def generate_table(self):
        pass

    def calculate_net_hours(self):
        pass

    def calculate_sprint_net_hours(self):
        pass

    def calculate_number_of_sprints(self):
        pass

    def calculate_billing_date(self):
        pass

    def calculate_sprint_cost(self):
        pass

    def generate_year_column(self):
        pass

    def generate_quarter_column(self):
        pass

    def generate_month_column(self):
        pass



