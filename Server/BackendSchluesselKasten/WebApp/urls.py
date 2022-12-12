from django.urls import path, reverse
from .views import aktuell_view, verlauf_view, tour_view, pdf_view
from django.shortcuts import redirect

app_name = 'WebApp'

urlpatterns = [
    path("", lambda request: redirect(reverse("WebApp:aktuell"))),
    path("tours/", tour_view, name='create'),
    path("aktuell/", aktuell_view, name="aktuell"),
    path("verlauf/", verlauf_view, name="verlauf"),
    path("pdf/", pdf_view, name="pdf"),
]
