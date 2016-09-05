from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import JsonResponse,StreamingHttpResponse
# from neomodel import UniqueProperty

from apis.models import *

import json

@csrf_exempt
def register(request):
	if request.method=='POST':
		try:
			received_json_data=json.loads(request.body)
		except:
			return JsonResponse({'requestStatus':'ERROR','error_message':'No data received'})
		
		if "UserDetails" in received_json_data:
			UserdetailObj=received_json_data['UserDetails']
			print len(UserdetailObj['picLink'])
			if 'fbId' in UserdetailObj and UserdetailObj['fbId']:
				fbId=UserdetailObj['fbId']
				if 'userName' in UserdetailObj and ('firstName' in UserdetailObj['userName']) and UserdetailObj['userName']['firstName']:
					firstName=UserdetailObj['userName']['firstName']
					if 'fbProfileLink' in UserdetailObj and UserdetailObj['fbProfileLink']:
						fbProfileLink=UserdetailObj['fbProfileLink']
						if 'gender' in UserdetailObj and UserdetailObj['gender']:
							if 'accessToken' in UserdetailObj and UserdetailObj['accessToken']:
								accessToken=UserdetailObj['accessToken']
								if 'picLink' in UserdetailObj and UserdetailObj['picLink']:
									picLink=UserdetailObj['picLink']
									if UserdetailObj['gender']!='MALE' and UserdetailObj['gender']!='FEMALE' and UserdetailObj['gender']!='OTHER':
										return JsonResponse({'requestStatus':'ERROR','error_message':'Incorrect gender'})
									else:
										gender=UserdetailObj['gender']
										try:
											user,created=UserDetails.objects.get_or_create(
												fbId=fbId,
												accessToken=accessToken,
													)
										except IntegrityError as e:
											return JsonResponse({'requestStatus':'ERROR','error_message':"Facebook details already used"})
										
										if created:
											user.firstName=firstName
											user.picLink=picLink
											user.fbProfileLink=fbProfileLink
											user.gender=gender
											created_dic={
												'requestStatus':'USER_CREATED',
												'fbId':fbId,
												'accessToken':accessToken,
												'userName':{'firstName':firstName},
												'picLink':picLink,
												'gender':gender,
												'fbProfileLink':fbProfileLink,
												'userId':user.userid
												}
											if 'email' in UserdetailObj and UserdetailObj['email']:
												email=UserdetailObj['email']
												user.email=email
												created_dic['email']=email
											try:
												user.save()
											except IntegrityError as e:
												user.delete()
												return JsonResponse({'requestStatus':'ERROR','error_message':'email already used'})
											if 'locale' in UserdetailObj and UserdetailObj['locale']:
												locale=UserdetailObj['locale']
												user.locale=locale
												created_dic['locale']=locale
											if 'lastName' in UserdetailObj['userName'] and UserdetailObj['userName']['lastName']:
												lastName=UserdetailObj['userName']['lastName']
												user.lastName=lastName
												created_dic['userName']['lastName']=lastName
											try:
												user.save()
												return JsonResponse(created_dic)
											except:
												user.delete()
												return JsonResponse({'requestStatus':'ERROR','error_message':"Internal Error while saving"})
										else:
											altered=False
											altered_dic={'requestStatus':'USER_UPDATED'}
											if 'email' in UserdetailObj and UserdetailObj['email']:
												email=UserdetailObj['email']
												if user.email!=email:
													return JsonResponse({'requestStatus':'ERROR','error_message':"Cannot update email"})
											if 'locale' in UserdetailObj and UserdetailObj['locale']:
												locale=UserdetailObj['locale']
												if user.locale!=locale:
													altered=True
													user.locale=locale
													altered_dic['locale']=locale
											if 'lastName' in UserdetailObj['userName'] and UserdetailObj['userName']['lastName']:
												lastName=UserdetailObj['userName']['lastName']
												if user.lastName!=lastName:
													altered=True
													user.lastName=lastName
													altered_dic['lastName']=lastName
											if user.firstName!=firstName:
													altered=True
													user.firstName=firstName
													altered_dic['firstName']=firstName
											if user.gender!=gender:
													altered=True
													user.gender=gender
													altered_dic['gender']=gender
											if user.fbProfileLink!=fbProfileLink:
													altered=True
													user.fbProfileLink=fbProfileLink
													altered_dic['fbProfileLink']=fbProfileLink
											if user.picLink!=picLink:
													altered=True
													user.picLink=picLink
													altered_dic['picLink']=picLink
											try:
												user.save()
												if altered:
													return JsonResponse(altered_dic)
												else:
													return JsonResponse({'requestStatus':'USER_UNALTERED'})
											except:
												return JsonResponse({'requestStatus':'ERROR','error_message':"Internal Error while saving"})
								else:
									return JsonResponse({'requestStatus':'ERROR','error_message':'picLink missing'})
							else:
								return JsonResponse({'requestStatus':'ERROR','error_message':'accessToken missing'})
						else:
							return JsonResponse({'requestStatus':'ERROR','error_message':'gender missing'})
					else:
						return JsonResponse({'requestStatus':'ERROR','error_message':'fbProfieLink missing'})
				else:
					return JsonResponse({'requestStatus':'ERROR','error_message':'firstName missing'})
			else:
				return JsonResponse({'requestStatus':'ERROR','error_message':'fbid missing'})
		else:
			return JsonResponse({'requestStatus':'ERROR','error_message':'User Details object missing'})
	return JsonResponse({'requestStatus':'ERROR','error_message':'it was a GET request'})

