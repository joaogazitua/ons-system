from table_generator.table_generator import TableGenerator
import math

def test_init():
    generator = TableGenerator(10,3, 1, "1/1/1",
                               1, 1, 1, 1,
                               1, 1)

    assert generator.net_dev_hours == 10
    assert generator.net_sprint_dev_hours == 3
    assert generator.days_per_sprint == 1
    assert generator.first_sprint_date == "1/1/1"
    assert generator.percent_for_tests == 1
    assert generator.percent_for_planning == 1
    assert generator.percent_for_review == 1
    assert generator.percent_for_retrospective == 1
    assert generator.fixed_alocation == 1
    assert generator.dev_team_value == 1
    assert generator.number_of_sprints == 4

def test_calculate_total_project_hours():
    gen = TableGenerator(100, 1,1,"1/1/1",
                         30,20, 10, 10,
                         10, 10)
    t = gen.net_dev_hours * 1.3
    x = gen.net_dev_hours + t + (t * 1.2) + (t * 1.1) + (t * 1.1) + (gen.fixed_alocation * (math.ceil(gen.net_dev_hours / gen.net_sprint_dev_hours)))
    net = gen.calculate_total_project_hours()

    assert net == x

def test_calculate_sprint_hours():
    gen = TableGenerator(100, 100, 1, "1/1/1",
                         30, 20, 10, 10,
                         10, 10)

    hours_1 = gen.calculate_sprint_hours(200)
    hours_2 = gen.calculate_sprint_hours(50)

    assert hours_1 == 682
    assert hours_2 == 346

def test_calculate_starting_date():
    gen = TableGenerator(100, 1, 5, "26/04/2025",
                         30, 20, 10, 10,
                         10, 10)

    end = "28/04/2025"
    start = gen.calculate_starting_date(end)

    assert start == "29/04/2025"

def test_calculate_ending_date():
    gen = TableGenerator(100, 1, 5, "26/04/2025",
                         30, 20, 10, 10,
                         10, 10)

    start = "26/04/2025"
    end = gen.calculate_ending_date(start)

    assert end == "02/05/2025"

def test_calculate_billing_date():
    gen = TableGenerator(100, 1, 5, "26/04/2025",
                         30, 20, 10, 10,
                         10, 10)
    bd_1 = gen.calculate_billing_date("01/12/2025")
    bd_2 = gen.calculate_billing_date("20/12/2025")
    bd_3 = gen.calculate_billing_date("21/12/2025")
    bd_4 = gen.calculate_billing_date("05/06/2025")
    bd_5 = gen.calculate_billing_date("20/06/2025")
    bd_6 = gen.calculate_billing_date("21/06/2025")

    assert bd_1 == "20/12/2025"
    assert bd_2 == "20/12/2025"
    assert bd_3 == "20/01/2026"
    assert bd_4 == "20/06/2025"
    assert bd_5 == "20/06/2025"
    assert bd_6 == "20/07/2025"


def test_calculate_sprint_cost():
    gen = TableGenerator(100, 1, 5, "26/04/2025",
                         30, 20, 10, 10,
                         10, 10)

    result = gen.calculate_sprint_cost(300)
    assert result == 3000

def test_get_year():
    gen = TableGenerator(100, 1, 5, "26/04/2025",
                         30, 20, 10, 10,
                         10, 10)

    year = gen.get_year(gen.first_sprint_date)

    assert year == "2025"


def test_get_quarter():
    gen = TableGenerator(100, 1, 5, "26/04/2025",
                         30, 20, 10, 10,
                         10, 10)
    q_1 = gen.get_quarter("01/01/2025")
    q_2 = gen.get_quarter("02/04/2025")
    q_3 = gen.get_quarter("03/07/2025")
    q_4 = gen.get_quarter("04/10/2025")

    assert q_1 == "Trimestre 1"
    assert q_2 == "Trimestre 2"
    assert q_3 == "Trimestre 3"
    assert q_4 == "Trimestre 4"

def test_get_month():
    gen = TableGenerator(100, 1, 5, "26/04/2025",
                         30, 20, 10, 10,
                         10, 10)
    d1 = gen.get_month("01/01/2025")
    d2 = gen.get_month("02/02/2025")
    d3 = gen.get_month("03/03/2025")
    d4 = gen.get_month("04/04/2025")
    d5 = gen.get_month("05/05/2025")
    d6 = gen.get_month("06/06/2025")
    d7 = gen.get_month("07/07/2025")
    d8 = gen.get_month("08/08/2025")
    d9 = gen.get_month("09/09/2025")
    d10 = gen.get_month("10/10/2025")
    d11 = gen.get_month("11/11/2025")
    d12 = gen.get_month("12/12/2025")

    assert d1 == "Janeiro"
    assert d2 == "Fevereiro"
    assert d3 == "Março"
    assert d4 == "Abril"
    assert d5 == "Maio"
    assert d6 == "Junho"
    assert d7 == "Julho"
    assert d8 == "Agosto"
    assert d9 == "Setembro"
    assert d10 == "Outubro"
    assert d11 == "Novembro"
    assert d12 == "Dezembro"

