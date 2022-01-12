# django
from django.shortcuts import render
# internal
from .models import Board


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})
