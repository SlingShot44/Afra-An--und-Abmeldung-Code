from django.urls import path, reverse_lazy
from django.contrib.auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='accounts/login.html'),
         name='login_url'),
    path('logout/', views.LogoutView.as_view(template_name='accounts/logout.html',
                                             next_page=reverse_lazy('WebApp:aktuell')), name='logout_url')
]
