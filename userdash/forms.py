from django import forms
from acp.models import *
from django.contrib.auth.models import User

class MailUserForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(MailUserForm, self).__init__(*args, **kwargs)

	class Meta:
		model = MailUser
		fields = ('username', 'domain', 'password', 'quota', 'active')

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name' ,'email')

class MailDomainForm(forms.ModelForm):
	class Meta:
		model = MailDomain
		fields = ('domain', 'notes')

class DomainNotesEditForm(forms.ModelForm):
	class Meta:
		model = MailDomain
		fields = ('notes',)

#class ChangePasswordForm