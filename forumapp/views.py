from django.shortcuts import render, redirect
from .models import Mainthread,Subthread, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect

def home(request):
    Thread = Mainthread.objects.annotate(num_topics=Count('subthread'))[0:4]

    othersub = Mainthread.objects.annotate(num_of_topics=Count('subthread'))[4:]

    context = {
    'Threads':Thread,
    'othersubs': othersub,



    }
    return render(request,'home.html',context)

def thread(request, my_id):

    Mthread = Mainthread.objects.get(id=my_id)
    Sthread = Subthread.objects.filter(mainthread=my_id)
    Mthread.number_of_views += 1
    Mthread.save()

    context={
        'Mthreads':Mthread,
        'Sthreads':Sthread,


    }
    return render(request,'forum/thread.html',context)
#to create a topic.
@login_required
def create(request,my_id):
    Mthread = Mainthread.objects.get(id=my_id)
    if request.method =='POST':
        postform = PostForm(request.POST)
        if postform.is_valid():
            data = postform.save(commit=False)
            data.user = request.user
            data.mainthread = Mthread
            postform.save()
            return redirect('/')
    else:
        postform = PostForm()
    context = {
        'Mthreads':Mthread,
        'postforums':postform,
    }
    return render(request,'forum/create.html',context)

def discussion(request,thread_ids,topic_ids):
    Mthread = Mainthread.objects.get(id=thread_ids)
    Sthread = Subthread.objects.get(id=topic_ids)
    replies = Comment.objects.filter(subthread=topic_ids)
    if request.method == 'POST':
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            data = commentform.save(commit=False)
            data.user = request.user
            data.subthread = Sthread
            commentform.save()
            return HttpResponseRedirect(request.path_info)
    else:
        commentform = CommentForm()

    context={
    'Divison' : Mthread,
    'Topic'   : Sthread,
    'commentforms':commentform,
    'replies' :replies,

    }
    return render(request,'forum/discussion.html',context)

"""def test(request):
    objs=Subthread.objects.all()
    context = {
    'obj':objs


    }
    return render(request,'test.html',context)
"""
