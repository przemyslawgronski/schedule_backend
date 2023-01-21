from django.db import models
from django.conf import settings
# stare: group_name = models.CharField(max_length=30, unique=True, null=True, blank=True)

class Group(models.Model):
    # TODO: Grupy powinny być obowiązkowe. "Nieprzypisani" grupa powinna być tworzona automatycznie
    # przy tworzeniu konta nowego użytkownika
    # TODO: zrobić unikalną nazwę grupy ale dla jednego użytkownika a nie dla wszystkich

    group_name = models.CharField(max_length=30)

    num_of_shifts = models.PositiveSmallIntegerField()
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # on_delete=models.CASCADE Removes this field if user is deleted

    class Meta:
        ordering = ['-updated']

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
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT) # one employee can have many shifts
    group = models.ForeignKey(Group, on_delete=models.PROTECT) # one group can be assigned to multiple shifts
    date = models.DateField()
    shift_num = models.PositiveSmallIntegerField()
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated']

    def __str__(self) -> str:
        return f'{self.employee.first_name}, {self.date}, {self.shift_num}'

# user - users can modify only rows created by them