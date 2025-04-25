from table_generator.table_generator import TableGenerator

def test_init():
    generator = TableGenerator(1,1, 1, "1/1/1",
                               1, 1, 1, 1, 1, 1)

    assert generator.total_dev_hours == 1
    assert generator.total_sprint_dev_hours == 1
    assert generator.days_per_sprint == 1
    assert generator.first_sprint_date == "1/1/1"
    assert generator.percent_for_tests == 1
    assert generator.percent_for_planning == 1
    assert generator.percent_for_review == 1
    assert generator.percent_for_retrospective == 1
    assert generator.fixed_alocation == 1
    assert generator.dev_team_value == 1

def test_generate_table():
    pass

def test_calculate_net_hours():
    pass

def test_calculate_sprint_net_hours():
    pass

def test_calculate_number_of_sprints():
    pass

def test_calculate_billing_date():
    pass

def test_calculate_sprint_cost():
    pass

def test_generate_year_column():
    pass

def test_generate_quarter_column():
    pass

def test_generate_month_column():
    pass