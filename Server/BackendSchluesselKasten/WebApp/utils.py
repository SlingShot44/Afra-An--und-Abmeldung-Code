from importlib.resources import path
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
from API.models import Tour, Account

import os
from django.conf import settings
import csv
from django.core.exceptions import ValidationError

path = os.path.join(settings.BASE_DIR, "print", "print.pdf")

def printPDF():
    generatePDF()
    try:
        os.system("lp %s" % path)   
    except Exception as e:
        print(e)

def generatePDF():
    file = open(path, "w+b")
    list = Tour.objects.filter(back=False).order_by("start").reverse()
    template = get_template("WebApp/pdf.html")
    html = template.render({"list": list, "date": timezone.localdate(timezone.now())})
    pisa_status = pisa.CreatePDF(html, dest=file, link_callback=link_callback)
    file.close()

def link_callback(uri: str,rel):
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL 
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )

    return path

def update(id: str):
    if not Tour.objects.filter(id = id).filter(back=False).exists():
        return
    tour = Tour.objects.filter(id=id).get(back=False)
    tour.back = True
    tour.end = timezone.now()
    tour.save()

def fill_db():
    path = os.path.join(os.path.dirname(__file__),"..","config","mensarfid.csv")
    with open(path, newline="", encoding="utf-8") as f:
        _csv = csv.DictReader(f, delimiter=";")
        for item in _csv:
            name = item[list(item.keys())[0]]
            name = name.split(" ")
            fn = " ".join(name[:-1])
            nn = name[-1]
            acc = Account(uid = item["cardnumber"], first_name = fn, last_name = nn, house = int(item["house"]))
            try:
                acc.full_clean()
                acc.save()
            except ValidationError as e:
                print(e)

def refresh_db():
    Account.objects.all().delete()
    fill_db()