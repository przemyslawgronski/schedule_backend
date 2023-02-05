from rest_framework.serializers import ModelSerializer
from .models import Employee, Group, Shift

# -------- Group Serializers --------

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class GroupSerializerName(ModelSerializer):
    class Meta:
        model = Group
        fields = ['group_name', 'user']

class GroupSerializerShift(ModelSerializer):
    class Meta:
        model = Group
        fields = ['num_of_shifts', 'user']


# -------- Employee Serializers --------

class EmployeeSerializer(ModelSerializer):
    # groups = GroupSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = '__all__' # ['first_name','last_name','groups','user']

class EmployeeSerializerFirstAndLastName(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name','last_name','user']

class EmployeeSerializerLastName(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['last_name','user']

class EmployeeSerializerGroups(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['groups','user']


# -------- Shift Serializers --------

class ShiftSerializer(ModelSerializer):

    class Meta:
        model = Shift
        fields = '__all__'