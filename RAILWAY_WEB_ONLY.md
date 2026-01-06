# 🌐 Railway Deployment - Sin CLI (Solo Web Browser)

## ✅ Todo Desde el Navegador

No necesitas instalar Railway CLI. Puedes hacer TODA la configuración desde el navegador.

---

## 📋 Paso 1: Verificar que el Deploy Completó

1. Ve a https://railway.app
2. Login con GitHub
3. Abre tu proyecto **LMS-Manager**
4. Verás 2 servicios:
   - **web** (tu app Django)
   - **Postgres** (base de datos)

### Verificar Status del Deploy:

- Click en el servicio **web**
- Ve a la pestaña **"Deployments"**
- El último deploy debe mostrar **"Success"** (verde)

**Si aún muestra error, espera unos minutos** - Railway puede tardar en detectar el nuevo `nixpacks.toml`

---

## 🗄️ Paso 2: Ejecutar Migraciones (Sin CLI)

### Opción 1: Usando Variables Temporales

1. Click en tu servicio **web**
2. Ve a **"Settings"** → **"Deploy"**
3. Busca **"Custom Start Command"**
4. Cambia **temporalmente** el comando a:
   ```
   python manage.py migrate && gunicorn lms_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 3
   ```
5. Click **"Save"**
6. Railway redesplegará automáticamente
7. Espera a que complete (verás en Deployments)
8. **Restaura el comando original:**
   ```
   gunicorn lms_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --threads 2 --timeout 120 --log-file -
   ```

### Opción 2: Agregar una "Tarea" Temporal

1. En tu proyecto, click **"+ New"**
2. Selecciona **"Empty Service"**
3. Configura:
   - **Name:** `migrations`
   - **Source:** Mismo repo que tu app
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python manage.py migrate && python manage.py createsuperuser`
4. Agrega las MISMAS variables de entorno que el servicio `web`:
   - `DATABASE_URL` (debe estar automáticamente)
   - `SECRET_KEY`
   - `DEBUG`
   - etc.
5. Deploy
6. Una vez complete, **elimina este servicio** (ya no lo necesitas)

---

## 👤 Paso 3: Crear Superusuario (Sin CLI)

### Método Interactivo (Más fácil):

1. Ve a tu servicio **web**
2. Click en **"Settings"**
3. En **"Custom Start Command"**, cambia temporalmente a:
   ```bash
   python manage.py createsuperuser --noinput --username admin --email admin@example.com && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u = User.objects.get(username='admin'); u.set_password('Admin123!'); u.save()" && gunicorn lms_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 3
   ```
   
   Esto crea:
   - **Usuario:** `admin`
   - **Email:** `admin@example.com`  
   - **Password:** `Admin123!`

4. Click **"Save"**
5. Espera que redesplegue
6. Restaura el comando original

### O Manualmente desde Django Shell:

1. Servicio web → **"Settings"** → **"Custom Start Command"**
2. Cambia a:
   ```
   python manage.py shell
   ```
3. Deploy
4. En los **logs** verás el shell interactivo
5. Escribe (no funcionará así, mejor usa el método anterior)

**Recomendación:** Usa el Método Interactivo que crea el usuario automáticamente.

---

## 🎨 Paso 4: Collectstatic (Opcional)

El `nixpacks.toml` ya ejecuta `collectstatic` durante el build, así que esto ya debería estar hecho.

Si necesitas ejecutarlo manualmente:

1. Custom Start Command temporal:
   ```
   python manage.py collectstatic --noinput && gunicorn lms_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 3
   ```

---

## 🔍 Paso 5: Verificar tu App

Una vez que todo esté desplegado:

### Obtener tu URL:

1. Click en tu servicio **web**
2. Ve a **"Settings"** → **"Domains"**
3. Verás algo como: `lms-production-xxxx.up.railway.app`
4. Click en **"Generate Domain"** si no tienes uno

### Probar la App:

1. **Homepage:** `https://tu-app.up.railway.app/`
2. **Admin:** `https://tu-app.up.railway.app/admin/`
   - Usuario: `admin`
   - Password: `Admin123!`

---

## 📊 Ver Logs en Tiempo Real

1. Click en tu servicio **web**
2. Ve a **"Deployments"**
3. Click en el último deployment
4. Verás los logs en tiempo real
5. Busca errores si algo falla

---

## 🎯 Resumen: Qué Hacer AHORA

### 1. Verificar Deploy Actual
- ✅ Ve a Railway → LMS-Manager
- ✅ Verifica que el último deploy sea "Success"

### 2. Si es Success, ejecuta migraciones:
- ✅ Custom Start Command temporal con migrate
- ✅ Espera redeploy
- ✅ Restaura comando original

### 3. Crear superusuario:
- ✅ Custom Start Command con createsuperuser
- ✅ Espera redeploy  
- ✅ Restaura comando

### 4. Probar:
- ✅ Abre tu-app.up.railway.app
- ✅ Login en /admin

---

## 🆘 Troubleshooting

### Si el deploy falla:

**Ver logs detallados:**
1. Deployments → Click en el deploy fallido
2. Lee el error en los logs

**Errores comunes:**

**"DisallowedHost":**
- Agrega tu dominio a `ALLOWED_HOSTS` en variables

**"No module named X":**
- Verifica `requirements.txt` esté en el repo

**"Database connection error":**
- Verifica que PostgreSQL esté agregado
- Verifica que `DATABASE_URL` esté en las variables

---

## 📝 Checklist Final

Desde el navegador, sin CLI:

- [ ] Deploy completó exitosamente
- [ ] Migraciones ejecutadas (via Custom Start Command)
- [ ] Superusuario creado (usuario: admin, pass: Admin123!)
- [ ] App accesible en tu URL de Railway
- [ ] Admin funciona (/admin)
- [ ] Puedes agregar contenido

---

**¡Todo se puede hacer desde el navegador Railway!** 🌐

No necesitas CLI en absoluto.
