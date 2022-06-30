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
    with open(id, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def index(request):
    if request.method == "POST":
        pdf = PDF(request.POST, request.FILES)
        
        files = request.FILES.getlist('file')
              
        i =[]
        for f in files:
            print("Hello")
            id = shortuuid.uuid() + ".pdf"
            handle_uploaded_file(f ,id)
            i.append(id)
        output = shortuuid.uuid() + ".pdf"
        print(i)
        out = merger(i, output)
        
        return FileResponse(open(output,'rb'),as_attachment=True)
            
    else:
        pdf = PDF()
        out = ""
        return render(request, "merger/index.html", {"form": pdf, "out": out})

def merger(inputs, output):
    o = open(output, "wb+")
    writer = PdfWriter()
    for inpfn in inputs:
        writer.addpages(PdfReader(inpfn).pages)
    writer.write(o.name)
    o.close()
    return o
    