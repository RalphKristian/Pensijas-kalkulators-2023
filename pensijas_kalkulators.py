import matplotlib.pyplot as plt
import sqlite3
import json
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect("datasheet.db")

LEVEL1_INDEXATION_RATE = 0.0353
LEVEL2_3_NOMINAL_YIELD = 0.0506
AVERAGE_SALARY_INCREASE = 0.0421
INFLATION_RATE = 0.0200
RETIREMENT_AGE = 64

def validate_salary(new_value):
    if new_value.isdigit() or (new_value == "" and entry_salary.index("end") == 0):
        return True
    else:
        return False

def validate_age(new_value):
    if new_value.isdigit():
        return True
    else:
        return False

def validate_years_in_service(new_value):
    if new_value.isdigit():
        return True
    else:
        return False

def validate_accumulation_input(new_value):
    if new_value.isdigit() or (new_value == "" and entry_accumulation.index("end") == 0):
        return True
    else:
        return False

def validate_contribution_years(new_value):
    if new_value.isdigit():
        return True
    else:
        return False

def get_inputs():
    salary = entry_salary.get()
    age = entry_age.get()
    years_in_service = entry_service.get()
    accumulation_input = entry_accumulation.get()
    contribution_years_for_pension_level_3 = entry_contribution.get()

    if not salary.isdigit() or int(salary) > 1000000:
        messagebox.showerror("Invalid salary", "Salary must be a positive number less than or equal to 1000000.")
        return None
    
    if not age.isdigit() or int(age) < 15:
        messagebox.showerror("Invalid age", "Age must be a positive number greater than or equal to 15.")
        return None
    
    if not years_in_service.isdigit():
        messagebox.showerror("Invalid years in service", "Years in service must be a positive number.")
        return None
    
    if not accumulation_input.isdigit() or int(accumulation_input) < 0:
        messagebox.showerror("Invalid accumulation input", "Accumulation input must be a non-negative number.")
        return None
    
    if not contribution_years_for_pension_level_3.isdigit():
        messagebox.showerror("Invalid contribution years for pension level 3", "Contribution years for pension level 3 must be a positive number.")
        return None
    
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS datasheet (id INTEGER PRIMARY KEY, age VARCHAR, salary VARCHAR, service VARCHAR, accumulation VARCHAR, contribution VARCHAR)")
    
    cursor.execute("INSERT INTO datasheet (age, salary, service, accumulation, contribution) VALUES (?, ?, ?, ?, ?)", (age, salary, years_in_service, accumulation_input, contribution_years_for_pension_level_3))

    conn.commit()
    
    return (
        salary or None,
        age or None,
        years_in_service or None,
        accumulation_input or None,
        contribution_years_for_pension_level_3 or None,
    )

def calculate_level1_pension():
    try:
        salary, age, years_in_service, accumulation_input, contribution_years_for_pension_level_3 = get_inputs()
        salary = float(salary)
        years_in_service = float(years_in_service)
        level1_pension_year = (14/100) * salary * 12
        level1_pension_year_inflation_rate = INFLATION_RATE * salary * 12
        level_1_pension_yearly_increase = level1_pension_year * LEVEL1_INDEXATION_RATE
        level1_pension_increase_by_year = level1_pension_year + level_1_pension_yearly_increase - level1_pension_year_inflation_rate * years_in_service

        label_result.config(text="Level 1 Pension:" + str(abs(round(level1_pension_increase_by_year, 2))))
        return level1_pension_increase_by_year
    
    except ValueError:
        label_result.config(text="Please enter valid numbers")

def calculate_level2_pension_year():
    try:
        salary, age, years_in_service, accumulation_input, contribution_years_for_pension_level_3 = get_inputs()
        salary = float(salary)
        years_in_service = float(years_in_service)
        level2_pension_year = (6/100) * salary * 12
        level2_pension_year_inflation_rate = INFLATION_RATE * salary * 12
        level_2_pension_yearly_increase = level2_pension_year * LEVEL2_3_NOMINAL_YIELD
        level2_pension_increase_by_year = level2_pension_year + level_2_pension_yearly_increase - level2_pension_year_inflation_rate * years_in_service

        label_result1.config(text="Level 2 Pension:" + str(abs(round(level2_pension_increase_by_year, 2))))
        return level2_pension_increase_by_year
    
    except ValueError:
        label_result1.config(text="Please enter valid numbers")

def calculate_expected_pensions_month():
    try:
        level1_pension_month = calculate_level1_pension() / 12
        level2_pension_month = calculate_level2_pension_year() / 12
        
        label_result3.config(text="Level 1 Pension a month:" + str(abs(round(level1_pension_month, 2))))
        label_result4.config(text="Level 2 Pension a month:" + str(abs(round(level2_pension_month, 2))))

        return level1_pension_month, level2_pension_month
    
    except ValueError:
        label_result3.config(text="Please enter valid numbers")
        label_result4.config(text="Please enter valid numbers")

def calculate_left_to_retire():
    try:
        salary, age, years_in_service, accumulation_input, contribution_years_for_pension_level_3 = get_inputs()
        age = float(age)
        retire_main_age = RETIREMENT_AGE
        main_retire_age = retire_main_age - age

        label_result5.config(text="Left to retire:" + str(abs(round(main_retire_age, 2))))
    except ValueError:
        label_result5.config(text="Please enter valid numbers")