@csrf_exempt
def fetch(request):
	if request.method=='GET':
		fbId=request.GET.get('fbId',None)
		userId=request.GET.get('userId',None)
		accessToken=request.GET.get('accessToken',None)
		email=request.GET.get('email',None)
		user=None
		if fbId or userId or email or accessToken:
			try:
				user=UserDetails.objects.get(email=email)
			except:
				pass
			try:
				user=UserDetails.objects.get(accessToken=accessToken)
			except:
				pass
			try:
				user=UserDetails.objects.get(fbId=fbId)
			except:
				pass
			try:
				user=UserDetails.objects.get(userid=int(userId))
			except:
				pass
			if user:
				found_dic={ 'requestStatus':'USER_DETAILS',
							'userId':user.userid,
					}
				UserDetails_obj={'fbId':user.fbId,
								 'gender':user.gender,
								 'userName':{'firstName':user.firstName},
								 'accessToken':user.accessToken,
								 'fbProfileLink':user.fbProfileLink,
								 'picLink':user.picLink
							}
				if user.email:
					UserDetails_obj['email']=user.email
				if user.locale:
					UserDetails_obj['locale']=user.locale
				if user.lastName:
					UserDetails_obj['userName']['lastName']=user.lastName
				found_dic['UserDetails']=UserDetails_obj
				return JsonResponse(found_dic)
			else:	
				return JsonResponse({'requestStatus':'USER_NOT_FOUND'})
		else:
			return JsonResponse({'requestStatus':'ERROR','error_message':'Neither of the required parameter given'})
	else:
		return JsonResponse({'requestStatus':'ERROR','error_message':'it was a POST request'})

# #for Neo4j

# # counter=100

# @csrf_exempt
# def register_node(request):
# 	if request.method=='POST':
# 		try:
# 			received_json_data=json.loads(request.body)
# 		except:
# 			return JsonResponse({'requestStatus':'ERROR','error_message':'No data received'})
		
