from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view()),
    path("healthcheck/", views.Healthcheck.as_view(), name="healthcheck"),
]
