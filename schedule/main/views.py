from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Group
from .serializers import EmployeeSerializer, GroupSerializer
from .utils import *


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def groups(request):

    if request.method == 'GET':
        return get_items_by_item(Group, GroupSerializer, request)

    if request.method == 'POST':
        return create_item(GroupSerializer, request, ["group_name","num_of_shifts"])
        # hide id false by default

@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def group(request, id):

    if request.method == 'GET':
        return get_item(Group, GroupSerializer, request, id)

    if request.method == "PUT":
        return change_item(Group, GroupSerializer, request, id, ["group_name", "num_of_shifts", "hide"])

    if request.method == 'DELETE':
        return delete_item(Group, request, id)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_employees(request, id):

    if request.method == 'GET':
        return get_items_by_item(Employee, EmployeeSerializer, request, **{'groups__id':id})


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def employees(request):

    if request.method == 'GET':
        return get_items_by_item(Employee, EmployeeSerializer, request)

    if request.method == 'POST':
        return create_item(EmployeeSerializer, request, ["first_name", "last_name", "groups"])

@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def employee(request, id):

    if request.method == 'DELETE':
        return delete_item(Employee, request, id)

    if request.method == 'GET':
        return get_item(Employee, EmployeeSerializer, request, id)

    if request.method == "PUT":
        return change_item(Employee, EmployeeSerializer, request, id, ["first_name","last_name","groups", "hide"])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employees_group(request, id):

    if request.method == 'GET':
        return get_items_by_item(Group, GroupSerializer, request, **{'employee__id':id})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def constraints(request):

    if request.method == 'GET':
        return get_constraints()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_solution(request):

    if request.method == "POST":
        return create_shifts(request) # save solution

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def render_solution(request):

    if request.method == "POST":
        return solve_problem(request)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def years_months_with_shifts(request):

    if request.method == "GET":
        return years_and_months_with_shifts(request)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shifts(request, year, month):

    if request.method == 'GET':
        return get_shifts(request, year, month)