# 		if "UserDetails" in received_json_data:
# 			UserdetailObj=received_json_data['UserDetails']
# 			if 'fbId' in UserdetailObj and UserdetailObj['fbId']:
# 				fbId=UserdetailObj['fbId']
# 				if 'userName' in UserdetailObj and ('firstName' in UserdetailObj['userName']) and UserdetailObj['userName']['firstName']:
# 					firstName=UserdetailObj['userName']['firstName']
# 					if 'fbProfileLink' in UserdetailObj and UserdetailObj['fbProfileLink']:
# 						fbProfileLink=UserdetailObj['fbProfileLink']
# 						if 'gender' in UserdetailObj and UserdetailObj['gender']:
# 							if 'accessToken' in UserdetailObj and UserdetailObj['accessToken']:
# 								accessToken=UserdetailObj['accessToken']

# 								if 'picLink' in UserdetailObj and UserdetailObj['picLink']:
# 									picLink=UserdetailObj['picLink']
# 									if UserdetailObj['gender']!='MALE' and UserdetailObj['gender']!='FEMALE' and UserdetailObj['gender']!='OTHER':
# 										return JsonResponse({'requestStatus':'ERROR','error_message':'Incorrect gender'})
# 									else:
# 										gender=UserdetailObj['gender']
# 										try:
# 											user=UserDetailsNode.nodes.get(fbId=fbId,accessToken=accessToken)
# 											altered=False
# 											altered_dic={'requestStatus':'USER_UPDATED'}
# 											if 'email' in UserdetailObj and UserdetailObj['email']:
# 												email=UserdetailObj['email']
# 												# print user.email
# 												if not user.email:
# 													try:
# 														u=UserDetailsNode.nodes.get(email=email)
# 														return JsonResponse({'requestStatus':'ERROR','error_message':'Email already used'})
# 													except:
# 														pass
# 													altered=True
# 													user.email=email
# 													altered_dic['email']=email
# 												else:
# 													if user.email!=email:
# 														return JsonResponse({'requestStatus':'ERROR','error_message':"Cannot update email"})
# 											if 'locale' in UserdetailObj and UserdetailObj['locale']:
# 												locale=UserdetailObj['locale']
# 												if user.locale!=locale:
# 													altered=True
# 													user.locale=locale
# 													altered_dic['locale']=locale
# 											if 'lastName' in UserdetailObj['userName'] and UserdetailObj['userName']['lastName']:
# 												lastName=UserdetailObj['userName']['lastName']
# 												if user.lastName!=lastName:
# 													altered=True
# 													user.lastName=lastName
# 													altered_dic['lastName']=lastName
# 											if user.firstName!=firstName:
# 													altered=True
# 													user.firstName=firstName
# 													altered_dic['firstName']=firstName
# 											if user.gender!=gender:
# 													altered=True
# 													user.gender=gender
# 													altered_dic['gender']=gender
# 											if user.fbProfileLink!=fbProfileLink:
# 													altered=True
# 													user.fbProfileLink=fbProfileLink
# 													altered_dic['fbProfileLink']=fbProfileLink
# 											if user.picLink!=picLink:
# 													altered=True
# 													user.picLink=picLink
# 													altered_dic['picLink']=picLink
# 											try:
# 												user.save()
# 												if altered:
# 													return JsonResponse(altered_dic)
# 												else:
# 													return JsonResponse({'requestStatus':'USER_UNALTERED'})
# 											except:
# 												return JsonResponse({'requestStatus':'ERROR','error_message':'Internal error while saving possibly due to overflow'})
# 										except:
# 											#new one 
# 											try:
# 												user=UserDetailsNode(fbId=fbId,accessToken=accessToken).save()
# 											except UniqueProperty:
# 												return JsonResponse({'requestStatus':'ERROR','error_message':"Facebook detials already used"})
# 											if 'email' in UserdetailObj and UserdetailObj['email']:
# 												email=UserdetailObj['email']
# 												try:
# 													u=UserDetailsNode.nodes.get(email=email)
# 													user.delete()
# 													return JsonResponse({'requestStatus':'ERROR','error_message':'Email already used'})
# 												except:
# 													user.email=email
# 											user.firstName=firstName
# 											user.picLink=picLink
# 											user.fbProfileLink=fbProfileLink
# 											user.gender=gender
# 											created_dic={
# 												'requestStatus':'USER_CREATED',
# 												'fbId':fbId,
# 												'accessToken':accessToken,
# 												'userName':{'firstName':firstName},
# 												'picLink':picLink,
# 												'gender':gender,
# 												'fbProfileLink':fbProfileLink
# 												}
# 											if 'locale' in UserdetailObj and UserdetailObj['locale']:
# 												locale=UserdetailObj['locale']
# 												user.locale=locale
# 												created_dic['locale']=locale
# 											if 'lastName' in UserdetailObj['userName'] and UserdetailObj['userName']['lastName']:
# 												lastName=UserdetailObj['userName']['lastName']
# 												user.lastName=lastName
# 												created_dic['userName']['lastName']=lastName
# 											try:
# 												user.save()
# 												c=Counter.nodes.get(name="counter")
# 												user.userId=c.counter
# 												c.counter=c.counter+1
# 												c.save()
# 												user.save()
# 												created_dic['userId']=user.userId
# 												return JsonResponse(created_dic)
# 											except:
# 												user.delete()
# 												return JsonResponse({'requestStatus':'ERROR','error_message':'Internal Error while saving'})				
# 								else:
# 									return JsonResponse({'requestStatus':'ERROR','error_message':'picLink missing'})
# 							else:
# 								return JsonResponse({'requestStatus':'ERROR','error_message':'accessToken missing'})
# 						else:
# 							return JsonResponse({'requestStatus':'ERROR','error_message':'gender missing'})
# 					else:
# 						return JsonResponse({'requestStatus':'ERROR','error_message':'fbProfieLink missing'})
# 				else:
# 					return JsonResponse({'requestStatus':'ERROR','error_message':'firstName missing'})
# 			else:
# 				return JsonResponse({'requestStatus':'ERROR','error_message':'fbid missing'})
# 		else:
# 			return JsonResponse({'requestStatus':'ERROR','error_message':'User Details object missing'})
# 	return JsonResponse({'requestStatus':'ERROR','error_message':'it was a GET request'})



