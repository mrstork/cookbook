from django.shortcuts import render

def teapot(request):
    return render(request, '418.html', status=418)
