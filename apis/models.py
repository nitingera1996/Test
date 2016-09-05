from django.db import models
# from neomodel import StructuredNode, StringProperty, IntegerProperty

class UserDetails(models.Model):
	userid=models.AutoField(primary_key=True)
	email=models.EmailField(max_length=100,unique=True,null=True)
	fbId=models.EmailField(max_length=100,unique=True)
	accessToken=models.EmailField(max_length=100,unique=True)
	firstName=models.CharField(max_length=40)
	lastName=models.CharField(max_length=40,null=True)
	gender=models.CharField(max_length=10)
	locale=models.CharField(max_length=10,null=True)
	picLink=models.CharField(max_length=100,null=True)
	fbProfileLink=models.CharField(max_length=100)

	def __unicode__(self):
		return self.fbId

# class UserDetailsNode(StructuredNode):
# 	print "Class for User Nodes"
	
# 	userId=IntegerProperty(index=True)
# 	email=StringProperty(required = False)
# 	fbId=StringProperty(unique_index=True,required=True)
# 	accessToken=StringProperty(unique_index=True,required=True)
# 	firstName=StringProperty()
# 	lastName=StringProperty()
# 	gender=StringProperty()
# 	locale=StringProperty()
# 	fbProfileLink=StringProperty()
# 	picLink=StringProperty()

# class Counter(StructuredNode):

# 	counter=IntegerProperty()
# 	name=StringProperty(default="counter")