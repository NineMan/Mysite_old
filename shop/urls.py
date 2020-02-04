from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
#    re_path(r'^user/(?P<pk>\d+)/$', views.user_page, name = 'user_page'),			# старый синтаксис
    path('user/<int:pk>/', views.user_page, name = 'user_page'),    				#  новый синтаксис
    path('accounts/', views.accounts_page, name = 'accounts_page'),
    path('account/<int:pk>', views.account_page, name = 'account_page'),
    path('search/', views.search_user, name = 'search_user'),
]