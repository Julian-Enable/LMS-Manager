# LMS + Knowledge Base Platform

Plataforma híbrida LMS (Sistema de Aprendizaje) + Knowledge Base (Biblioteca de Conocimiento) para gestión de videos de capacitación con navegación por timestamps.

## 🚀 Características

- **Búsqueda Inteligente**: Busca por título, código o tags de error
- **Reproductor Inteligente**: Salto automático al timestamp exacto
- **Modo Curso**: Vista secuencial para aprendizaje estructurado
- **Modo Biblioteca**: Navegación por categorías y búsqueda libre
- **Multi-plataforma**: Soporte para YouTube, Vimeo, Cloudflare Stream

## 📋 Requisitos

- Python 3.11+
- Django 5.x
- PostgreSQL (producción) / SQLite (desarrollo)

## 🛠️ Instalación Local

```bash
# Clonar el repositorio
git clone <repo-url>
cd "LMS Manager"

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Correr servidor
python manage.py runserver
```

Accede a:
- **Frontend**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

## 🎯 Uso

### Agregar Contenido

1. Accede al panel de administración
2. Crea **Categorías** (ej: Ventas, Inventario, CEDI)
3. Crea **VideoAssets** con la plataforma y ID externo
4. Crea **Topics** vinculando videos con timestamps específicos
5. Agrega **Tags** para búsquedas de errores

### Buscar Contenido

- Por código: `1.13`
- Por tema: `Facturación`
- Por error: `Error 505`

## 🌐 Deployment en Railway

### Quick Start

1. **Push a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/TU_USUARIO/lms-platform.git
   git push -u origin main
   ```

2. **Crear proyecto en Railway:**
   - Ve a https://railway.app
   - New Project → Deploy from GitHub
   - Selecciona tu repositorio
   - Railway detecta automáticamente Django

3. **Agregar PostgreSQL:**
   - En tu proyecto: + New → Database → PostgreSQL
   - Railway configura `DATABASE_URL` automáticamente

4. **Configurar Variables de Entorno:**
   ```bash
   SECRET_KEY=<genera-una-nueva>
   DEBUG=False
   ALLOWED_HOSTS=.up.railway.app,.railway.app
   CSRF_TRUSTED_ORIGINS=https://tu-app.up.railway.app
   ```

5. **Ejecutar Migraciones:**
   ```bash
   railway run python manage.py migrate
   railway run python manage.py createsuperuser
   ```

📖 **Guía Completa:** Ver [deploy_railway.md](deploy_railway.md)

📋 **Checklist:** Ver [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

## 🔒 Seguridad en Producción

✅ **Configurado automáticamente:**
- HTTPS forzado
- Security headers (HSTS, XSS, CSP)
- CSRF protection
- Secure cookies
- SQL injection protection
- XSS protection

---

## 📁 Estructura del Proyecto

```
LMS Manager/
├── core/                   # App principal
│   ├── models.py          # Category, VideoAsset, Topic, Tag, Quiz
│   ├── views.py           # Vistas para home, search, topic, etc.
│   ├── admin.py           # Admin personalizado
│   └── templates/         # Templates con TailwindCSS
├── lms_platform/          # Configuración Django
├── requirements.txt       # Dependencias
├── Procfile              # Railway deployment
└── runtime.txt           # Python version
```

## 🎨 Stack Tecnológico

- **Backend**: Django 5.x
- **Frontend**: Django Templates + TailwindCSS (CDN) + Alpine.js
- **DB**: SQLite (dev) → PostgreSQL (prod)
- **Hosting**: Railway
- **Videos**: YouTube, Vimeo, Cloudflare Stream

## 📝 Licencia

Proyecto privado para uso interno.
