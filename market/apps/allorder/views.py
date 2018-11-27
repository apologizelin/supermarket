from django.shortcuts import render


def allorder(request):
    return render(request, "allorder/allorder.html")
