from django.shortcuts import get_object_or_404, render,redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

from main.models import Post, Category
from account.models import Account
def home(request):
    return render(request, 'main/home.html')
def post_list(request):
    print(request.user.username)
    context={}
    
    category_id = request.GET.get('category')

    posts = Post.objects.filter(deadline__gte=timezone.now())
    vacancies=Post.objects.first().vacancy
    vacancy_list = vacancies.split('\n')
    attributes=Post.objects.first().attributes
    attributes_list=attributes.split('\n')

    if category_id:
        category = Category.objects.get(pk=category_id)
        posts = posts.filter(category=category)

    categories = Category.objects.all()

    context['vacancy_list']=vacancy_list
    context['attributes_list']=attributes_list
    context['posts']=posts
    context['categories']=categories
    context['category_id']=category_id

    return render(request, 'main/post_list.html', context)

# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'main/post_list.html', {'posts': posts})
@login_required
def post_detail(request, pk):
    context={}
    uname=request.user.username
    user= Account.objects.get(username=uname)
    user1=user.is_activated
    if user1==False:
        return redirect('activate')
    else:
        post = Post.objects.get(pk=pk)
        vacancy_list = post.vacancy.split('\n')
        attribute_list=post.attributes.split('\n')
    context['vacancy_list']=vacancy_list
    context['attribute_list']=attribute_list
    context['post']=post


    return render(request, 'main/post_detail.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = Category.objects.get(pk=pk)
    posts = Post.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'posts': posts})




@login_required
def post_create(request):
    categories = Category.objects.all()
      
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        
        if title and content and category_id:
            category = Category.objects.get(pk=category_id)
            post = Post(title=title, content=content, category=category,author=request.user.username)
            post.save()
            return redirect('post_list')  # Redirect to the list of posts
    
    return render(request, 'staff/post_create.html', {'categories': categories})
@login_required
def post_edit(request, pk):
    categories=Category.objects.all()
    post = get_object_or_404(Post, pk=pk)
    if not request.user.username==post.author:
        print('error: not  legit author')
        return redirect('post_list')
    else:
    
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            category_id = request.POST.get('category')
            
            if title and content and category_id:
                category = Category.objects.get(pk=category_id)
                post.title = title
                post.content = content
                post.category = category
                post.save()
                return redirect('post_list')  # Redirect to the list of posts
    
    return render(request, 'staff/post_edit.html', {'post': post, 'categories': categories})
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if  request.user.username==post.author:    
        post.delete()
    return redirect('post_list')