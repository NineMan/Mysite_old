from .models import User, Account

'''
def sum_accounts(transfer_accounts, transfer_sum):
	# accounts = accounts 	# список всех счетов списания
		# сумма списания

	sum = 0
	print('\n\n')
	print(transfer_accounts)
	print(type(transfer_accounts))
	print('\n\n')
	

	for account in transfer_accounts:
		sum += account.value
#		print(account.number)
	

	return sum
'''



def sum_accounts(transfer_accounts, transfer_sum):
	transfer_sum_all = int(100 * transfer_sum)              # задаем сумму которую списывать в копейках


	acc_dict = transfer_accounts                       # задаем словарь счетов и переводим в копейки
	accounts_dict = {}

	for account in acc_dict:
		accounts_dict[account.number] = int(account.value * 100)
#	print('\n\n')
#	print(accounts_dict)
#	print('\n\n')


#	accounts_dict = {                               # задаем словарь счетов и переводим в копейки
#	    'account_1': int(100 * 333.33),
#	    'account_2': int(100 * 333.35),
#	    'account_3': int(100 * 333.33),
#	}




	count_accounts = len(accounts_dict)                         # считаем количество счетов
	transfer_sum_piece = transfer_sum_all // count_accounts     # считаю сумму списания с одного счёта
	transfer_sum_balance = transfer_sum_all % count_accounts    # считаю нераспределённый остаток

	accounts_list_sorted = sorted(accounts_dict.items(), \
	                              key=lambda kv: -kv[1])        # из словаря делаю сортированный список


	accounts_list_sorted_lenght = len(accounts_list_sorted)     # узнаю длину списка



	# С каждого счёта, начиная с самого большого списываем по одной дополнительной копейки из "нераспределённая часть суммы
	# списания". Нужный элемент сортированного списка - последний с которого нужно списать дополнительную копейку,
	# чтобы закончилась "нераспределённая часть суммы списания".
	start = accounts_list_sorted[transfer_sum_balance - 1][1] >= transfer_sum_piece + int(bool(transfer_sum_balance))
	end = accounts_list_sorted[accounts_list_sorted_lenght - 1][1] >= transfer_sum_piece

	if start and end:
	    for i in range(accounts_list_sorted_lenght):
	        if transfer_sum_balance:
	            accounts_dict[accounts_list_sorted[i][0]] -= (transfer_sum_piece + 1)
	            transfer_sum_balance -= 1
	        else:
	            accounts_dict[accounts_list_sorted[i][0]] -= transfer_sum_piece
	else:
	    print('На счетах недостаточно средств.')

	for account in accounts_dict:
	    accounts_dict[account] /= 100


	return accounts_dict
