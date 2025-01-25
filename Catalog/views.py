from django.shortcuts import render
# from models import Category, Collection, ClothingItem, ItemPhoto, ItemColor, Tag, MaterialComposition,FootwearSize, ClothingTopSize,ClothingBottomSize,Like
from django.contrib.auth.models import User
from django.views.generic import TemplateView

class TestView(TemplateView):
    template_name = "test_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Test Page"
        return context





