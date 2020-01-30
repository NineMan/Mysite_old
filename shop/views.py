from django.core.paginator import Paginator, EmptyPage

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .models import User, Account






def index(request):
	users = User.objects.all().order_by('name')
	limit = 20

	page = request.GET.get('page', 1)
	paginator = Paginator(users, limit)
	paginator.baseurl = '/shop/?page='	#

	try:
		page = paginator.page(page)					# Page
	except EmptyPage:						# Exception as e:
		page = paginator.page(paginator.num_pages)

	return render(request, 'index.html', {
		'list_users' : page.object_list,
		'paginator' : paginator,
		'page' : page,
		})


def user_page(request, pk):
	not_found = ''
	user = get_object_or_404(User, pk=pk)
	users_accounts = Account.objects.all().filter(user_account=user)


	query = request.GET.get('q')
	list_found_users = User.objects.all().order_by('name')		# Не правильно фильтрует. Нужно перенести в models
	list_found_users = User.objects.filter(name=query)

	if query and not list_found_users:
		not_found = 'Такого пользователя не существует. Уточните поиск.'

	list_accounts = []

	for users in list_found_users:
		list_accounts.append(users.account_set.all())

	print(list_accounts[0][0], list_accounts[0][1])
	print(list_accounts[1])

	return render(request, 'user_detail.html', { 
		'user' : user, 
		'users_accounts' : users_accounts,

		'list_found_users' : list_found_users,
		'not_found' : not_found
		})












def accounts_page(request):
	pk_list = request.GET.getlist("acc")
	print('\n\n   pk_list = {}   \n\n'.format(pk_list))
	
	if not pk_list:
		print("Не выбран счёт\n\n")
		return HttpResponseNotFound("Счёт не выбран")

	pk = pk_list[0]
	print('\n\n   pk = {}   \n\n'.format(pk))

	accounts = []
	total_value = 0
	for pk in pk_list:
		account = get_object_or_404(Account, pk=pk)			# Выбираю первый отмеченный счёт
		accounts.append(account)							# Собирают list (список) счетов 
		total_value = total_value + account.value 			# Считаю сумму на счетах
	print('\n\n   accounts = {}   \n\n'.format(accounts))



	user_id = Account.objects.get(pk=pk).user_account_id	# Получаю id user'a у которого этот аккаунт
	user = get_object_or_404(User, pk=user_id)				# На основе user_id получаю самого user'a


	return render(request, 'account_detail.html', { 
		'user' : user,
		'accounts' : accounts,
		'total_value' : total_value 
		})


def account_page(request, pk):
	account = get_object_or_404(Account, pk=pk)
	us_id = Account.objects.get(pk=pk).user_account_id
	user = get_object_or_404(User, pk=us_id)

	return render(request, 'account_detail.html', { 
		'user' : user,
		'account' : account 
		})




#----------------------------------

def search_page(request):
	not_found = ''
	query = request.GET.get('q')
	list_users = User.objects.all().order_by('name')
	list_users = User.objects.filter(name=query)

	if query and not list_users:
		not_found = 'Такого пользователя не существует. Уточните поиск.'

	return render(request, 'search_page.html', {
		'list_users' : list_users,
		'not_found' : not_found
		})

