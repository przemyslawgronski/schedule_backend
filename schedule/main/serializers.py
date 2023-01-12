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




# class EmployeeSerializer(ModelSerializer):
#     groups = GroupSerializer(many = True, read_only = True)
#     group_ids = ListField(
#         child = IntegerField(), write_only = True
#     )

#     class Meta:
#         model = Employee
#         fields = '__all__'
#         extra_fields = ['group_ids']

#     def create(self, validated_data):
#         group_ids = validated_data.pop('group_ids')
#         employee = Employee.objects.create(**validated_data)
#         employee.groups.set(group_ids)
#         return employee

#     def update(self, instance, validated_data):
#         print("update called")
#         group_ids = validated_data.pop('group_ids')
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.groups.set(group_ids)
#         instance.save()
#         return instance





# -------- Shift Serializers --------

class ShiftSerializer(ModelSerializer):

    # employee.groups = GroupSerializer()
    # groups = PrimaryKeyRelatedField(many=True, read_only=True)


    class Meta:
        model = Shift
        fields = '__all__'

    # def to_representation(self, instance):
    #     rep = super(ShiftSerializer, self).to_representation(instance)

    #     print(rep)
    #     # rep['employee_f'] = instance.employee.first_name
    #     # rep['employee_l'] = instance.employee.last_name
    #     return rep