# @csrf_exempt
# def fetch_node(request):
# 	if request.method=='GET':
# 		fbId=request.GET.get('fbId',None)
# 		userId=request.GET.get('userId',None)
# 		accessToken=request.GET.get('accessToken',None)
# 		email=request.GET.get('email',None)
# 		user=None
# 		if fbId or userId or email or accessToken:
# 			try:
# 				user=UserDetailsNode.nodes.get(email=email)
# 			except:
# 				pass
# 			try:
# 				user=UserDetailsNode.nodes.get(accessToken=accessToken)
# 			except:
# 				pass
# 			try:
# 				user=UserDetailsNode.nodes.get(fbId=fbId)
# 			except:
# 				pass
# 			try:
# 				user=UserDetailsNode.nodes.get(userId=int(userId))
# 			except:
# 				pass
# 			if user:
# 				found_dic={ 'requestStatus':'USER_DETAILS',
# 							'userId':user.userId,
# 					}
# 				UserDetails_obj={'fbId':user.fbId,
# 								 'gender':user.gender,
# 								 'userName':{'firstName':user.firstName},
# 								 'accessToken':user.accessToken,
# 								 'fbProfileLink':user.fbProfileLink,
# 								 'picLink':user.picLink
# 							}
# 				if user.email:
# 					UserDetails_obj['email']=user.email
# 				if user.locale:
# 					UserDetails_obj['locale']=user.locale
# 				if user.lastName:
# 					UserDetails_obj['userName']['lastName']=user.lastName
# 				found_dic['UserDetails']=UserDetails_obj
# 				return JsonResponse(found_dic)
# 			else:	
# 				return JsonResponse({'requestStatus':'USER_NOT_FOUND'})
# 		else:
# 			return JsonResponse({'requestStatus':'ERROR','error_message':'Neither of the required parameter given'})
# 	else:
# 		return JsonResponse({'requestStatus':'ERROR','error_message':'it was a POST request'})