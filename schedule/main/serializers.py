from rest_framework.serializers import ModelSerializer
from .models import Employee, Group, Shift

# There is no need to include user id

# -------- Group Serializers --------

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','group_name','num_of_shifts', 'updated']

# -------- Employee Serializers --------

class EmployeeSerializer(ModelSerializer):
    # groups = GroupSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = ['id','first_name','last_name','groups','updated']


# -------- Shift Serializers --------

class ShiftSerializer(ModelSerializer):

    class Meta:
        model = Shift
        fields = ['id','employee','group','date','shift_num','updated']