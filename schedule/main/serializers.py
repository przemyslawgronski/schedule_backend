from rest_framework.serializers import ModelSerializer
from .models import Employee, Group, Shift, Constraints, AvailableConstraints

# There is no need to include user id

# -------- Group Serializers --------

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        #fields = ['id','group_name','num_of_shifts', 'updated', 'hide']

# -------- Employee Serializers --------

class EmployeeSerializer(ModelSerializer):
    # groups = GroupSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = '__all__'
        #fields = ['id','first_name','last_name','groups','updated', 'hide']


# -------- Shift Serializers --------

class ShiftSerializer(ModelSerializer):

    class Meta:
        model = Shift
        fields = '__all__'
        #fields = ['id','employee','group','date','shift_num','updated']


# -------- Constraints Serializers --------

class ConstraintsSerializer(ModelSerializer):

    class Meta:
        model = Constraints
        fields = '__all__'


# -------- AvailableConstraints Serializers --------

class AvailableConstraintsSerializer(ModelSerializer):

    class Meta:
        model = AvailableConstraints
        fields = '__all__'