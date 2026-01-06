"""
Django Admin Configuration para LMS + Knowledge Base
=====================================================
Interfaz administrativa optimizada para gestionar contenido del sistema.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, VideoAsset, Topic, Tag, Quiz


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin para categorías con ordenamiento y previsualización.
    """
    list_display = ['name', 'slug', 'icon_preview', 'order', 'topic_count']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    
    def icon_preview(self, obj):
        """Muestra el icono si está configurado."""
        if obj.icon:
            return format_html('<i class="{}"></i> {}', obj.icon, obj.icon)
        return '-'
    icon_preview.short_description = 'Icono'
    
    def topic_count(self, obj):
        """Muestra el número de topics en esta categoría."""
        return obj.topics.count()
    topic_count.short_description = 'Temas'


@admin.register(VideoAsset)
class VideoAssetAdmin(admin.ModelAdmin):
    """
    Admin para videos con preview y validación.
    """
    list_display = ['title', 'platform', 'external_id', 'duration_formatted', 'topic_count', 'created_at']
    list_filter = ['platform', 'created_at']
    search_fields = ['title', 'external_id', 'description']
    readonly_fields = ['created_at', 'updated_at', 'preview_url']
    fieldsets = [
        ('Información del Video', {
            'fields': ['title', 'platform', 'external_id', 'duration_seconds', 'uploaded_date']
        }),
        ('Descripción', {
            'fields': ['description']
        }),
        ('Vista Previa', {
            'fields': ['preview_url'],
            'classes': ['collapse']
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def duration_formatted(self, obj):
        """Muestra la duración en formato MM:SS."""
        if obj.duration_seconds:
            hours = obj.duration_seconds // 3600
            minutes = (obj.duration_seconds % 3600) // 60
            seconds = obj.duration_seconds % 60
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            return f"{minutes:02d}:{seconds:02d}"
        return '-'
    duration_formatted.short_description = 'Duración'
    
    def topic_count(self, obj):
        """Muestra el número de topics que usan este video."""
        count = obj.topics.count()
        return format_html('<strong>{}</strong> temas', count)
    topic_count.short_description = 'Topics'
    
    def preview_url(self, obj):
        """Genera un link de previsualización del video."""
        url = obj.get_watch_url()
        if url:
            return format_html('<a href="{}" target="_blank">Ver video en {}</a>', url, obj.get_platform_display())
        return '-'
    preview_url.short_description = 'Preview'


class TagInline(admin.TabularInline):
    """
    Inline para gestionar tags desde el admin de Topic.
    """
    model = Tag.topics.through
    extra = 1
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """
    Admin principal para Topics - El corazón del sistema.
    """
    list_display = [
        'code', 
        'title', 
        'category', 
        'video_link', 
        'timestamp_formatted', 
        'location_tag',
        'tag_count',
        'is_published'
    ]
    list_filter = ['category', 'location_tag', 'is_published', 'created_at']
    search_fields = ['code', 'title', 'description', 'tags__name']
    list_editable = ['is_published']
    prepopulated_fields = {}
    autocomplete_fields = ['video', 'category']
    readonly_fields = ['created_at', 'updated_at', 'video_preview', 'navigation_links']
    inlines = [TagInline]
    
    fieldsets = [
        ('Identificación', {
            'fields': ['code', 'title', 'category']
        }),
        ('Video y Timestamp', {
            'fields': ['video', 'start_seconds', 'video_preview'],
            'description': 'El timestamp es en SEGUNDOS. Ej: 125 = 02:05'
        }),
        ('Contenido', {
            'fields': ['description', 'location_tag']
        }),
        ('Configuración', {
            'fields': ['is_published']
        }),
        ('Navegación', {
            'fields': ['navigation_links'],
            'classes': ['collapse']
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    ordering = ['code']
    
    def timestamp_formatted(self, obj):
        """Muestra el timestamp en formato legible."""
        formatted = obj.get_formatted_timestamp()
        return format_html(
            '<code>{}</code> <small>({}s)</small>', 
            formatted, 
            obj.start_seconds
        )
    timestamp_formatted.short_description = 'Inicia en'
    
    def video_link(self, obj):
        """Link al video externo."""
        return format_html(
            '<a href="{}" target="_blank" title="{}">{}</a>',
            obj.get_video_url_with_timestamp(),
            obj.video.title,
            obj.video.title[:30] + '...' if len(obj.video.title) > 30 else obj.video.title
        )
    video_link.short_description = 'Video'
    
    def tag_count(self, obj):
        """Muestra el número de tags."""
        count = obj.tags.count()
        if count > 0:
            tags = ', '.join([tag.name for tag in obj.tags.all()[:3]])
            if count > 3:
                tags += f'... (+{count-3})'
            return format_html('<span title="{}">{} tags</span>', tags, count)
        return '-'
    tag_count.short_description = 'Tags'
    
    def video_preview(self, obj):
        """Muestra un iframe de preview del video con timestamp."""
        if obj.video:
            embed_url = obj.get_embed_url_with_timestamp()
            return format_html(
                '<iframe width="560" height="315" src="{}" '
                'frameborder="0" allowfullscreen></iframe><br>'
                '<a href="{}" target="_blank">Abrir en nueva ventana</a>',
                embed_url,
                obj.get_video_url_with_timestamp()
            )
        return '-'
    video_preview.short_description = 'Preview del Video'
    
    def navigation_links(self, obj):
        """Muestra links de navegación al topic anterior/siguiente."""
        prev_topic = obj.get_previous_topic()
        next_topic = obj.get_next_topic()
        
        html = '<div>'
        if prev_topic:
            html += format_html(
                '← <a href="/admin/core/topic/{}/change/">Anterior: {} - {}</a><br>',
                prev_topic.id,
                prev_topic.code,
                prev_topic.title
            )
        if next_topic:
            html += format_html(
                '<a href="/admin/core/topic/{}/change/">Siguiente: {} - {}</a> →',
                next_topic.id,
                next_topic.code,
                next_topic.title
            )
        if not prev_topic and not next_topic:
            html += 'No hay temas adyacentes'
        html += '</div>'
        return format_html(html)
    navigation_links.short_description = 'Navegación'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin para tags con contador de topics.
    """
    list_display = ['name', 'slug', 'topic_count_display', 'topic_preview']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    filter_horizontal = ['topics']
    
    def topic_count_display(self, obj):
        """Muestra el número de topics etiquetados."""
        count = obj.get_topic_count()
        return format_html('<strong>{}</strong> temas', count)
    topic_count_display.short_description = 'Temas'
    
    def topic_preview(self, obj):
        """Muestra preview de los topics asociados."""
        topics = obj.topics.all()[:5]
        if topics:
            preview = ', '.join([f"{t.code}" for t in topics])
            if obj.get_topic_count() > 5:
                preview += f'... (+{obj.get_topic_count()-5})'
            return preview
        return '-'
    topic_preview.short_description = 'Preview'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """
    Admin para quizzes con selector de topics.
    """
    list_display = ['title', 'topic_count_display', 'passing_score', 'time_limit_minutes', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['topics']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at', 'topic_codes_display', 'estimated_duration']
    
    fieldsets = [
        ('Información del Quiz', {
            'fields': ['title', 'description']
        }),
        ('Temas Evaluados', {
            'fields': ['topics', 'topic_codes_display']
        }),
        ('Configuración', {
            'fields': ['passing_score', 'time_limit_minutes', 'is_active']
        }),
        ('Estadísticas', {
            'fields': ['estimated_duration'],
            'classes': ['collapse']
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def topic_count_display(self, obj):
        """Muestra el número de topics incluidos."""
        count = obj.topics.count()
        return format_html('<strong>{}</strong> temas', count)
    topic_count_display.short_description = 'Topics'
    
    def topic_codes_display(self, obj):
        """Muestra los códigos de los topics incluidos."""
        codes = obj.get_topic_codes()
        if codes:
            return ', '.join(codes)
        return 'No hay temas asignados'
    topic_codes_display.short_description = 'Códigos de Temas'
    
    def estimated_duration(self, obj):
        """Muestra la duración estimada total."""
        total_seconds = obj.get_total_duration_seconds()
        if total_seconds:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            if hours > 0:
                return f"{hours}h {minutes}m"
            return f"{minutes}m"
        return 'No calculado'
    estimated_duration.short_description = 'Duración Estimada'


# Configuración del sitio admin
admin.site.site_header = 'LMS + Knowledge Base - Administración'
admin.site.site_title = 'LMS Admin'
admin.site.index_title = 'Panel de Administración'
