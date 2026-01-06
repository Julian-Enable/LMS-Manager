"""
LMS + Knowledge Base - Core Models
===================================

Arquitectura de Datos:
- Category: Categorías macro (Ventas, Inventario, CEDI)
- VideoAsset: Almacena la referencia física del video (plataforma + ID externo)
- Topic: El conocimiento/tema (la unidad central) que apunta a un video y timestamp específico
- Quiz: Evaluaciones que pueden agrupar múltiples Topics
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


class Category(models.Model):
    """
    Categorías macro para organizar los temas.
    Ejemplo: Ventas, Inventario, CEDI, Finanzas, etc.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de la Categoría"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Slug (URL amigable)"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Clase CSS del icono (ej: 'fa-shopping-cart')",
        verbose_name="Icono"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Orden de visualización (menor = primero)",
        verbose_name="Orden"
    )
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class VideoAsset(models.Model):
    """
    Almacena la referencia al archivo de video físico.
    Este modelo NO tiene timestamps, solo guarda dónde está el video.
    """
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('cloudflare', 'Cloudflare Stream'),
        ('drive', 'Google Drive'),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name="Título del Video",
        help_text="Nombre interno del archivo de video"
    )
    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        default='youtube',
        verbose_name="Plataforma"
    )
    external_id = models.CharField(
        max_length=100,
        verbose_name="ID Externo",
        help_text="ID del video en la plataforma (ej: dQw4w9WgXcQ para YouTube)"
    )
    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Duración (segundos)",
        help_text="Duración total del video en segundos"
    )
    uploaded_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Subida"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción del Video"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Video Asset"
        verbose_name_plural = "Video Assets"
        ordering = ['-created_at']
        unique_together = ['platform', 'external_id']
    
    def __str__(self):
        return f"{self.title} ({self.get_platform_display()})"
    
    def get_embed_url(self, start_seconds=None):
        """
        Genera la URL de embed según la plataforma.
        Si se proporciona start_seconds, incluye el timestamp.
        """
        if self.platform == 'youtube':
            base_url = f"https://www.youtube.com/embed/{self.external_id}"
            params = []
            if start_seconds:
                params.append(f"start={start_seconds}")
            if params:
                return f"{base_url}?{'&'.join(params)}"
            return base_url
        
        elif self.platform == 'vimeo':
            base_url = f"https://player.vimeo.com/video/{self.external_id}"
            if start_seconds:
                # Vimeo usa #t= para timestamps
                return f"{base_url}#t={start_seconds}s"
            return base_url
        
        elif self.platform == 'cloudflare':
            # Cloudflare Stream
            base_url = f"https://iframe.cloudflarestream.com/{self.external_id}"
            if start_seconds:
                return f"{base_url}?startTime={start_seconds}"
            return base_url
        
        elif self.platform == 'drive':
            # Google Drive - formato: https://drive.google.com/file/d/FILE_ID/preview
            base_url = f"https://drive.google.com/file/d/{self.external_id}/preview"
            # Google Drive no soporta timestamps en embed, pero podemos intentar con parámetro t
            if start_seconds:
                return f"{base_url}?t={start_seconds}s"
            return base_url
        
        return ""
    
    def get_watch_url(self, start_seconds=None):
        """
        Genera la URL pública de visualización (no embed).
        """
        if self.platform == 'youtube':
            base_url = f"https://www.youtube.com/watch?v={self.external_id}"
            if start_seconds:
                return f"{base_url}&t={start_seconds}s"
            return base_url
        
        elif self.platform == 'vimeo':
            base_url = f"https://vimeo.com/{self.external_id}"
            if start_seconds:
                return f"{base_url}#t={start_seconds}s"
            return base_url
        
        elif self.platform == 'cloudflare':
            return f"https://cloudflarestream.com/{self.external_id}"
        
        elif self.platform == 'drive':
            # Google Drive - URL de visualización
            return f"https://drive.google.com/file/d/{self.external_id}/view"
        
        return ""


