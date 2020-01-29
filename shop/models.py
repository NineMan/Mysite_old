from django.db import models


class User(models.Model):
	name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=50, null=True)


	class Meta():
		verbose_name = ('Пользователь')
		verbose_name_plural = ('Пользователи')

	def __str__(self):
		return self.name



class Account(models.Model):
	user_account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	number = models.IntegerField()
	value = models.DecimalField(max_digits=7, decimal_places=2)

	class Meta():
		verbose_name = ('Счёт')
		verbose_name_plural = ('Счета')

	def __str__(self): 
		return str(self.number)

"""
	def get_url(self):
		return "//{}".format(self.id)

""
    def get_url(self):
        return "/question/{}/".format(self.id)
"""	
