from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.home, name="home"),
    path('store/', views.store,  name="store"),
    path('availability/', views.availability, name="availability"),
	path('login/', views.login, name="login"),
	path('register/', views.register, name="register"),
	path('accounts/', include('django.contrib.auth.urls')),
	path('enquire/', views.enquire, name="enquire"),
	path('orders/',views.orders,name="orders"),
	path('admins/',views.admins,name='admins'),
	path('updates/',views.updates,name='updates'),
	path('updates/<str:pk>/',views.updates,name='updates'),
	path('block/',views.block,name='block'),
	path('admn/',views.admn,name='admn'),
	path('free/',views.free,name="free"),
	path('product/',views.product,name="product"),
	path('tag/',views.tag,name="tag"),
	path('info/',views.info,name='info'),
	path('info/<str:pk>/',views.info,name='info'),
]


