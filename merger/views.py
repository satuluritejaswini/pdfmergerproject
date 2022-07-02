from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse

from .forms import PDF
from pdfrw import PdfReader, PdfWriter
import os
from django.conf import settings
import shortuuid
from . models import myuploadfile

# Create your views here.
def handle_uploaded_file(f, id):
    with open("media/" + id, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def index(request):
    if request.method == "POST":
        pdf = PDF(request.POST, request.FILES)
        
        files = request.FILES.getlist('file')
              
        i =[]
        for f in files:
            id = shortuuid.uuid() + ".pdf"
            handle_uploaded_file(f ,id)
            i.append(id)
        output = shortuuid.uuid() + ".pdf"
        out = merger(i, output)
        i.clear()
        return FileResponse(open( "media/"+output,'rb') ,as_attachment=True)
            
    else:
        pdf = PDF()
        out = ""
        return render(request, "merger/index.html", {"form": pdf, "out": out})

def merger(inputs, output):
    o = open("media/" + output, "wb+")
    writer = PdfWriter()
    for inpfn in inputs:
        writer.addpages(PdfReader("media/" + inpfn).pages)
    writer.write(o.name)
    o.close()
    return o
    