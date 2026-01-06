# 🎯 Próximos Pasos - Railway Deployment

## ✅ Código Ya en GitHub
**Repositorio:** https://github.com/Julian-Enable/LMS-Manager

---

## 🚂 Pasos para Railway (5 minutos)

### 1. Crear Cuenta en Railway
1. Ve a: https://railway.app
2. Click en **"Login with GitHub"**
3. Autoriza Railway

### 2. Crear Nuevo Proyecto
1. En Railway Dashboard, click **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca y selecciona: **"Julian-Enable/LMS-Manager"**
4. Railway automáticamente:
   - ✅ Detecta que es Django
   - ✅ Lee el `Procfile`
   - ✅ Instala dependencias

### 3. Agregar PostgreSQL
1. En tu proyecto, click **"+ New"**
2. Selecciona **"Database"** → **"PostgreSQL"**
3. Railway automáticamente configura `DATABASE_URL`

### 4. Configurar Variables de Entorno

Click en tu servicio → **"Variables"** → Agregar estas 4 variables:

#### 1. SECRET_KEY
Genera una nueva:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copia el resultado y pégalo en Railway.

#### 2. DEBUG
```
False
```

#### 3. ALLOWED_HOSTS
```
.up.railway.app,.railway.app
```

#### 4. CSRF_TRUSTED_ORIGINS
Espera a que Railway te dé tu URL (ej: `lms-production-xxxx.up.railway.app`)

Luego agrega:
```
https://lms-production-xxxx.up.railway.app
```

### 5. Deploy Automático
Railway automáticamente:
1. ✅ Hace build del proyecto
2. ✅ Ejecuta migraciones (`release` command en Procfile)
3. ✅ Ejecuta `collectstatic`
4. ✅ Inicia gunicorn
5. ✅ Te da una URL pública

**Tiempo estimado:** 2-3 minutos

### 6. Crear Superusuario

Una vez desplegado, desde tu terminal:

```powershell
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link al proyecto
railway link

# Crear superusuario
railway run python manage.py createsuperuser
```

O alternativamente:
1. Ve a Railway → tu servicio → **"Settings"**
2. En **"Deploy"** → **"Custom Start Command"**
3. Cambia temporalmente a: `python manage.py createsuperuser`
4. Espera que termine
5. Restaura el comando del Procfile

---

## 🎉 ¡Listo!

Tu URL será algo como:
```
https://lms-production-xxxx.up.railway.app
```

Verifica:
- ✅ Homepage: `https://tu-app.up.railway.app/`
- ✅ Admin: `https://tu-app.up.railway.app/admin/`

---

## 🔄 Actualizaciones Futuras

Cada vez que hagas cambios:
```powershell
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main
```

Railway automáticamente detecta el push y redespliega. 🚀

---

## 📊 Monitoreo

En Railway Dashboard verás:
- CPU usage
- Memory usage
- Request logs
- Deployment history

---

## 💰 Costos

Railway te da **$5 de créditos gratis** para empezar.
Plan Hobby: **$5/mes** (más que suficiente para esta app)

---

## 🆘 Troubleshooting

### Si ves "DisallowedHost":
Agrega tu dominio a `ALLOWED_HOSTS` en las variables de Railway.

### Si no cargan los archivos estáticos:
Railway ejecuta automáticamente `collectstatic` en el `release` command del Procfile.

### Ver logs en tiempo real:
```powershell
railway logs
```

---

**¡Tu LMS está listo para deployment profesional!** 🚀
