from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from django.db.models import Q
from .forms import RoomForm 
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
# rooms = [
#     {'id':1, 'login':'snagat'},
#     {'id':2, 'login':'strng1'},
#     {'id':3, 'login':'okcava'},
# ]

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    try:
        user = User.objects.get(username= username)
    except:
        messages.error(request,"User doesnt exist")
        
    context = {}
    return(render(request, 'firstapp/register.html', context))

def home(response):
    q = response.GET.get('q') if response.GET.get('q') != None else ''
    query = Q(topic__name__icontains = q) | Q(name__icontains = q) | Q(descption__icontains = q)
    rooms = Room.objects.filter(query)
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 
               'topics' :topics,
               'room_count' : room_count,
               
    }
    return render(response, 'firstapp/home.html', context)

def room(response, pk):
    room = Room.objects.get(id=pk)
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    context = {'room':room}    
    return render(response, 'firstapp/room.html', context)

def create_view(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
                
    context = {'form': form}
    return render(request, 'firstapp/room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance= room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'firstapp/room_form.html',context)
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'firstapp/delete.html', context)
    
