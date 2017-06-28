from django.shortcuts import render

def letsencrypt_verification(request):
    return HttpResponse("Q5SduN6E7TdVdOf-5QctkLAUKfMpBcOGWU9uoe4PGrQ.XL-z7MVJQ86Sm96eh66a1JG9NoLw9X1CW9OVBdHzK7E")

def index(request):
    return render(request, 'index.html')
