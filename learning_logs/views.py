from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """学习笔记主页"""
    # 只显示非私有的主题和条目
    topics = Topic.objects.filter(private=False).order_by('date_added')
    entries = Entry.objects.filter(private=False).order_by('-date_added')[:5]
    
    context = {'topics': topics, 'entries': entries}
    return render(request, 'learning_logs/index.html', context)

@login_required
def topics(request):
    """显示用户的所有主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个主题及其所有条目"""
    topic = Topic.objects.get(id=topic_id)
    # 确保主题属于当前用户
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 没有提交数据；创建一个空表单
        form = TopicForm()
    else:
        # 提交了数据；处理数据
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # 显示空白或无效的表单
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def edit_topic(request, topic_id):
    """修改一个现有的主题"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # 没有提交数据；创建一个空表单
        form = TopicForm(instance=topic)
    else:
        # 提交了数据；处理数据
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # 显示空白或无效的表单
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)
        

@login_required
def new_entry(request, topic_id):
    """添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # 没有提交数据；创建一个空表单
        form = EntryForm()
    else:
        # 提交了数据；处理数据
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # 显示空白或无效的表单
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑现有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_topic(request, topic_id):
    """删除主题及其所有条目"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        # POST data submitted; delete topic and all its entries.
        topic.delete()
        return redirect('learning_logs:topics')

    # Display confirmation page for POST data.
    context = {'topic': topic}
    return render(request, 'learning_logs/delete_topic.html', context)

@login_required
def delete_entry(request, entry_id):
    """删除条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        # POST data submitted; delete entry and return to topic page.
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)

    # Display confirmation page for POST data.
    context = {'entry': entry, 'topic': topic}
    return render(request, 'learning_logs/delete_entry.html', context)

@login_required
def share_entry(request, token):
    share_url = f"{request.scheme}://{request.get_host()}/shared_entry/{token}"
    entry = get_object_or_404(Entry, token=token)
    return render(request, 'learning_logs/share_entry.html', {'share_url': share_url,'entry':entry})

def shared_entry(request, token):
    entry = Entry.objects.get(token=token)
    return render(request, 'learning_logs/shared_entry.html', {'entry': entry})

def entry_token(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    return redirect('learning_logs:share_entry', token=entry.token)

def logs(request):
    """显示日志"""
    logs = []
    class Log:
        def __init__(self, date, message):
            self.message = message.replace('\\n', '\n')
            self.date_added = date
        def __str__(self):
            return self.message
    with open('learning_log/logs.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(' ', 1)
            logs.append(Log(parts[0], parts[1] if len(parts) > 1 else ''))
    context = {'logs': logs}
    return render(request, 'learning_logs/logs.html', context)