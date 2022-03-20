"""frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.urls import include
from django.urls import path


urlpatterns = [
    path("", include("frontend.urls")),
]
