from django.shortcuts import render, redirect
from .models import Mainthread,Subthread, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib import messages

def home(request):
    Thread = Mainthread.objects.annotate(num_topics=Count('subthread'))[0:4]
    othersub = Mainthread.objects.annotate(num_of_topics=Count('subthread'))[4:]
    total_topics = Subthread.objects.count()
    total_posts = Comment.objects.count()
    # below list contain number of comments from each thread
    list=[]
    for x in Thread:
        list.append(Subthread.objects.filter(mainthread=x.id).aggregate(com = Count('comment')))

    newzip = zip(Thread,list)
    # below list contain number of comments from each thread from other subjects
    post_list = []
    for y in othersub:
        post_list.append(Subthread.objects.filter(mainthread=y.id).aggregate(com = Count('comment')))


    two_zip = zip(othersub,post_list)


    context = {
    'Threads':newzip,
    'othersubs': two_zip,
    'total_topics':total_topics,
    'total_posts':total_posts,
    }
    return render(request,'home.html',context)
#to each subthreads
def thread(request, my_id):

    Mthread = Mainthread.objects.get(id=my_id)
    #reply_count contains number of comments per topic.
    Sthread = Subthread.objects.filter(mainthread=my_id).annotate(reply_count=Count('comment'))
    #total_comment contains total comments
    total_comment = Subthread.objects.filter(mainthread=my_id).aggregate(com = Count('comment'))

    #to get views
    Mthread.number_of_views += 1
    Mthread.save()

    context={
        'Mthreads':Mthread,
        'Sthreads':Sthread,
        'count':total_comment,


    }
    return render(request,'forum/thread.html',context)
#to create a topic.
@login_required
def create(request,my_id):
    print(my_id)
    Mthread = Mainthread.objects.get(id=my_id)
    if request.method =='POST':
        postform = PostForm(request.POST)
        if postform.is_valid():

            data = postform.save(commit=False)
            data.user = request.user
            data.mainthread = Mthread
            data.time = datetime.time(datetime.now())
            data.date = datetime.now()
            postform.save()
            return redirect('/thread/{id}'.format(id=my_id))
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
            data.date = datetime.now()
            data.time = datetime.time(datetime.now())
            commentform.save()
            return HttpResponseRedirect(request.path_info)
    else:
        commentform = CommentForm()
        Sthread.number_of_views += 1
        Sthread.save()

    context={
    'Divison' : Mthread,
    'Topic'   : Sthread,
    'commentforms':commentform,
    'replies' :replies,

    }
    return render(request,'forum/discussion.html',context)

@login_required
def delete_topic(request,thread_id,topic_id):
    Sthread = Subthread.objects.get(id=topic_id)

    if request.user == Sthread.user:
        Sthread.delete()
        #redirecting to subthread page
        return redirect('/thread/{id}'.format(id=thread_id))
    else:
        messages.info(request,'You dont have permission')
        #redirecting to same page
        return redirect('discussion',thread_ids=thread_id, topic_ids=topic_id)
@login_required
def delete_comment(request,thread_id,topic_id,comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()
        # redirecting to same page

        return redirect('discussion',thread_ids=thread_id, topic_ids=topic_id)
    else:
        messages.info(request,'You dont have permission')
        #redirecting to same page
        return redirect('discussion',thread_ids=thread_id, topic_ids=topic_id)


