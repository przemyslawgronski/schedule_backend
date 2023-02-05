from rest_framework.serializers import ModelSerializer
from .models import Employee, Group, Shift

# -------- Group Serializers --------

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


# -------- Employee Serializers --------

class EmployeeSerializer(ModelSerializer):
    # groups = GroupSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = '__all__' # ['first_name','last_name','groups','user']


# -------- Shift Serializers --------

class ShiftSerializer(ModelSerializer):

    class Meta:
        model = Shift
        fields = '__all__'