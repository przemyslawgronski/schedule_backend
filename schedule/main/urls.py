from django.urls import path
from .views import *

urlpatterns = [
    path('groups', groups),
    path('groups/<int:id>', group),
    path('groups/<int:id>/employees', group_employees),
    path('employees', employees),
    path('employees/<int:id>', employee),
    path('employees/<int:id>/groups', employees_group),
    path('constraints', constraints),
    path('constraints/<int:id>', constraint),
    path('available-constraints', available_constraints),
    path('save-solution', save_solution),
    path('render-solution', render_solution),
    path('groups/<int:id>/years-months-with-shifts', years_months_with_shifts_by_group),
    path('shifts/<int:id>/<int:year>/<int:month>', shifts),
]