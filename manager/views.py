from django.shortcuts import render


# Create your views here.
def timekeeping(request):
    return render(request, "timekeeping.html")


def worksheet(request):
    return render(request, "worksheet.html")
