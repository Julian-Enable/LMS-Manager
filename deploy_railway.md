# 🚀 Guía de Deployment a Railway - LMS Platform

## Paso 1: Preparar el Repositorio Git

```bash
# Inicializar git (si no lo has hecho)
git init

# Agregar todos los archivos
git add .

# Commit inicial
git commit -m "feat: LMS + Knowledge Base platform ready for production"

# Crear repositorio en GitHub
# Ve a https://github.com/new

# Conectar con GitHub
git remote add origin https://github.com/TU_USUARIO/lms-platform.git
git branch -M main
git push -u origin main
```

---

## Paso 2: Crear Cuenta en Railway

1. Ve a https://railway.app
2. Regístrate con GitHub
3. Autoriza Railway a acceder a tus repositorios

---

## Paso 3: Crear Nuevo Proyecto

### 3.1 Desde Railway Dashboard:

1. Click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca y selecciona tu repositorio `lms-platform`
4. Railway automáticamente:
   - ✅ Detecta Python/Django
   - ✅ Lee el `Procfile`
   - ✅ Instala dependencias de `requirements.txt`

### 3.2 Agregar PostgreSQL:

1. En tu proyecto, click **"+ New"**
2. Selecciona **"Database"** → **"PostgreSQL"**
3. Railway automáticamente:
   - ✅ Crea la base de datos
   - ✅ Configura `DATABASE_URL`

---

## Paso 4: Configurar Variables de Entorno

En Railway Dashboard → **"Variables"**:

### Variables Obligatorias:

```bash
# Genera una nueva SECRET_KEY
# Desde tu terminal local, corre:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Luego en Railway:

| Variable | Valor | Ejemplo |
|----------|-------|---------|
| `SECRET_KEY` | *Tu secret key generada* | `django-ins3cur3-x8f9...` |
| `DEBUG` | `False` | `False` |
| `ALLOWED_HOSTS` | *Tu dominio de Railway* | `.up.railway.app,.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | *URLs completas* | `https://tu-app.up.railway.app` |
| `DJANGO_SETTINGS_MODULE` | `lms_platform.settings` | - |

### Variables Opcionales:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `ADMIN_URL` | `panel-admin-secreto/` | URL personalizada del admin |
| `SECURE_SSL_REDIRECT` | `True` | Forzar HTTPS |

> **Nota:** `DATABASE_URL` ya está configurada automáticamente por Railway.

---

## Paso 5: Ejecutar Migraciones

### Opción A: Desde Railway CLI

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Ejecutar migraciones
railway run python manage.py migrate

# Crear superusuario
railway run python manage.py createsuperuser
```

### Opción B: Desde Railway Dashboard

1. Ve a tu servicio → **"Settings"**
2. En **"Deploy"** → **"Custom Start Command"**
3. Temporalmente cambia a:
   ```
   python manage.py migrate && python manage.py createsuperuser && gunicorn lms_platform.wsgi:application
   ```
4. Espera que el deploy termine
5. Restaura el comando original del `Procfile`

---

## Paso 6: Collectstatic (Archivos Estáticos)

Railway ejecuta automáticamente:
```bash
python manage.py collectstatic --noinput
```

Esto está configurado en `railway.json`.

---

## Paso 7: Verificar Deployment

### URLs de tu aplicación:

Railway te da una URL como:
```
https://tu-app-production-XXXX.up.railway.app
```

### Verificar:

1. ✅ **Homepage:** `https://tu-app.up.railway.app/`
2. ✅ **Admin:** `https://tu-app.up.railway.app/admin/`
3. ✅ **Health Check:** Railway verifica `/admin/login/`

---

## Paso 8: Configurar Dominio Personalizado (Opcional)

### Desde Railway:

1. Ve a **"Settings"** → **"Domains"**
2. Click **"Generate Domain"** (Railway te da uno gratis)
3. O agrega tu dominio personalizado:
   - Agrega tu dominio: `lms.tu-empresa.com`
   - Railway te dará registros DNS para configurar
   - Agrega el CNAME en tu proveedor de DNS

### Actualizar Variables:

```bash
# Agregar tu nuevo dominio a ALLOWED_HOSTS
ALLOWED_HOSTS=.up.railway.app,.railway.app,lms.tu-empresa.com

# Actualizar CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS=https://tu-app.up.railway.app,https://lms.tu-empresa.com
```

---

## Paso 9: Monitoreo y Logs

### Ver Logs en Tiempo Real:

```bash
railway logs
```

O desde Railway Dashboard → **"Deployments"** → Click en el deploy → **"View Logs"**

### Métricas:

Railway muestra automáticamente:
- CPU usage
- Memory usage
- Network traffic
- Request count

---

## 🔄 Actualizaciones Continuas

Cada vez que hagas `git push`:

```bash
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main
```

Railway automáticamente:
1. ✅ Detecta el push
2. ✅ Hace build
3. ✅ Ejecuta tests (si los tienes)
4. ✅ Despliega la nueva versión
5. ✅ Rollback automático si falla

---

## 📊 Configuración de Producción Actual

### ✅ Seguridad Activada:

- HTTPS forzado
- Security headers (HSTS, XSS, CSP)
- CSRF protection
- Secure cookies
- Admin URL personalizable

### ✅ Performance:

- Whitenoise para archivos estáticos
- GZip compression
- Template caching
- Static files caching
- 3 workers de Gunicorn

### ✅ Database:

- PostgreSQL (Railway managed)
- Connection pooling
- Backups automáticos

---

## 🆘 Troubleshooting

### Error: "DisallowedHost"

**Solución:** Agrega tu dominio a `ALLOWED_HOSTS`

```bash
ALLOWED_HOSTS=.up.railway.app,tu-dominio.com
```

### Error: "CSRF verification failed"

**Solución:** Agrega a `CSRF_TRUSTED_ORIGINS`

```bash
CSRF_TRUSTED_ORIGINS=https://tu-app.up.railway.app
```

### Error: Archivos estáticos no cargan

**Solución:** Verifica que collectstatic se ejecutó:

```bash
railway run python manage.py collectstatic --noinput
```

### Ver variables de entorno:

```bash
railway variables
```

---

## 📝 Checklist Pre-Deployment

- [ ] `SECRET_KEY` generada y configurada
- [ ] `DEBUG=False` en producción
- [ ] `ALLOWED_HOSTS` configurado
- [ ] `CSRF_TRUSTED_ORIGINS` configurado
- [ ] PostgreSQL conectado
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] `collectstatic` ejecutado
- [ ] Variables de entorno validadas
- [ ] Logs revisados sin errores

---

## 🎯 Costos Estimados

Railway ofrece:
- **Free Tier:** $5 de créditos gratis/mes
- **Hobby Plan:** $5/mes
- **Pro Plan:** $20/mes

Tu app consumirá aproximadamente **$3-5/mes** en el plan Hobby.

---

## 📞 Soporte

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Tu repositorio

---

**¡Tu LMS está listo para producción!** 🚀
