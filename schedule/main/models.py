from django.db import models
from django.conf import settings

 # Grupy nie są obowiązkowe, ale bez nich się nie utworzy zmian.
class Group(models.Model):
    group_name = models.CharField(max_length=30)
    num_of_shifts = models.PositiveSmallIntegerField()
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # on_delete=models.CASCADE Removes this field if user is deleted

    class Meta:
        ordering = ['-updated']
        unique_together = (('group_name', 'user'),) # Unique name of the group for a given user

    def __str__(self) -> str:
        return self.group_name
    

class Employee(models.Model):
    # TODO: When employee is deleted and shifts exists then change the name of the employee to "deleted"
    # If shifts connected to this employee doesn't exists then delete shifts
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    groups = models.ManyToManyField(Group, blank=True) # Many employees - many groups
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated']

    def __str__(self) -> str:
        return f'{self.first_name}, {self.last_name}'

class Shift(models.Model):
    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL) # one employee can have many shifts
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL) # one group can be assigned to multiple shifts
    # SET_NULL - user knows that shift was assigned to a group or employee that doesn't exist anymore
    date = models.DateField()
    shift_num = models.PositiveSmallIntegerField()
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated']

    def __str__(self) -> str:
        return f'{self.employee.first_name}, {self.date}, {self.shift_num}'

# user - users can modify only rows created by them