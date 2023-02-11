from django.db import models
from django.conf import settings


class Group(models.Model):
    group_name = models.CharField(max_length=30)
    num_of_shifts = models.PositiveSmallIntegerField()
    constraints = models.ForeignKey('Constraints', on_delete=models.CASCADE, blank=True, null=True) # one set of constraints can be assigned to multiple groups
    hide = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated']
        unique_together = (('group_name', 'user'),) # Unique name of the group for a given user

    def __str__(self) -> str:
        return self.group_name
    

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    groups = models.ManyToManyField(Group, blank=True) # Many employees - many groups
    updated = models.DateTimeField(auto_now=True)
    hide = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated']

    def __str__(self) -> str:
        return f'{self.first_name}, {self.last_name}'


class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) # one employee can have many shifts
    group = models.ForeignKey(Group, on_delete=models.CASCADE) # one group can be assigned to multiple shifts
    # CASCADE - Remove this field if employee is deleted
    date = models.DateField()
    shift_num = models.PositiveSmallIntegerField()
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated']

    def __str__(self) -> str:
        return f'{self.employee.first_name}, {self.date}, {self.shift_num}'


class AvaibleConstraints(models.Model):
    '''Avaible constraints edited by admin only (superuser)'''
    name = models.CharField(max_length=30)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self) -> str:
        return f'{self.representation}'


class Constraints(models.Model):
    '''Sets of avaible constraints'''
    representation = models.CharField(max_length=30)
    avaible_constraints = models.ManyToManyField(AvaibleConstraints, blank=True) # Many constraints - many avaible constraints
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated']

    def __str__(self) -> str:
        return f'{self.representation}'


# user - users can modify only rows created by them