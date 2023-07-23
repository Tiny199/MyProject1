from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post,Category,Profile,Comment
from .form import PostModel,EditPost,LoginForm,SignUpForm,EditProfilForm,PassChangedForm,ProfilePageForm,AddCommentForm
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.views import PasswordChangeView



#def LikeViewPost(request, pk):
#    post = get_object_or_404(Post, id=request.POST.get("post_id"))
#    liked = False
#    if post.likes.filter(id=request.user.id).exists():
#        post.likes.remove(request.user)
#        liked = False
#    else:
#        post.likes.add(request.user)
#        liked = True
#    return HttpResponseRedirect(reverse('article-details',args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name = 'home/home1.html'
    ordering = ['-post_date']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView,self).get_context_data(*args, **kwargs)
        context['cat_menu']=cat_menu

        return context





def Categoryview(request,cats):
    category_posts = Post.objects.filter(category=cats)
    return render(request,'blog/category.html',{'cats':cats.title(),'category_posts':category_posts})

class ArticleView(DetailView):
    model = Post
    template_name = 'home/article_detail.html'
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleView,self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked= True
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article-details', args=[str(pk)]))

class AddPost(CreateView):
    model = Post
    form_class = PostModel
    template_name = 'home/add_post.html'
    #fields = '__all__'

class AddCategory(CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = '__all__'

class EditPost(UpdateView):
    model = Post
    form_class = EditPost
    template_name= 'blog/post_form.html'
    #fields = '__all__'

class DeletePost(DeleteView):
    model = Post
    template_name = 'home/delete_post.html'
    success_url = reverse_lazy('home')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('home')
                else:
                    return HttpResponse('DeActive Hastid')
            else:
                return HttpResponse('etelaAte Shoma Ghalate')

    else:
        form = LoginForm()

    return render(request,'member/login.html',{'form':form})


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'member/register.html'
    success_url = reverse_lazy('home')

class UserEditView(generic.UpdateView):
    form_class = EditProfilForm
    template_name = 'member/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

def user_logout(request):
    logout(request)
    return redirect('home')

class PassChangeVW(PasswordChangeView):
    form_class = PassChangedForm
    #success_url = reverse_lazy('home')
    success_url = reverse_lazy('password_changed')


def passs_changed(request):
    return render(request,'member/pass_su.html', {})


class ProfilePageView(DetailView):
    model = Profile
    template_name = 'member/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        #users = Profile.objects.all()
        context = super(ProfilePageView,self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id = self.kwargs['pk'])

        context['page_user']= page_user

        return context


class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'member/edit_profile_page.html'
    success_url = reverse_lazy('home')
    fields = ['bio', 'profile_pic', 'website_url', 'instagram_url', 'twitter_url']


class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'member/create_profile_page.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddCommentview(CreateView):
    model = Comment
    form_class = AddCommentForm
    template_name = 'member/add_comment.html'
    #fields = '__all__'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('home')