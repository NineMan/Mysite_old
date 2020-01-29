from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .models import User, Account



def index(request):
	list_users = User.objects.all().order_by('id')

	return render(request, 'index.html', {'list_users' : list_users})


def user_page(request, pk):
	user_page = get_object_or_404(User, pk=pk)
	accounts = Account.objects.all().filter(user_account=user_page)

	return render(request, 'user_detail.html', { 
		'user_page' : user_page, 
		'accounts' : accounts 
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
#	account = get_object_or_404(Account, pk=pk)
	list_users = User.objects.all().order_by('name')

	query = request.GET.get('q')
#	if query:
	list_users = User.objects.filter(name=query)
	if query and not list_users:
		return render(request, 'search_not_found.html')


	return render(request, 'search_page.html', {'list_users' : list_users})

