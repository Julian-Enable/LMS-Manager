# 🔧 Solución: Error de Deployment en Railway

## ❌ Error Detectado

```
django.db.utils.OperationalError: could not translate host name "host" to address
```

**Causa:** El `release` command en el Procfile intentaba ejecutar migraciones durante el BUILD, pero la base de datos aún no estaba disponible.

---

## ✅ Solución Implementada

### 1. Procfile Actualizado

**ANTES (causaba error):**
```
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

**AHORA (corregido):**
```
web: gunicorn lms_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 3
```

**Razón:** Las migraciones se ejecutarán MANUALMENTE después del primer deploy, cuando la DB esté lista.

---

## 🚀 Pasos para Completar el Deployment

### Paso 1: Verificar PostgreSQL en Railway

1. En Railway Dashboard → Tu proyecto
2. Verifica que tengas **2 servicios:**
   - ✅ `web` (tu app Django)
   - ✅ `PostgreSQL` (base de datos)

**Si NO tienes PostgreSQL:**
- Click **"+ New"**
- **"Database"** → **"PostgreSQL"**
- Railway automáticamente configura `DATABASE_URL`

### Paso 2: Push del Procfile Corregido

```bash
git add Procfile
git commit -m "fix: remove release command from Procfile"
git push origin main
```

Railway redesplegará automáticamente (sin errores esta vez).

### Paso 3: Esperar que el Deploy Complete

En Railway → **Deployments** → Espera a que el status sea **"Success"** (verde)

### Paso 4: Ejecutar Migraciones MANUALMENTE

Una vez que el deploy exitoso:

**Opción A: Railway CLI**
```bash
# Instalar CLI
npm install -g @railway/cli

# Login
railway login

# Link al proyecto
railway link

# Ejecutar migraciones
railway run python manage.py migrate

# Crear superusuario
railway run python manage.py createsuperuser

# Collectstatic
railway run python manage.py collectstatic --noinput
```

**Opción B: Desde Railway Dashboard**
1. Ve a tu servicio `web`
2. Click **"Settings"** → **"Deploy"**
3. En **"Custom Start Command"**, cambia temporalmente a:
   ```
   python manage.py migrate && python manage.py collectstatic --noinput && python manage.py createsuperuser
   ```
4. Espera que termine
5. Restaura el comando original del Procfile

---

## 🔍 Verificar Variables de Entorno

En Railway → tu servicio `web` → **"Variables"**

**Debe tener:**
```
DATABASE_URL=postgresql://... (auto-generada por Railway)
SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=.up.railway.app,.railway.app
CSRF_TRUSTED_ORIGINS=https://tu-app.up.railway.app
```

**IMPORTANTE:** `DATABASE_URL` debe aparecer automáticamente cuando agregues PostgreSQL.

---

## ✅ Checklist de Resolución

- [ ] PostgreSQL agregado al proyecto
- [ ] `DATABASE_URL` aparece en variables
- [ ] Procfile corregido (sin `release` command)
- [ ] `git push` con el Procfile actualizado
- [ ] Deploy completa exitosamente
- [ ] Migraciones ejecutadas manualmente
- [ ] Superusuario creado
- [ ] Collectstatic ejecutado
- [ ] App funcionando en Railway URL

---

## 🎯 Orden Correcto de Ejecución

1. **Railway crea PostgreSQL** → `DATABASE_URL` disponible
2. **Deploy de la app** → Gunicorn inicia
3. **Manualmente:** Ejecutar migraciones
4. **Manualmente:** Crear superusuario
5. **Manualmente:** Collectstatic

---

## 📞 Si Persiste el Error

**Error: "No module named 'decouple'"**
```bash
# Verifica que requirements.txt incluya:
python-decouple
```

**Error: "ALLOWED_HOSTS"**
```bash
# Agrega tu dominio Railway a las variables:
ALLOWED_HOSTS=.up.railway.app,tu-dominio.railway.app
```

**Ver logs en tiempo real:**
```bash
railway logs
```

---

## 🚀 Después de la Corrección

Tu app estará en:
```
https://tu-app-production-XXXX.up.railway.app
```

Admin en:
```
https://tu-app-production-XXXX.up.railway.app/admin
```

---

**¡Ahora debería funcionar sin problemas!** 🎉
