from smtplib import SMTPException

from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404

from .forms import EmailPostForm
from .models import Post

def index(request):
  posts = get_list_or_404(Post, status=Post.Status.PUBLISHED)
  paginator = Paginator(posts, 10)
  page_number = request.GET.get('page', 1)
  try:
    posts = paginator.page(page_number)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  return render(request, 'blog/post/list.html', {
    'posts': posts,
  })

def detail(request, year, month, day, post):
  post = get_object_or_404(Post,
                           status=Post.Status.PUBLISHED,
                           slug=post,
                           publish__year=year,
                           publish__month=month,
                           publish__day=day
                           )
  return render(request, 'blog/post/detail.html', {
    'post': post,
  })

def share(request, post_id):
  post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
  sent = False
  if(request.method == 'POST'):
    form = EmailPostForm(request.POST)
    if form.is_valid():
      safeData = form.cleaned_data
      post_url = request.build_absolute_uri(
        post.get_absolute_url()
      )
      subject = (
        f"{safeData['name']} ({safeData['email']}) "
        f"recommends you read {post.title}"
      )
      message = (
        f"Read {post.title} at {post_url}\n\n"
        f"{safeData['name']}\'s comments: {safeData['comments']}"
      )
      try:
        send_mail(
          subject=subject,
          message=message,
          from_email=None,
          recipient_list=[safeData['to']]
        )
        sent = True
      except SMTPException:
        messages.error(request, "There was an error sending the email. Please try again later.")
        sent = False

  else:
    form = EmailPostForm()

  return render(
    request,
    'blog/post/share.html',
    {
      'post': post,
      'form': form,
      'sent': sent
    }
  )

