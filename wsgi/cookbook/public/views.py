from django.shortcuts import render

def letsencrypt_verification(request):
    return HttpResponse("Ue5gFdAxr7B5JiMqbvqz5wLCwWwW6BSBK9z2P1WRW_Q.XL-z7MVJQ86Sm96eh66a1JG9NoLw9X1CW9OVBdHzK7E")

def index(request):
    return render(request, 'index.html')
