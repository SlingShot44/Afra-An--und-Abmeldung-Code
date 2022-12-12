from django.urls import path
from .views import function_view, tour_list, option_view, print_view
from rest_framework.authtoken import views

urlpatterns = [
    path("", tour_list),
    path("<int:uid>/", function_view),
    path('get-Token/', views.obtain_auth_token),
    path('options/', option_view),
    # path('print/', print_view)
]
