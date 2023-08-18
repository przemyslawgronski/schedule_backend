from ortools.sat.python import cp_model

def solve_constraints(num_days:int, num_shifts:int, employees=None, constraints=None, days_off=None):

    # print(num_days, num_shifts, employees, constraints, days_off, sep='\n\n\n')

    all_employees = employees if employees else []
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: employee 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_employees:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar(f'shift_n{n}d{d}s{s}')

    # Each shift is assigned to exactly one employee in .
    if '1_prac_na_zmianie' in constraints:
        for d in all_days:
            for s in all_shifts:
                model.Add(sum(shifts[(n, d, s)] for n in all_employees) == 1)

    # Each employee works at most one shift per day.
    if 'max_1_prac_na_dzien' in constraints:
        for n in all_employees:
            for d in all_days:
                model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    # Days off
    # example: days_off_ls=[(1, ['18']), (2, ['27', '28'])]
    # example: days_off_ls = {3: [24], 45: [], 54: [26, 27], 55: []}
    if days_off:
        for emp_id, days_off in days_off.items():
            for day_off in days_off:
                # emp_id - employee number
                # day_off - list of days
                model.Add(sum(shifts[(emp_id, day_off, s)] for s in all_shifts) == 0)

    if 'po_rowno' in  constraints:
        lista_sum = []

        for n in all_employees:
            suma = model.NewIntVar(0,100, "suma")
            model.Add(suma == sum(shifts[(n,d,s)] for d in all_days for s in all_shifts))
            lista_sum.append(suma)

        max_hour = model.NewIntVar(0,100,"max_hour")
        model.AddMaxEquality(max_hour, lista_sum)
        model.Minimize(max_hour)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    for d in all_days:
        result[d] = {}

    if status == cp_model.OPTIMAL:
        for d in all_days:
            for n in all_employees:
                for s in all_shifts:
                    if solver.Value(shifts[(n, d, s)]) == 1:
                        if not n in result[d]: # If there is no employee key in day dict
                            result[d][n] = []
                        result[d][n].append(s)
    
    else:
        result = ""

    return result

if __name__ == '__main__':
    print(solve_constraints(
        num_days=31,
        employees=[3,45,54,55],
        num_shifts=3,
        constraints=['1_prac_na_zmianie', 'max_1_prac_na_dzien', 'po_rowno'],
        days_off = {3: [24], 45: [], 54: [26, 27], 55: []}
    ))



#     30


# 3


# [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]


# ['po_rowno', '1_prac_na_zmianie']


# {2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 15: [], 16: [], 17: [], 18: [], 19: [], 20: [], 21: [], 22: []}