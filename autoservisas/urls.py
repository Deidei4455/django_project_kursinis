from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_n'),
    path('cars', views.get_cars, name='cars_n'),
    path('car/<int:car_id>', views.get_one_car, name='one-car'),
    path('uzsakymai/', views.UzsakymasListView.as_view(), name='uzsakymai'),
    path('uzsakymas/<int:pk>', views.UzsakymasDetailView.as_view(), name='uzsakymas'),
    path('uzsakymai/<str:status_s>', views.order_with_status, name='order-status'),
    path('search/', views.search, name='search_n'),
    path('klientai/', views.KlientasListView.as_view(), name='klientai'),
    path('klientai/<int:klientas_id>', views.get_klientas, name='klientas'),
    path('myorders/', views.OrdersByUserListView.as_view(), name='my-orders'),
    path('register/', views.register_user, name='register'),
    path('profile', views.get_user_profile, name='user-profile'),
    path('profile', views.get_user_profile, name='user-profile'),
    path('myorders/new', views.UzsakymasByUserCreateView.as_view(), name='user-new-order'),
    path('myorders/update<int:pk>', views.UzsakymasByUserUpdateView.as_view(), name='user-update-order'),
    path('myorders/delete<int:pk>', views.UzsakymasByUserDeleteView.as_view(), name='user-delete-order'),

]
