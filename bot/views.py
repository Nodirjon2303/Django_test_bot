from django.core.files.storage import default_storage
import os
import docx
# Create your views here
from django.http import HttpResponse
from django.shortcuts import render
from .models import *

from .forms import File

def read():
    path = default_storage.open(os.path.join('Savolar.docx'))
    print(path)
    doc = docx.Document(path)
    soni = 1
    id = 1
    fayl = []
    for par in doc.paragraphs:
        fayl.append(par.text)
        print(par.text)
        test = Test.objects.get(id=id)
        if soni % 5 == 1:
            if par.text:
                test = Test.objects.create(question=par.text)
                id = test.id
        elif soni % 5 == 2:
            question = Answer.objects.create(test=test, var=par.text)
            test.right = question.id
            test.save()
        else:
            question = Answer.objects.create(test=test, var=par.text)
        soni += 1
    print('succes')