class Topic(models.Model):
    """
    LA UNIDAD CENTRAL del sistema.
    Representa un tema/conocimiento específico dentro de un video.
    
    Un video puede tener múltiples Topics (timestamps diferentes).
    Ejemplo: "Gestión de Ventas" (video) tiene:
      - Topic 1.11: "Toma de Pedido" (empieza en 00:30)
      - Topic 1.12: "Facturación" (empieza en 15:45)
      - Topic 1.13: "Cierre" (empieza en 28:10)
    """
    LOCATION_CHOICES = [
        ('piso_1', 'Piso 1'),
        ('piso_2', 'Piso 2'),
        ('piso_3', 'Piso 3'),
        ('piso_4', 'Piso 4'),
        ('caja', 'Caja'),
        ('bodega', 'Bodega'),
        ('cedi', 'CEDI'),
        ('oficina', 'Oficina'),
        ('remoto', 'Remoto'),
        ('general', 'General'),
    ]
    
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código",
        help_text="Código del tema (ej: '1.13', '2.15') para ordenamiento secuencial"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Título del Tema",
        help_text="Ej: 'Creación de Cliente', 'Proceso de Facturación'"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='topics',
        verbose_name="Categoría"
    )
    video = models.ForeignKey(
        VideoAsset,
        on_delete=models.CASCADE,
        related_name='topics',
        verbose_name="Video",
        help_text="Video que contiene este tema"
    )
    start_seconds = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name="Inicia en (segundos)",
        help_text="Segundo exacto donde empieza este tema en el video"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Notas, instrucciones, contexto. Soporta Markdown."
    )
    location_tag = models.CharField(
        max_length=20,
        choices=LOCATION_CHOICES,
        blank=True,
        verbose_name="Ubicación/Contexto",
        help_text="Contexto físico donde aplica este tema (informativo)"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Publicado",
        help_text="Desmarcar para ocultar este tema del sistema"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tema"
        verbose_name_plural = "Temas"
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['category', 'code']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.title}"
    
    def get_absolute_url(self):
        """URL canónica del tema."""
        return reverse('topic_detail', kwargs={'code': self.code})
    
    def get_video_url_with_timestamp(self):
        """
        Genera la URL de YouTube (o plataforma) con el timestamp.
        Este es el método clave para el reproductor inteligente.
        """
        return self.video.get_watch_url(start_seconds=self.start_seconds)
    
    def get_embed_url_with_timestamp(self):
        """
        Genera la URL de embed con timestamp para el reproductor.
        """
        return self.video.get_embed_url(start_seconds=self.start_seconds)
    
    def get_formatted_timestamp(self):
        """
        Convierte start_seconds a formato MM:SS o HH:MM:SS.
        Ejemplo: 125 -> "02:05", 3665 -> "01:01:05"
        """
        hours = self.start_seconds // 3600
        minutes = (self.start_seconds % 3600) // 60
        seconds = self.start_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_next_topic(self):
        """
        Obtiene el siguiente tema en el orden secuencial por código.
        Útil para navegación tipo curso.
        """
        try:
            return Topic.objects.filter(
                code__gt=self.code,
                is_published=True
            ).order_by('code').first()
        except Topic.DoesNotExist:
            return None
    
    def get_previous_topic(self):
        """
        Obtiene el tema anterior en el orden secuencial por código.
        """
        try:
            return Topic.objects.filter(
                code__lt=self.code,
                is_published=True
            ).order_by('-code').first()
        except Topic.DoesNotExist:
            return None


class Tag(models.Model):
    """
    Tags para búsqueda de errores o conceptos específicos.
    Ejemplo: "Error 505", "Saldo negativo", "Timeout"
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre del Tag"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Slug"
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='tags',
        blank=True,
        verbose_name="Temas"
    )
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_topic_count(self):
        """Retorna el número de temas asociados a este tag."""
        return self.topics.count()


class Quiz(models.Model):
    """
    Evaluación que puede agrupar múltiples temas.
    Un quiz puede evaluar conocimientos de varios Topics relacionados.
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Título del Quiz"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='quizzes',
        verbose_name="Temas Evaluados",
        help_text="Selecciona los temas que este quiz evalúa"
    )
    passing_score = models.PositiveIntegerField(
        default=70,
        verbose_name="Puntaje Mínimo (%)",
        help_text="Porcentaje mínimo para aprobar"
    )
    time_limit_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Tiempo Límite (minutos)",
        help_text="Dejar en blanco para sin límite"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_topic_codes(self):
        """
        Retorna una lista de códigos de los temas asociados.
        Ej: ['1.11', '1.12', '1.13']
        """
        return list(self.topics.values_list('code', flat=True).order_by('code'))
    
    def get_total_duration_seconds(self):
        """
        Calcula la duración total estimada basada en los videos de los topics.
        """
        total = 0
        for topic in self.topics.all():
            if topic.video.duration_seconds:
                total += topic.video.duration_seconds
        return total
