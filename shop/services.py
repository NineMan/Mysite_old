from .models import User, Account


def sum_accounts(accounts):
	# accounts = accounts 	# список всех счетов списания
		# сумма списания

	sum = 0
	for account in accounts:
		sum += account.value
	

	return sum
