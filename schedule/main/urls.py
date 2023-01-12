from django.urls import path
from .views import employees_group, group_employees, groups, group, employees, employee, constraints, save_solution, render_solution, years_months_with_shifts, shifts

urlpatterns = [
    path('groups', groups),
    path('groups/<int:id>', group),
    path('groups/<int:id>/employees', group_employees),
    path('employees', employees),
    path('employees/<int:id>', employee),
    path('employees/<int:id>/groups', employees_group),
    path('constraints', constraints),
    path('save-solution', save_solution),
    path('render-solution', render_solution),
    path('years-months-with-shifts', years_months_with_shifts),
    path('shifts/<int:year>/<int:month>', shifts),
]