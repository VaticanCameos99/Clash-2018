from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import validate_email
import datetime



class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	score = models.IntegerField(default = 0)
	skip_count = models.IntegerField(default = 2)
	question_skip_count = models.IntegerField(default = 0)
	perception_present = models.IntegerField(default = 2)
	incr = 	models.IntegerField(default = 4, null = True)
	decr = models.IntegerField(default = 2, null = True)
	perception_active = models.IntegerField(default = 0)	
	perception_question_count =  models.IntegerField(default = 3)
	timer = models.IntegerField(default = 0)
	email_1 = models.EmailField(max_length = 20, validators = [validate_email], default = "player_1@gmail.com", editable = True)
	email_2 = models.EmailField(max_length = 20 , validators = [validate_email], default = "player_2@gmail.com", editable = True)
	name_1 = models.CharField(max_length = 20, default = "player_1", editable = True)
	name_2 = models.CharField(max_length = 20 ,default = "player_2", editable = True)
	number_1 = models.IntegerField(default = 0 , editable = True)
	number_2 = models.IntegerField(default = 0 , editable = True)
	level =  models.IntegerField(default = 0, editable = True)
	number_of_questions = models.IntegerField(default = 0)
	correct_answer = models.IntegerField(default = 0)
	ad_pass = models.CharField(max_length = 20,default = "abcd")
	add_time = models.IntegerField(default = 0)
	year =  models.IntegerField(default = 2, editable = True)

	def __str__(self):
		return self.user.username

def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance']) #what are kwargs? also, this creates an entry in profile and sets values to default

post_save.connect(create_profile, sender=User) 

class Question_list(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question_list = models.IntegerField(default = 0)
	answer =  models.IntegerField(default = 0, editable = True)
	

def create_list(sender, **kwargs):
	if kwargs['created']:
		ques = Question_list.objects.create(user=kwargs['instance'])


post_save.connect(create_list, sender=User) 

class MCQ(models.Model):
	question = models.TextField(max_length=150, default=' ')
	answer = models.IntegerField(default=' ')
	A = models.TextField(max_length=150, default=' ')
	B = models.TextField(max_length=150, default=' ')
	C = models.TextField(max_length=150, default=' ')
	D = models.TextField(max_length=150, default=' ')
	level = models.IntegerField(default=1)

