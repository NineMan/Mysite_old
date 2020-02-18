from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .models import User, Account
from . import services


def index(request):
	users = User.objects.all().order_by('id')
	limit = 20

	page = request.GET.get('page', 1)
	paginator = Paginator(users, limit)
	paginator.baseurl = '/shop/?page='	#

	try:
		page = paginator.page(page)						# Page
	except EmptyPage:									# Exception as e:
		page = paginator.page(paginator.num_pages)

	return render(request, 'index.html', {
		'list_users' : page.object_list,
		'paginator' : paginator,
		'page' : page,
		})


def user_page(request, pk):
	user = get_object_or_404(User, pk=pk)
	users_accounts = Account.objects.all().filter(user_account=user)

	return render(request, 'user_detail.html', { 
		'user' : user, 
		'users_accounts' : users_accounts,
		})


def account_page(request, pk):
	account = get_object_or_404(Account, pk=pk)
	us_id = Account.objects.get(pk=pk).user_account_id
	user = get_object_or_404(User, pk=us_id)

	return render(request, 'account_detail.html', { 
		'user' : user,
		'account' : account 
		})


def search_user(request):
	not_found = ''
	pk = request.GET.get('pk')
	user = User.objects.get(pk=pk)

	query = request.GET.get('q')
	list_users = User.objects.filter(name=query)

	if query and not list_users.exists():
		not_found = 'Такого пользователя не существует. Уточните поиск.'

	return render(request, 'search_user.html', {
		'user' : user,
		'list_users' : list_users,
		'not_found' : not_found,
		})


def accounts_page(request):
	transfer_user = request.GET.get('tu')			# tu == transfer_user (id)	==	отправитель(id)
	recipient_user = request.GET.get('ru')			# recipient_user (id)		==	получатель (id)
	recipient_account = request.GET.get('ra')		# recipient_account (id)	==	счёт получателя (id)

	user = User.objects.get(pk=transfer_user)
	users_accounts = Account.objects.all().filter(user_account=user)

	return render(request, 'accounts.html', {
		'user' : user,
		'users_accounts' : users_accounts,
		'recipient_user' : recipient_user,
		'recipient_account': recipient_account,
		})


def sum_transfer(request):
	transfer_user = request.GET.get('tu')			# tu == transfer_user (id)	==	отправитель(id)
	transfer_account = request.GET.getlist('ta')	# ta == transfer_account (id) == счет(а) отправителя(id)
	recipient_user = request.GET.get('ru')			# recipient_user (id)		==	получатель (id)
	recipient_account = request.GET.get('ra')		# recipient_account (id)	==	счёт получателя (id)

	user = User.objects.get(pk=transfer_user)

	return render(request, 'sum_transfer.html', {
		'user' : user,
		'transfer_user' : transfer_user,
		'transfer_account' : transfer_account,
		'recipient_user' : recipient_user,
		'recipient_account': recipient_account,
		})


def transfer_detail(request):
	transfer_user_id = request.GET.get('tu')			# tu == transfer_user (id)	==	отправитель(id)
	transfer_accounts_id = request.GET.getlist('ta')	# ta == transfer_account (id) == счет(а) отправителя(id)
	transfer_sum = int(request.GET.get('ts'))			# ts == tansfer_sum == сумма перевода
	recipient_user_id = request.GET.get('ru')			# recipient_user (id)		==	получатель (id)
	recipient_account_id = request.GET.get('ra')		# recipient_account (id)	==	счёт получателя (id)


	user = User.objects.get(pk=transfer_user_id)
	transfer_user = user
	transfer_accounts = []
	for account in transfer_accounts_id:
		transfer_accounts.append(Account.objects.get(pk=account))

	recipient_user = User.objects.get(pk=recipient_user_id)
	recipient_account = Account.objects.get(pk=recipient_account_id)

	return render(request, 'transfer_detail.html', {
		'user' : user,
		'transfer_user_id' : transfer_user_id,
		'transfer_user' : transfer_user,
		'transfer_accounts_id' : transfer_accounts_id,
		'transfer_accounts' : transfer_accounts,
		'transfer_sum' : transfer_sum,
		'recipient_user_id' : recipient_user_id,
		'recipient_user' : recipient_user,
		'recipient_account_id' : recipient_account_id,
		'recipient_account' : recipient_account,
		})


def transfer_calc(request):
	transfer_user_id = request.GET.get('tu')			# tu == transfer_user (id)	==	отправитель(id)
	user = User.objects.get(pk=transfer_user_id)
	transfer_user = user

	transfer_accounts_id = request.GET.getlist('ta')	# ta == transfer_account (id) == счет(а) отправителя(id)
#	print(transfer_accounts_id)
#	print(type(transfer_accounts_id))
	transfer_accounts = []
	for account in transfer_accounts_id:
		transfer_accounts.append(Account.objects.get(pk=account))

#	transfer_accounts = Account.objects.
	
	transfer_sum = int(request.GET.get('ts'))			# ts == tansfer_sum == сумма перевода

	recipient_user_id = request.GET.get('ru')			# recipient_user (id)		==	получатель (id)
	recipient_user = User.objects.get(pk=recipient_user_id)

	recipient_account_id = request.GET.get('ra')		# recipient_account (id)	==	счёт получателя (id)
	recipient_account = Account.objects.get(pk=recipient_account_id)



	new_transfer_accounts = services.sum_accounts(transfer_accounts, transfer_sum)
	print(new_transfer_accounts)


	return render(request, 'transfer_calc.html', {
		'user' : user,
		'test' : new_transfer_accounts,
		'transfer_user' : transfer_user,
		'transfer_accounts' : transfer_accounts,



		'transfer_user' : transfer_user,
		'transfer_accounts_id' : transfer_accounts_id,
		'transfer_sum' : transfer_sum,
		'recipient_user_id' : recipient_user_id,
		'recipient_user' : recipient_user,
		'recipient_account_id' : recipient_account_id,
		'recipient_account' : recipient_account,
		})
