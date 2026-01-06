"""
Views para LMS + Knowledge Base
================================
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Category, Topic, Tag


class HomeView(ListView):
    """
    Vista principal: Buscador + Categorías destacadas.
    """
    model = Topic
    template_name = 'core/home.html'
    context_object_name = 'recent_topics'
    
    def get_queryset(self):
        """Obtiene los últimos 6 topics publicados."""
        return Topic.objects.filter(is_published=True).select_related('category', 'video')[:6]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class TopicDetailView(DetailView):
    """
    Vista de detalle del Topic con reproductor inteligente.
    """
    model = Topic
    template_name = 'core/topic_detail.html'
    context_object_name = 'topic'
    slug_field = 'code'
    slug_url_kwarg = 'code'
    
    def get_queryset(self):
        """Solo muestra topics publicados."""
        return Topic.objects.filter(is_published=True).select_related('category', 'video').prefetch_related('tags', 'quizzes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.object
        
        # Navegación prev/next
        context['prev_topic'] = topic.get_previous_topic()
        context['next_topic'] = topic.get_next_topic()
        
        # Quizzes relacionados
        context['quizzes'] = topic.quizzes.filter(is_active=True)
        
        return context


class CategoryView(ListView):
    """
    Vista de topics filtrados por categoría (Modo Biblioteca).
    """
    model = Topic
    template_name = 'core/category_list.html'
    context_object_name = 'topics'
    paginate_by = 20
    
    def get_queryset(self):
        """Filtra por categoría."""
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Topic.objects.filter(
            category=self.category,
            is_published=True
        ).select_related('video', 'category').order_by('code')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['all_categories'] = Category.objects.all()
        return context


class SearchView(ListView):
    """
    Buscador inteligente: Title, Code, Tags.
    """
    model = Topic
    template_name = 'core/search_results.html'
    context_object_name = 'results'
    paginate_by = 20
    
    def get_queryset(self):
        """Búsqueda en Title, Code y Tags."""
        query = self.request.GET.get('q', '').strip()
        self.query = query
        
        if not query:
            return Topic.objects.none()
        
        # Búsqueda en múltiples campos
        return Topic.objects.filter(
            Q(title__icontains=query) |
            Q(code__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(description__icontains=query),
            is_published=True
        ).select_related('category', 'video').distinct().order_by('code')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['total_results'] = self.get_queryset().count()
        return context


class CourseView(ListView):
    """
    Modo Curso: Lista secuencial ordenada por código.
    """
    model = Topic
    template_name = 'core/course_mode.html'
    context_object_name = 'topics'
    paginate_by = 50
    
    def get_queryset(self):
        """Todos los topics ordenados por código."""
        return Topic.objects.filter(
            is_published=True
        ).select_related('category', 'video').order_by('code')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_topics'] = self.get_queryset().count()
        return context
