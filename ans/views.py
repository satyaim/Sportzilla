from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect, JsonResponse
from .models import CustomUser, Question
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.views.generic import View
from django.views import generic
from ans.forms import QSForm
from django.db import IntegrityError
from django.contrib.auth.models import User
import json
from django.core import serializers
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()

from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import re


def main(request):
	if (request.user.is_authenticated()):
		leaderboard = User.objects.order_by('score').reverse()
		user=request.user
		email=user.email
		tail = email.split('@')[1]
		if not re.match(tail, 'pilani.bits-pilani.ac.in'):
			logout(request)
			return HttpResponseRedirect('https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://127.0.0.1:8000')
		else:
			return render(request,'index.html',{'user':user.username,'score':user.score,'rank':user.rank,'leaderboard':leaderboard})
	else:
		return render(request,'front.html')

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://127.0.0.1:8000')
	



def answer(request, number):
	if request.user.is_authenticated():
		user = request.user

		if number=='1':
			product=Question.objects.get(question_type='football',question_no=user.question_no1)
			qsno=user.question_no1
			no=1
		elif number=='2':
			product=Question.objects.get(question_type='cricket',question_no=user.question_no2)
			qsno=user.question_no2
			no=2
		elif number=='3':
			product=Question.objects.get(question_type='miscellaneous',question_no=user.question_no3)
			qsno=user.question_no3
			no=3
		elif number=='4':
			product=Question.objects.get(question_type='track&field',question_no=user.question_no4)
			qsno=user.question_no
			no=4
		elif number=='5':
			product=Question.objects.get(question_type='extras',question_no=user.question_no5)
			qsno=user.question_no5
			no=5
		
		user.score+=1
		answerof = request.POST.get("answerof", "Guest (or whatever)")


		if answerof == product.solution:
			list1 = list(user.answers_given)
			list1[6*(number-1) +qsno] = '1'
			user.answers_given = ''.join(list1)
			if number=='1':
				user.question_no1+=1
			elif number=='2':
				user.question_no2+=1
			elif number=='3':
				user.question_no3+=1
			elif number=='4':
				user.question_no4+=1
			elif number=='5':
				user.question_no5+=1
			user.save()
			error = False
		else:
			list1 = list(user.answers_given)
			list1[6*(no-1)+qsno] = '3'
			user.answers_given = ''.join(list1)
			user.save()
			return HttpResponseRedirect('/accounts/profile/%s/' % number)

		user.score = 100 *user.answers_given.count('1')-25*user.answers_given.count('2')
		
		leaderboard = User.objects.order_by('score').reverse()
		i = 0

		for player in leaderboard:
			if user.score == player.score:
				user.rank = i + 1
				user.save()
			else:
				i += 1

		user.save()
		return HttpResponseRedirect('/accounts/profile/%s/' % number, {'error': error,})
	else:
		return HttpResponseRedirect('/')




def detail(request, number):
	if request.user.is_authenticated():
		error = False
		u = request.user

		if number=='1':
			product=Question.objects.get(question_type="football",question_no=u.question_no1)
			qsno=u.question_no1
			no=1
			left=5
		elif number=='2':
			product=Question.objects.get(question_type="cricket",question_no=u.question_no2)
			qsno=u.question_no2
			no=2
			left=5
		elif number=='3':
			product=Question.objects.get(question_type="miscellaneous",question_no=u.question_no3)
			qsno=u.question_no3
			no=3
			left=5
		elif number=='4':
			product=Question.objects.get(question_type="track&field",question_no=u.question_no4)
			qsno=u.question_no
			no=4
			left=5
		elif number=='5':
			product=Question.objects.get(question_type="extras",question_no=u.question_no5)
			qsno=u.question_no5
			no=5
			left=5
		s = u.answers_given.count('2')
		u.save()
		qsleft=left-product.question_no
		resp={'score':u.score,'hint':product.question,'skip':s,'djangoNoofQuestionsLeft':qsleft,'qsno':qsno}
		
		return JsonResponse(resp)
	else:
		return HttpResponseRedirect('/')



def skip(request, number):
	if request.user.is_authenticated():
		u=request.user
		if number=='1':
			product=Question.objects.get(question_type='football',question_no=u.question_no1)
			qsno=u.question_no1
			no=1
		elif number=='2':
			product=Question.objects.get(question_type='cricket',question_no=u.question_no2)
			qsno=u.question_no2
			no=2
		elif number=='3':
			product=Question.objects.get(question_type='miscellaneous',question_no=u.question_no3)
			qsno=u.question_no3
			no=3
		elif number=='4':
			product=Question.objects.get(question_type='track&field',question_no=u.question_no4)
			qsno=u.question_no
			no=4
		elif number=='5':
			product=Question.objects.get(question_type='extras',question_no=u.question_no5)
			qsno=u.question_no5
			no=5
		
		s = u.answers_given.count('2')

		if s < 3:
			list1 = list(u.answers_given)
			list1[6*(no-1)+qsno] = '2'
			u.answers_given = ''.join(list1)
			if number=='1':
				u.question_no1+=1
			elif number=='2':
				u.question_no2+=1
			elif number=='3':
				u.question_no3+=1
			elif number=='4':
				u.question_no4+=1
			elif number=='5':
				u.question_no5+=1
			u.save()
			c = u.answers_given.count('1')
			s = u.answers_given.count('2')
			u.score = (c * 100) - (s * 25)

			leaderboard = User.objects.order_by('score').reverse()
			i = 0

			for player in leaderboard:
				if u.score == player.score:
					u.rank = i + 1
					u.save()
				else:
					i += 1

			u.save()
			return HttpResponseRedirect('/accounts/profile/%s/' % number)

		else:
			return HttpResponseRedirect('/accounts/profile/%s/' % number)
	else:
		return HttpResponseRedirect('/')




def leave(request, number):
	if request.user.is_authenticated():
		u = request.user
		if number=='1':
			product=Question.objects.get(question_type='football',question_no=u.question_no1)
			qsno=u.question_no1
			no=1
		elif number=='2':
			product=Question.objects.get(question_type='cricket',question_no=u.question_no2)
			qsno=u.question_no2
			no=2
		elif number=='3':
			product=Question.objects.get(question_type='miscellaneous',question_no=u.question_no3)
			qsno=u.question_no3
			no=3
		elif number=='4':
			product=Question.objects.get(question_type='track&field',question_no=u.question_no4)
			qsno=u.question_no
			no=4
		elif number=='5':
			product=Question.objects.get(question_type='extras',question_no=u.question_no5)
			qsno=u.question_no5
			no=5
		u = request.user
		u.score-=50
		leaderboard = User.objects.order_by('score').reverse()
		i = 0

		for player in leaderboard:
			if u.score == player.score:
				u.rank = i + 1
				u.save()
			else:
				i += 1
		u.save()
		resp={'score':u.score}
		
		return HttpResponse(json.dumps(resp),content_type='application/json')
	else:
		return HttpResponseRedirect('/')




def leaderboard(request):
	if request.user.is_authenticated():
		leaderboard = User.objects.order_by('score').reverse()
		
		resp={'leaderboard':leaderboard}
		
		return HttpResponse(json.dumps(resp),content_type='application/json')
	else:
		return HttpResponseRedirect('/')