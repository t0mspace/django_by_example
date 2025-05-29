
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="posts"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>", views.detail, name="detail"),
    path("<int:post_id>/share/", views.share, name="share"),
]
