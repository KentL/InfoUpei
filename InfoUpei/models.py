from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Role(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=128,blank=False,help_text="Course Name:")
    slug=models.SlugField(unique=True)
    instructor = models.ForeignKey(User,related_name="intructor_courses_set")
    course_description_text=models.TextField(help_text="Course Description:",blank=True)
    course_description_file=models.FileField(upload_to="course_description_files",blank=True,help_text="Course Description File:")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.instructor_name=str(self.instructor)
        self.slug=slugify(self.name)
        super(Course,self).save(*args, **kwargs)


class Rating(models.Model):
    student=models.ForeignKey(User)
    course=models.ForeignKey(Course,null=True)
    rating=models.IntegerField(default=0)

    def __str__(self):
        return self.student+"-"+self.course+"-"+self.rating


class UserProfile(models.Model):
    user=models.OneToOneField(User)
    first_name=models.CharField(max_length=128,blank=False)
    middle_name=models.CharField(max_length=128,blank=True)
    last_name=models.CharField(max_length=128,blank=False)
    website=models.URLField(blank=True)
    picture=models.ImageField(upload_to='profile_images',blank=True)
    birthday=models.DateField(blank=False,default=datetime(1993,11,21))
    role=models.ForeignKey(Role)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        name=self.first_name
        if self.middle_name:
            name += " "+self.middle_name
        name += " "+self.last_name
        return name

class StudentProfile(models.Model):
    student=models.ForeignKey(User)
    registered_courses=models.ManyToManyField(Course,related_name="registered_student")

    def __str__(self):
        return  self.student.username