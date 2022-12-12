from django.contrib.auth.decorators import login_required
from .forms import TourSearchForm, TourCreateForm
from django.core.paginator import Paginator
from API.models import Tour, Account
from django.shortcuts import render
from crispy_forms.utils import render_crispy_form
from django.template.context_processors import csrf
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from functools import reduce
from operator import or_
import os
from django.conf import settings
from django.http import FileResponse
from .utils import generatePDF
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from API.json_tools import house_list
from django.views.decorators.cache import cache_control

def make_context(query: QuerySet, searchForm: TourSearchForm, tourForm: TourCreateForm, request: HttpRequest):
    paginator = Paginator(query, 10)
    page = request.GET.get('page',1)
    if int(page) <= paginator.num_pages:
        query = paginator.page(page)
    ff = "Firefox" in request.headers["User-Agent"]
    for item in query:
        item.target = house_list()[int(item.target)]
    return {'list': query, 'form': searchForm, 'tourForm': tourForm, 'ff':ff}

def search(request: HttpRequest, qs: QuerySet, name:str = None) -> tuple[QuerySet, HttpRequest]:  
    name  = name or request.session["name"]
    names = name.split(" ")
    query = qs.filter(reduce(or_,[(Q(owner__first_name__icontains=name)|Q(owner__last_name__icontains=name)) for name in names])).order_by("start").reverse()
    request.session["query"] = "2"
    request.session["name"] = name
    return query, request

@login_required(login_url='/accounts/login')
@cache_control(no_cache=True, private=True)
def aktuell_view(request: HttpRequest) -> HttpResponse:
    tourForm = TourCreateForm(None)
    qs = Tour.objects.all()
    if request.method == "GET":
        query = qs.filter(back=False).order_by("start").reverse()
        context = make_context(query, "", tourForm, request)
        return render(request, "WebApp/Aktuell.html", context)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@login_required(login_url='/accounts/login')
@cache_control(no_cache=True, private=True)
def verlauf_view(request: HttpRequest) -> HttpResponse:
    searchForm = TourSearchForm(request.POST or None)
    tourForm = TourCreateForm(None)
    qs = Tour.objects.all()
    print(qs)
    if request.method == "GET":
        print("get")
        if request.GET.get('page'):
            ind = request.session["query"]
            if ind == "1":
                query = qs.order_by('start').reverse()
            elif ind == "2":
                query, request = search(request, qs)
            context = make_context(
                query, searchForm, tourForm, request)
            return render(request, "WebApp/Verlauf.html", context)
        query = qs.order_by("start").reverse()
        request.session["query"] = "1"
        context = make_context(query, searchForm, tourForm, request)
        return render(request, "WebApp/Verlauf.html", context)
    elif request.method == "POST":
        name = request.POST.get('name')
        if name == '':
            query = qs.order_by("start").reverse()
            request.session["query"] = "1"
        else:
            query, request = search(request, qs, name)
        context = make_context(query, searchForm, tourForm, request)
        return render(request, "WebApp/Verlauf.html", context)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([StaticHTMLRenderer])
def tour_view(request: HttpRequest) -> Response:
    if request.method == "POST":
        form = TourCreateForm(request.POST)
        valid = False
        if form.is_valid():
            valid = request.POST.get("owner",-1)!=-1 and not Tour.objects.filter(owner=Account.objects.get(uid=request.POST["owner"])).filter(back=False).exists()
            if valid:
                form.save()
            form = TourCreateForm(None)
        csrf_context = {}
        csrf_context.update(csrf(request))
        html = render_crispy_form(form, context=csrf_context)
        if not valid:
            return Response(html, status=status.HTTP_400_BAD_REQUEST)
        return Response(html, status= status.HTTP_201_CREATED)

@login_required(login_url='/accounts/login')
def pdf_view(request: HttpRequest) -> FileResponse:
    path = os.path.join(settings.BASE_DIR, "print", "print.pdf")
    generatePDF()
    return FileResponse(open(path, "rb"))