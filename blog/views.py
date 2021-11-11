from django.core import paginator
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag
from .forms import EmailForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.db.models import Q

def post_list(request, tag_slug=None):
    form = SearchForm()
    object_list = Post.objects.filter(status='published')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list,1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    q = request.GET.get('q')
    if q:
        posts = object_list.filter(Q(title__contains=q) |  Q(body__contains=q) ) 
    return render(request, 'blog/post/list.html',{'posts':posts, 'page':page,'tag':tag,'form':form})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post.comments.filter(active = True)
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        form = CommentForm()
    #rekomendatsiya
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.objects.filter(status='published').filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = set(similar_posts[:4])
    context = {
        'post':post,
        'form': form,
        'new_comment': new_comment,
        'comments': comments,
        'similar_posts':similar_posts,
    }
    return render(request, 'blog/post/detail.html', context)


def post_share(request, id):
    post = get_object_or_404(Post, id=id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} sizga {post.title} ni o'qishni tavsiya qiladi."
            message = f"Salom, yaxshimisiz. Quyidagi linkdagi postni o'qib ko'ring. {post_url}\n\nComents:{cd['comments']}"
            send_mail(subject,message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form,'sent':sent})
