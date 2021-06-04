from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.db.models.fields import CharField

class Department(models.Model):
	name = models.CharField(max_length=200)
	image = models.ImageField(null=True, blank=True)

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

	class Meta:
		verbose_name_plural = "Departments"

	def __str__(self):
		return self.name

class Stream(models.Model):
	category = (("Computer Stream", "Computer Stream"), 
				("Communication Stream", "Communication Stream"),
				("Control Stream", "Control Stream"),
				("Power Stream", "Power Stream"))
	stream = models.CharField(max_length=200, choices=category)
	class Meta:
		verbose_name_plural = "Streams"

	def __str__(self):
		return self.stream

class SchoolYear(models.Model):
	category = ((1, 1),  (2, 2), (3, 3) , (4, 4), (5, 5))
	year = models.IntegerField(max_length=30, choices=category)
	name = models.CharField(max_length=30, default=" ")
	image = models.ImageField(null=True, blank=True)
	stream = models.ForeignKey(Stream, on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		verbose_name_plural = "SchoolYear"
    
	def __str__(self):
		return str(self.year)
	
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url



class StudentProfile(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
	stream = models.ForeignKey(Stream, on_delete=models.CASCADE, null=True, blank=True)
	profile_image = models.ImageField(null=True, blank=True)
	
	def imageURL(self):
		try:
			url = self.profile_image.url
		except:
			url = ''
		return url

	class Meta:
		verbose_name_plural = "Students Profile"

	def __str__(self):
		return self.name



class Project(models.Model):
	project_title = models.CharField(max_length=200, primary_key=True)
	abstract = models.TextField()

	published_on = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(StudentProfile, null=True, on_delete=models.CASCADE)

	image = models.ImageField(upload_to='project/', null=True, blank=True)
	source_pdf = models.FileField(upload_to='pdf', null=True)

	class Meta:
		verbose_name_plural = "Project"

	def __str__(self):
		return self.project_title

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	
	@property
	def pdfURL(self):
		try:
			url = self.source_pdf.url
		except:
			url = ''
		return url


class Comment(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	project = models.ForeignKey(Project, related_name="comments", on_delete=models.CASCADE)
	body = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return '%s - %s'%(self.project.project_title)
