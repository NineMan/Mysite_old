from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .models import User, Account


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

	print("\n\n")
	print(transfer_user)
	print(recipient_user)
	print(recipient_account)
	print("\n\n")


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
#	transfer_account_ids = request.GET.getlist('ta')	# ta == transfer_account (id) == счет(а) отправителя(id)
	transfer_sum = int(request.GET.get('ts'))			# ts == tansfer_sum == сумма перевода
	print(transfer_sum)
	recipient_user_id = request.GET.get('ru')			# recipient_user (id)		==	получатель (id)
	recipient_account_id = request.GET.get('ra')		# recipient_account (id)	==	счёт получателя (id)


	user = User.objects.get(pk=transfer_user_id)
	transfer_user = user
	recipient_user = User.objects.get(pk=recipient_user_id)
	recipient_account = Account.objects.get(pk=recipient_account_id)

	return render(request, 'transfer_detail.html', {
		'user' : user,
		'transfer_user_id' : transfer_user_id,
		'transfer_sum' : transfer_sum,
		'recipient_user_id' : recipient_user_id,
		'recipient_account_id' : recipient_account_id,
		'transfer_user' : transfer_user,
		'recipient_user' : recipient_user,
		'recipient_account' : recipient_account,
		})


'''
def accounts_page(request):
	pk_list = request.GET.getlist("accounts")
	print('\n\n   pk_list = {}   \n\n'.format(pk_list))
	
	if not pk_list:
		return HttpResponseNotFound("Ни один счёт не выбран")

	accounts = []
	total_value = 0
	for pk in pk_list:
		account = get_object_or_404(Account, pk=pk)			# Выбираю первый отмеченный счёт
		accounts.append(account)							# Собирают list (список) счетов 
		total_value = total_value + account.value 			# Считаю сумму на счетах

	user_id = Account.objects.get(pk=pk).user_account_id	# Получаю id user'a у которого этот аккаунт
	user = get_object_or_404(User, pk=user_id)				# На основе user_id получаю самого user'a

	return render(request, 'account_detail.html', { 
		'user' : user,
		'accounts' : accounts,
		'total_value' : total_value 
		})
'''

