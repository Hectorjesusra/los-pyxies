from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
#from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from .forms import CreateUserForm, UpdateUserForm, UpdateProfileForm
from .models import Post

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Su perfil ha sido actualizado!')
            return redirect('/forum/profile')
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'forum/profile.html',context)

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name='forum/posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/forum'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('/forum')
    else:
        form= CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()

                user=form.cleaned_data.get('username')
                messages.success(request,user)

                return redirect('/forum/login')

        context={'form':form}
        return render(request, 'forum/register.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('/forum')
    else:
        if request.method == 'POST':
            username= request.POST.get('username')
            password= request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/forum')

            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'forum/login.html' ,context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('/forum/login')