def calculate_pension_third_level():
    try:
        salary, age, years_in_service, accumulation_input, contribution_years_for_pension_level_3 = get_inputs()
        accumulation_input = float(accumulation_input)
        contribution_years_for_pension_level_3 = float(contribution_years_for_pension_level_3)
        pension_accumulation = accumulation_input * 12 * contribution_years_for_pension_level_3
        pension_accumulation_inflation = INFLATION_RATE * pension_accumulation * 12
        pension_accumulation_increase = pension_accumulation * LEVEL2_3_NOMINAL_YIELD
        pension_accumulation_by_year = pension_accumulation + pension_accumulation_increase - pension_accumulation_inflation

        label_result6.config(text="Pension level 3:" + str(abs(round(pension_accumulation_by_year, 2))))
        return pension_accumulation_by_year
    
    except ValueError:
        label_result6.config(text="Please enter valid numbers")

def calculate_pension_all():
    try:
        salary, age, years_in_service, accumulation_input, contribution_years_for_pension_level_3 = get_inputs()
        age = float(age)
        level1_pension_increase_by_year = calculate_level1_pension()
        pension_sum_for_all = level1_pension_increase_by_year + calculate_level2_pension_year() + calculate_pension_third_level()
        real_age = age - 15
        calc_age_for_pension = RETIREMENT_AGE - real_age
        calc_whole_pension = calc_age_for_pension * pension_sum_for_all

        label_result7.config(text="Pension all:" + str(abs(round(calc_whole_pension, 2))))
    except ValueError:
        label_result7.config(text="Please enter valid numbers")

root = tk.Tk()
root.title("Pensijas Kalkulators")
root.geometry("600x800")

def calculate():
    calculate_left_to_retire()
    calculate_level1_pension()
    calculate_level2_pension_year()
    calculate_expected_pensions_month()
    calculate_pension_third_level()
    calculate_pension_all()

label_salary = tk.Label(root, text="Salary:")
label_salary.pack()

entry_salary = tk.Entry(root, validate="key")
entry_salary.config(validatecommand=(root.register(validate_salary), "%P"))
entry_salary.pack()

label_service = tk.Label(root, text="contribution:")
label_service.pack()

entry_service = tk.Entry(root, validate="key")
entry_service.config(validatecommand=(root.register(validate_years_in_service), "%P"))
entry_service.pack()

label_age = tk.Label(root, text="Age:")
label_age.pack()

entry_age = tk.Entry(root, validate="key")
entry_age.config(validatecommand=(root.register(validate_age), "%P"))
entry_age.pack()

label_accumulation = tk.Label(root, text="accumulation:")
label_accumulation.pack()

entry_accumulation = tk.Entry(root, validate="key")
entry_accumulation.config(validatecommand=(root.register(validate_accumulation_input), "%P"))
entry_accumulation.pack()

label_contribution = tk.Label(root, text="contribution:")
label_contribution.pack()

entry_contribution = tk.Entry(root, validate="key")
entry_contribution.config(validatecommand=(root.register(validate_contribution_years), "%P"))
entry_contribution.pack()

button_calculate = tk.Button(root, text="Calculate", command=lambda: calculate())
button_calculate.pack()

label_result = tk.Label(root, text="")
label_result.pack()

label_result1 = tk.Label(root, text="")
label_result1.pack()

label_result3 = tk.Label(root, text="")
label_result3.pack()

label_result4 = tk.Label(root, text="")
label_result4.pack()

label_result5 = tk.Label(root, text="")
label_result5.pack()

label_result6 = tk.Label(root, text="")
label_result6.pack()

label_result7 = tk.Label(root, text="")
label_result7.pack()

class Correlation_photo(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.calculate_button = tk.Button(self, text="Pensijas korelācijas attēls", command=self.calculate_pensions)
        self.calculate_button.pack()

    def calculate_pensions(self):
        level1_pension_month, level2_pension_month = calculate_expected_pensions_month()
        years = list(range(2023, 2063))

        level1_pensions = []
        for year in years:
            level1_pensions.append(calculate_level1_pension() * ((1 + LEVEL1_INDEXATION_RATE) ** (year - 2023)))

        level2_pensions = []
        for year in years:
            level2_pensions.append(calculate_level2_pension_year() * ((1 + LEVEL2_3_NOMINAL_YIELD) ** (year - 2023)))

        plt.plot(years, level1_pensions, label='Pirmā līmeņa pensija')
        plt.plot(years, level2_pensions, label='Otrā līmeņa pensija')
        plt.title('Korelācija starp gadiem')
        plt.xlabel('Gads')
        plt.ylabel('Pensijas lielums (eur/gadā)')
        plt.legend()

        plt.savefig('Tavas pensijas korelācija.png')

app = Correlation_photo(master=root)

cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM datasheet")
    rows = cursor.fetchall()
except sqlite3.OperationalError:
    rows = []

data = []

for row in rows:
    data.append({
        'id': row[0],
        'age': row[1],
        'salary': row[2],
        'service': row[3],
        'accumulation': row[4],
        'contribution': row[5]
    })

json_data = json.dumps(data)

with open('api_data.json', 'w') as f:
    f.write(json_data)

root.mainloop()
conn.close()