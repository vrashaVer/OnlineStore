from django.shortcuts import render
# from models import Category, Collection, ClothingItem, ItemPhoto, ItemColor, Tag, MaterialComposition,FootwearSize, ClothingTopSize,ClothingBottomSize,Like
from django.contrib.auth.models import User
from django.views.generic import TemplateView, View
from Catalog.footer_help_data import category_data

class TestView(TemplateView):
    template_name = "test_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Test Page"
        return context
    

# HElP

class AccountHelpView(TemplateView):
    template_name = "help/account_help.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Категорії з підсторінками та інформацією
        global category_data
        categories = category_data

        active_category = kwargs.get('category')  # Отримання категорії
        active_section = kwargs.get('section')  # Отримання секції

        # Перевіряємо, чи категорія існує
        if active_category not in categories:
            raise KeyError(f"Category '{active_category}' not found.")

        # Дані категорії
        category_info = categories[active_category]
        sections = category_info['sections']

        # Якщо секція не задана, перенаправляємо на перший розділ категорії
        if not active_section:
            first_section = next(iter(sections))  # Перший ключ секції
            self.template_name = 'help/account_help.html'
            return self.get_context_data(category=active_category, section=first_section)

        # Якщо секція задана, перевіряємо, чи вона існує
        if active_section not in sections:
            raise KeyError(f"Section '{active_section}' not found in category '{active_category}'.")

        # Додаємо дані до контексту
        context['categories'] = categories
        context['active_category'] = active_category
        context['category_name'] = category_info['name']
        context['sections'] = sections
        context['active_section'] = active_section
        context['active_section_data'] = sections[active_section]
        
        return context
class AboutView(TemplateView):
    template_name = "help/about_us.html"


class JoinUsView(TemplateView):
    template_name = "help/join_us.html"


