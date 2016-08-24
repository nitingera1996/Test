from django.db import models

class UserDetails(models.Model):
	userid=models.AutoField(primary_key=True)
	email=models.EmailField(max_length=100,unique=True,null=True)
	fbId=models.EmailField(max_length=100,unique=True)
	accessToken=models.EmailField(max_length=100,unique=True)
	firstName=models.CharField(max_length=40)
	lastName=models.CharField(max_length=40,null=True)
	gender=models.CharField(max_length=10)
	locale=models.CharField(max_length=10,null=True)
	picLink=models.CharField(max_length=10,null=True)
	fbProfileLink=models.CharField(max_length=100)

	def __unicode__(self):
		return self.fbId