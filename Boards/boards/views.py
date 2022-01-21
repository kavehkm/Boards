# django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# internal
from django.db.models import Count
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


def pager(request, query_set):
    page = request.GET.get('page', 1)
    paginator = Paginator(query_set, 10)
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    return current_page


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    query_set = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    topics = pager(request, query_set)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        user = request.user
        if form.is_valid():
            # create topic
            topic = Topic.objects.create(
                subject=form.cleaned_data.get('subject'),
                board=board,
                starter=user
            )
            # create post
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    # increase views value and save
    topic.views += 1
    topic.save()
    posts = pager(request, topic.posts.order_by('created_at'))
    return render(request, 'topic_posts.html', {'topic': topic, 'posts': posts})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                topic=topic,
                created_by=request.user,
                message=form.cleaned_data.get('message')
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'form': form, 'topic': topic})
