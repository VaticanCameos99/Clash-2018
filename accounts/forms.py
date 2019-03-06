from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationFrom(UserCreationForm):
	phone_number = forms.IntegerField(required = True)
	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'phone_number',
			'password1',
			'password2',
			)

	def save(self, commit = True):
		user = super(RegistrationFrom, self).save(commit = False)
		user.phone_number = self.cleaned_data['phone_number']


		if commit:
			user.save()

		return user





