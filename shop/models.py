from django.db import models


class User(models.Model):
	name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=50, null=True)


	class Meta():
		verbose_name = ('Пользователь')
		verbose_name_plural = ('Пользователи')

	def create_dict_of_users_and_accounts(list_users):
	# Для списка (list) пользователей создаем словарь [пользователи: их счета]
		dict_users = {}
		for user in list_users:
			dict_users[user] = user.account_set.all()
		return dict_users

	def __str__(self):
		return self.name



class Account(models.Model):
	user_account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	number = models.IntegerField()
	value = models.DecimalField(max_digits=7, decimal_places=2)
	
	def list_of_accounts(user):
		user_accounts = Account.objects.all().filter(user_account=user)
		return user_accounts

	class Meta():
		verbose_name = ('Счёт')
		verbose_name_plural = ('Счета')

	def __str__(self): 
		return str(self.number)
