import datetime
from rest_framework.response import Response
from .solve_constraints import solve_constraints
from .serializers import ShiftSerializer
from .models import Employee, Shift
from django.db.models.functions import ExtractYear, ExtractMonth
from collections import defaultdict


# --------------- constraints -----------------
    
def solve_problem(request):

    chosen_group = request.user.group_set.get(id=request.data['group_id'])
    constraints = request.user.constraints_set.filter(id=chosen_group.constraints_id)
    constraints_or_empty = [c.name for c in constraints[0].available_constraints.all()] if constraints.exists() else []

    result = solve_constraints(
        num_days  = request.data['num_days'],
        employees = [int(k) for k in request.data['checkedBoxes'].keys()],
        num_shifts = chosen_group.num_of_shifts,
        constraints = constraints_or_empty,
        days_off = { int(k):v for k,v in request.data['checkedBoxes'].items()},
    )
    
    return Response(result)

# TODO: What to do if there are already shifts in the database?
# TODO: Generate download link


def create_shifts(request):

    user = request.user

    # Cancel if there are already shifts in the database for this group at the same day
    # if user.shift_set.filter(
    #     group = user.group_set.get(id=request.data["group_id"]),
    #     date__year = request.data['year'],
    #     date__month = request.data['month']+1, # +1 to convert from 0 to 1 based
    # ).exists():
    #     print("There are already shifts in the database for this group at the same day")


    for day in request.data['solution']:
        for emp_id in request.data['solution'][day]:
            for shift in request.data['solution'][day][emp_id]:
                Shift.objects.create(
                    employee = Employee.objects.get(id=int(emp_id)),
                    date = datetime.date(request.data['year'], request.data['month']+1, int(day)+1), # +1 to convert from 0 to 1 based
                    shift_num = shift,
                    group = user.group_set.get(id=request.data["group_id"]),
                    user = user,
                )

    return Response("Zapisano")


def years_and_months_with_shifts(request, group_id):

    user = request.user

    # <QuerySet [{'year': 2022, 'month': 7}, {'year': 2021, 'month': 7}, ...]
    years_and_months = user.shift_set.filter(group_id=group_id).values(
        year=ExtractYear('date'),
        month=ExtractMonth('date')
        ).distinct().order_by()

    years_and_months_to_send = defaultdict(set)

    for y_m in years_and_months:
        years_and_months_to_send[y_m['year']].add(y_m['month'])

    years_and_months_to_send = {year:sorted(months, reverse=True) for year,months in years_and_months_to_send.items()}

    # {2022: [10, 9, 8, 7, 2], 2021: [7]}
    return Response(years_and_months_to_send)


def get_shifts(request, id, year, month):
    user = request.user
    shifts = user.shift_set.filter(date__year=year, date__month=month, group__id=id)

    return Response(ShiftSerializer(shifts, many=True).data)

def delete_shifts(request, id, year, month):
    user = request.user
    shifts = user.shift_set.filter(date__year=year, date__month=month, group__id=id)
    shifts.delete()
    return Response("Usunięto")

# ------ Generic functions for views -----------

# get multiple items

def get_items_by_item(ObjType, ObjSerializer, request, **kwargs):
    objects = ObjType.objects.filter(user=request.user, **kwargs)
    return Response(ObjSerializer(objects, many=True).data)

def get_items_non_personal(ObjType, ObjSerializer, request):
    '''Every user will see the same objects'''
    objects = ObjType.objects.all()
    return Response(ObjSerializer(objects, many=True).data)

# create_item, get_item, change_item, delete_item

def create_item(ItemSerializer, request, fields):

    data_to_serialize = { field:request.data[field] for field in fields }

    serializer = ItemSerializer(
        data={ **data_to_serialize, 'user': request.user.id }
    )

    if serializer.is_valid():
        item = serializer.save()
        return Response(ItemSerializer(item).data)
        #return Response([serializer.data[field] for field in fields])
    return Response(f"Coś poszło nie tak: {serializer.errors}")


def get_item(ObjectType, ObjectSerializer, request, id):
    item = get_obj(ObjectType, request, id)
    return Response(ObjectSerializer(item).data)


def change_item(ObjectType, ObjectSerializer, request, id, fields):

    item = get_obj(ObjectType, request, id)
    data_to_serialize = { field:request.data[field] for field in fields }

    serializer = ObjectSerializer(
        instance=item,
        data={ **data_to_serialize, 'user': item.user.id }
    )

    if serializer.is_valid():
        serializer.save()
        return Response(ObjectSerializer(item).data)
            
    return Response(f"Coś poszło nie tak: {serializer.errors}")


def delete_item(ObjectType, request, id):
    item = get_obj(ObjectType, request, id)
    
    # Exception handled in exception_handler.py
    item.delete()

    return Response("Usunięto")


def get_obj(ObjectType, request, id):
    '''try to get object by id and chceck for user id compatibility'''

    # Exception handled in exception_handler.py
    item = ObjectType.objects.get(id=id, user=request.user)
    
    return item