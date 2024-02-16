from django.shortcuts import render, redirect
from .models import Blogger, Post, BlockedUser
from .forms import PostForm, BlockedUserForm


# Create your views here.
def posts(request):
    blogger = Blogger.objects.get(user=request.user)
    blocked_users = BlockedUser.objects.filter(user=blogger)
    blocked_user_ids = blocked_users.values_list('blocked_user_id', flat=True)
    posts_blocked = Post.objects.exclude(author_id__in=blocked_user_ids).exclude(author__user=request.user)
    dictionary = {'posts': posts_blocked}
    return render(request, "Posts.html", context=dictionary)


def addPost(request):
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            add = form.save(commit=False)
            add.author = Blogger.objects.get(user=request.user)
            form.photo = form.cleaned_data['image']
            add.save()
            return redirect("AddPost")
    return render(request, "AddPost.html", context={"form": PostForm})


def blockedUsers(request):
    blogger = Blogger.objects.get(user=request.user)
    blocked_users = BlockedUser.objects.filter(user=blogger).values_list("blocked_user", flat=True)
    blocked_by_blogger = []
    for block in blocked_users:
        blogger_block = Blogger.objects.get(user=block)
        blocked_by_blogger.append(blogger_block)

    if request.method == "POST":
        form = BlockedUserForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            block = form.save(commit=False)
            block.user = Blogger.objects.get(user=request.user)
            block.save()
            return redirect("BlockedUsers")
    dictionary = {"blogger": blogger, "blocked": blocked_by_blogger, "form": BlockedUserForm}
    return render(request, "BlockedUsers.html", context=dictionary)


def profile(request):
    author = Blogger.objects.get(user=request.user)
    posts = Post.objects.filter(author=author)
    dictionary = {"posts": posts, "blogger": Blogger.objects.get(user=request.user)}
    return render(request, "Profile.html", context=dictionary)
