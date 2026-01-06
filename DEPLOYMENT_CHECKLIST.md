# LMS + Knowledge Base - Deployment Checklist

## 🚀 Checklist Pre-Deployment

### Configuración Inicial
- [ ] Git inicializado (`git init`)
- [ ] Repositorio en GitHub creado
- [ ] Remote origin configurado
- [ ] `.env` NO está en el repositorio Git

### Variables de Entorno
- [ ] `SECRET_KEY` generada para producción
- [ ] `DEBUG=False` configurado
- [ ] `ALLOWED_HOSTS` con dominio de Railway
- [ ] `CSRF_TRUSTED_ORIGINS` configurado
- [ ] `DATABASE_URL` (automático en Railway)

### Base de Datos
- [ ] Migraciones creadas (`makemigrations`)
- [ ] Sin migraciones pendientes
- [ ] PostgreSQL agregado en Railway

### Archivos Estáticos
- [ ] `collectstatic` ejecutado
- [ ] Whitenoise configurado
- [ ] TailwindCSS CDN funcionando

### Seguridad
- [ ] HTTPS forzado (`SECURE_SSL_REDIRECT=True`)
- [ ] Security headers configurados
- [ ] CSRF protection activo
- [ ] Session cookies secure

### Testing
- [ ] Homepage carga correctamente
- [ ] Admin panel accesible
- [ ] Búsqueda funciona
- [ ] Videos se reproducen
- [ ] Navegación prev/next funciona

### Railway Específico
- [ ] `Procfile` configurado
- [ ] `runtime.txt` con Python 3.11
- [ ] `railway.json` creado
- [ ] Variables de entorno configuradas
- [ ] Release command configurado

### Post-Deployment
- [ ] Ejecutar migraciones en Railway
- [ ] Crear superusuario
- [ ] Verificar logs sin errores
- [ ] Probar funcionalidad completa
- [ ] Configurar dominio custom (opcional)

## 📋 Comandos Rápidos

### Local
```bash
# Verificar configuración
python check_deployment.sh  # Linux/Mac
# O manualmente revisar

# Commit y push
git add .
git commit -m "feat: ready for production deployment"
git push origin main
```

### Railway CLI
```bash
# Login
railway login

# Link proyecto
railway link

# Variables
railway variables

# Migraciones
railway run python manage.py migrate

# Superusuario
railway run python manage.py createsuperuser

# Logs
railway logs
```

## ✅ Verificación Final

Antes de marcar como completado:

1. Abrir URL de Railway
2. Verificar homepage carga
3. Login al admin
4. Crear un Topic de prueba
5. Verificar que el video se reproduce
6. Probar búsqueda
7. Verificar navegación

**URL de Producción:** `https://___________.up.railway.app`

**Status:** 🟡 Pendiente | 🟢 Completado | 🔴 Error

---

*Última actualización: {{ fecha }}*
