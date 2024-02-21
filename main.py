import pandas

GRADE_PAYMENT = {1: 20000, 2: 25000, 3: 30000, 4: 40000, 5: 45000, 6: 50000, 7: 60000,
                 8: 65000, 9: 75000, 10: 80000, 11: 85000, 12: 100000, 13: 110000, 14: 115000, 15: 120000}
POSITION_PAYMENT = {
    "Cleaner": 25000,
    "Security": 29000,
    "Gardener": 15000,
    "Driver": 30000,
    "Cook": 28000,
}
TAX = 5
PART_TIME_DAILY = {1: 2000, 2: 2500, 3: 3000, 4: 4000, 5: 4500, 6: 5000, 7: 0000,
                   8: 6500, 9: 7500, 10: 8000, 11: 8500, 12: 10000, 13: 11000, 14: 11500, 15: 12000}
OVERTIME_PAYMENT = 3000

# TO CALCULATE EARNINGS
#   salary(full time) = grade payment post
#   salary(part time) = days * payment
#   deductions *= grade_payment/100
#   overtime = overtime_hours * overtime_rate
#   earnings = allowances - upfront - deductions + overtime + salary
#   net_salary  = earnings - (tax * earnings)


overtime_file = pandas.read_csv("overtime_records.csv")
salary_file = pandas.read_csv("payroll.csv")
salary = 0
deduction = 0
overtime = 0
upfront = 0
allowances = 0
tax = 0
total_hours = 0
gross_salary = 0
net_salary = 0
net_salary_list = []


def net_salary_calculator(person):
    global salary, deduction, overtime, upfront, \
        allowances, tax, total_hours, net_salary_list, gross_salary, net_salary
    salary = 0
    deduction = 0
    overtime = 0
    upfront = 0
    allowances = 0
    tax = 0
    total_hours = 0
    gross_salary = 0
    net_salary = 0
    # To get salary
    if person.Staff == "Full":
        salary = GRADE_PAYMENT[person.Grade]
    if person.Staff == "Part":
        salary = PART_TIME_DAILY[person.Grade] * person["Number of days"]
    if person.Staff == "Casual":
        salary = POSITION_PAYMENT[person.Position]
# To get allowances
    allowances = person.Allowances
# To get upfront
    upfront = person.Upfront
# To get deduction
    deduction = (person.Deductions/100) * salary
# To get overtime, loop starts
    person_row = overtime_file[overtime_file["Ref Number"] == person["Ref Number"]]
    person_row = person_row.fillna(0)
    for i in range(31):
        total_hours += sum(person_row[f'{i + 1}'])
    overtime = total_hours * OVERTIME_PAYMENT
    gross_salary = salary + allowances - deduction - upfront + overtime
# to get tax
    tax = (TAX/100)*gross_salary
    net_salary = gross_salary - tax
    net_salary_list.append(net_salary)


for n in range(salary_file.shape[0]):
    person = salary_file.loc[n]
    net_salary_calculator(person)

# send out made salary list
net_salary_file = pandas.DataFrame({
    "Ref Number": salary_file["Ref Number"],
    "Names": salary_file.Name,
    "Net Salary": net_salary_list
})
net_salary_file.to_csv("Net Salary File.csv")


choice = input("Do you wish to review any payment?\n")
if choice.lower() == "yes":
    ID = input("Input employee's Reference Number\n")

    loop = True
    while loop:
        if ID in salary_file["Ref Number"].to_list():
            person = salary_file[salary_file["Ref Number"] == ID]
            person = person.loc[sum(person.index)]
            net_salary_calculator(person)
            print(f"Ref Number = {person['Ref Number']}        Name = {person.Name}")
            if person.Staff == "Full":
                print(f"Income = {salary} for Grade {int(person.Grade)}")
            if person.Staff == "Part":
                print(f"Part time Salary of Grade {int(person.Grade)} = {salary}, Days = {int(person['Number of days'])}")
                print(f"Income = Part time Grade Salary * Number of Days\n\t = {salary}")
            if person.Staff == "Casual":
                print(f"Income = {salary} for {person.Position}")
            print(f"Allowances = {allowances}")
            print(f"Overtime = {overtime}, Hours = {int(total_hours)}, Rate = {OVERTIME_PAYMENT} per hour")
            print(f"Upfront = {upfront}")
            print(f"tax = {tax}, at {TAX}%")
            print(f"Deductions = {deduction}, at {person.Deductions}%")
            print(f"Net Salary = Income + Allowances + Overtime - Upfront - Tax - Deductions\n\t= {net_salary}")
            loop = False

        else:
            print("Invalid Reference Number")
            ID = input("Please input reference number or type end to terminate\n")
            if ID == "end":
                loop = False
