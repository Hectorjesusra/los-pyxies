from django.shortcuts import render

# Create your views here.
def molemule(request):
    return render(request, 'lab/apps/molemule.html')

def acidos_nucleicos(request):
    return render(request, 'lab/apps/acidos.html')

def pyteins(request):
    return render(request, 'lab/apps/pyteins.html')
