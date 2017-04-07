from django.shortcuts import render

def page_not_found(request):
    return render(request, '404.html', status_code=404)

def server_error(request):
    return render(request, '500.html', status_code=500)

def permission_denied(request):
    return render(request, '403.html', status_code=403)

def bad_request(request):
    return render(request, '400.html', status_code=400)
