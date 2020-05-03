from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Events(models.Model):
    title = models.CharField(max_length=100)
    date_from = models.DateField(null=True)
    date_to = models.DateField(null=True)
    t1 = models.TimeField(null=True)
    t2 = models.TimeField(null=True)
    pic = models.FileField(null=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    course_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.course_name


class College(models.Model):
    college_name = models.CharField(max_length=100, null=True)
    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.college_name


class Notices(models.Model):
    notice = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)
    pic = models.FileField(null=True)

    def __str__(self):
        return self.notice


class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    f_name = models.CharField(max_length=100, null=True)
    l_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    ph_no = models.PositiveIntegerField(default=999999999999)
    collegeid = models.CharField(max_length=100, null=True)
    level = models.IntegerField(default=0)
    start_year = models.CharField(max_length=4, null=True)
    end_year = models.CharField(max_length=4, null=True)
    birth_date = models.DateField(max_length=10, null=True)
    gender = models.CharField(max_length=10, null=True)
    dp = models.FileField(null=True)
    bio = models.CharField(max_length=100, null=True)
    score = models.CharField(max_length=20, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username + ' -- ' + self.email
