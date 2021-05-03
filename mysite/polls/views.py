from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Song
from .models import playlist_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from youtube_search import YoutubeSearch

# Create your views here.


from .form import CreateUserForm

'''
    this is code for login_page, register_page, hello_page(test)
    able to do the sign in ( sign in is required )
    can`t jump from page to page by changing the url 
'''
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/polls/index/')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('/polls/login')

        context = {'form': form}
        return render(request, 'polls/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/polls/index/')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/polls/index")
            else:
                messages.info(request, 'username or password is incorrect')
        return render(request, 'polls/login.html')

def logoutUser(request):
    logout(request)
    return redirect('/polls/login')


def test(request):
    '''
        this code is for introduce_page(welcome page)
    '''
    return render(request, 'polls/test.html')


'''
    this is code for music
    able to list all the music in songs.html
    can choose which song to play
'''

@login_required(login_url='/polls/login')
def index(request):
    song = Song.objects.all()
    context = {'song': song}
    return render(request, 'polls/index.html', context)

@login_required(login_url='/polls/login')
def songs(request):
    song = Song.objects.all()
    context = {'song': song}
    return render(request, 'polls/songs.html', context)

@login_required(login_url='/polls/login')
def songpost(request, id):
    song = Song.objects.filter(song_id=id).first()
    context = {'song': song}
    return render(request, 'polls/songpost.html', context)

def search(request):
  if request.method == 'POST':

    add_playlist(request)
    return HttpResponse("")
  try:
    search = request.GET.get('search')
    song = YoutubeSearch(search, max_results=10).to_dict()
    song_li = [song[:10:2],song[1:10:2]]
    # print(song_li)
  except:
    return redirect('/')

  return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})




def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])




