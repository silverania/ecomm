
from .forms import UserEditForm, ProfileEditForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
import json
from django.core import serializers
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import Group
valuenext = ""
userLoggedIN = None
list_current_user = None
scrollTo = ''


@method_decorator(csrf_exempt, name='dispatch')
class checkUser(View):
    def post(self, request):
        global valuenext, userLoggedIN, list_current_user
        myuser = object()
        userThatLoginIn = object()
        list_json_user_data = json.loads(request.body)
        print("json : "+str(list_json_user_data))
        for key, value in list_json_user_data.items():
            if 'user' in key:
                myuser = value
            if 'password' in key:
                password = value
        if not bool(userLoggedIN):
            print("if userloggedin mi da : " + str(userLoggedIN))
        if not isinstance(myuser, User):
            try:
                myuser = authenticate(username=myuser, password=password)
                print("Verifica ... myuser non è di tipo User , ho proceduto"
                      + "ad authenticazione !! verifico se sta nel gruppo Blog..")
                if myuser.groups.filter(name__in=['BlogAdmin']).exists():
                    print("myuser sta già nel gruppo blog_admin.....")
                else:
                    print("user myuser NON sta nel gruppo blog_admin.....provvedo"
                          + "ad aggiungerlo ....")
                    group = Group.objects.get(name='BlogAdmin')
                    myuser.groups.add(group)
                    print('myuser aggiunto al gruppo blogadmin ')
            except Exception:
                print("Errore nel autenticazione dell user , e/o nella sua assegnazione"
                      + "al gruppo BlogAdmin")
                myuser = "None"
                list_current_user = myuser
        else:
            print(
                "L user era autentticato non c' è stato bisogno di ripetere l autenticaxzione"
                'L user è autenticato . la funzione request.user mi da : '+str(request.user))

        def getUser(user):
            firstName = user.username
            current_user = Profile.objects.filter(first_name=firstName)
            list_current_user = list(current_user)
            list_current_user = serializers.serialize(
                "json", list_current_user)
            return list_current_user
        if isinstance(myuser, User):
            list_current_user = getUser(myuser)
        if isinstance(userLoggedIN, User):
            userThatLoginIn = getUser(userLoggedIN)
        else:
            userThatLoginIn = "None"
        data = json.dumps(
            {
                "userLogged": list_current_user,
                "userLoggedIN": userThatLoginIn,
            })
        print(str(JsonResponse(data, safe=False)))
        response = JsonResponse(
            data, safe=False
        )
        return response

    def get(self, request):
        return HttpResponse("GET")

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get(request)
        elif request.method == 'POST':
            cv = request.body
            print("from dispatch method :"+str(cv))
            return self.post(request, *args, **kwargs)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def getUrlRequest(request):
    urls = request.build_absolute_uri()
    return urls


def user_login(request):
    global te, scrollTo, valuenext, userLoggedIN
    password = ''
    print("entry in view user_login")
    if request.user.is_authenticated:
        print("AUTHENTICATTTTTTTTTTTTT, request.user ="+str(request.user)
              + "userLoggedIN = "+str(userLoggedIN))
        return render(request, "seigiaautenticato.html", {'valuenext': valuenext})
    if request.method == 'POST':
        print("view: user_login , POST method")
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            myuser = authenticate(request,
                                  username=cd['username'],
                                  password=cd['password'])
            if myuser is not None:
                if myuser.is_active:
                    login(request, myuser)
                    userLoggedIN = myuser
                    return HttpResponseRedirect(valuenext)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        if request.method == 'GET':
            if 'blog' in request.get_full_path():
                scrollTo = "#footer"
            if 'next' in request.GET:
                valuenext = request.GET.get('next')+scrollTo
            myuser = None
            breakpoint()
    return render(request, 'registration/login.html', {'form': form,
                  'next': valuenext, 'user': myuser, 'password': password})


@login_required
def home(request):
    return render(request, 'compilare_il_kernel.html')


@login_required
def dashboard(request):
    return render(request, ' user/dashboard.html', {'section': 'dashboard'})


class Logout(View):
    def get(self, request):
        global userLoggedIN
        logout(request)
        userLoggedIN = None
        if 'next' in request.GET:
            breakpoint()
            print("next in request !")
            next = request.GET.get('next')
            template = "registration/logged_out.html"
            # return redirect(next)
            return render(request, "seiuscito.html", {'valuenext': next})
        return render(request, "seiuscito.html", {'valuenext': next})


def user_register(request):
    global valuenext
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.photo = form.cleaned_data.get('photo')
            # myphoto = request.FILES('photo')
            # user.profile.photo = myphoto
            user.profile.first_name = form.cleaned_data.get('username')
            user.save()
            print("USERPROFILEPHOTO"+str(request.FILES))
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # login(request, user)
            if 'blog' in request.path and 'next' in request.GET:
                return redirect('/user/login/blog')
            elif 'blog' in request.path:
                return HttpResponse("<h1>Authenticated on HostMS !</h1>")
            elif 'next' in request.GET:
                return redirect('/user/login')
            else:
                return redirect('/user/login')
    else:
        if 'blog' in request.path and 'next' in request.GET:
            scrollTo = '#footer'
            valuenext = request.GET.get('next')+scrollTo
        elif 'blog' in request.path:
            scrollTo = '#footer'
        elif 'next' in request.GET:
            valuenext = request.GET.get('next')
        form = SignUpForm()
        #print("USERPROFILEPHOTO"+str(myphoto))
    return render(request, 'user/register.html', {'form': form})


@ login_required
def edit(request):
    print("request="+str(request))
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request, 'edit.html', {'user_form': user_form, 'profile_form': profile_form})
