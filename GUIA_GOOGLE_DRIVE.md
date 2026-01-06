# 📹 Guía: Cómo Usar Videos de Google Drive en el LMS

## 🔑 Paso 1: Obtener el ID del Video de Google Drive

### Opción A: Desde la URL del archivo

Si tienes un video en Drive, la URL se ve así:
```
https://drive.google.com/file/d/1a2B3c4D5e6F7g8H9i0J/view?usp=sharing
```

**El ID del video es:** `1a2B3c4D5e6F7g8H9i0J`

### Opción B: Compartir el video

1. Haz clic derecho en el video en Google Drive
2. Selecciona **"Compartir"**
3. Cambia a **"Cualquier persona con el enlace"**
4. Copia el enlace
5. Extrae el ID entre `/d/` y `/view`

---

## ⚙️ Paso 2: Configurar Permisos del Video

**IMPORTANTE:** El video DEBE estar configurado como:

✅ **"Cualquier persona con el enlace puede ver"**

De lo contrario, el reproductor mostrará un error de permisos.

### Cómo configurar los permisos:

1. Abre Google Drive
2. Haz clic derecho en el video
3. Selecciona **"Compartir"**
4. En **"Acceso general"**, selecciona:
   - **"Cualquier persona con el enlace"**
   - **Rol:** "Lector"
5. Haz clic en **"Listo"**

---

## 📝 Paso 3: Agregar el Video en el Admin

1. Ve a http://127.0.0.1:8000/admin
2. Haz clic en **"Video Assets"** → **"Agregar Video Asset"**

3. Completa los campos:
   - **Título del Video:** Ej: "Gestión de Ventas - Completo"
   - **Plataforma:** Selecciona **"Google Drive"**
   - **ID Externo:** Pega el ID que copiaste (ej: `1a2B3c4D5e6F7g8H9i0J`)
   - **Duración (segundos):** (Opcional) Duración total del video
   - **Descripción:** (Opcional)

4. Haz clic en **"Guardar"**

---

## 🎬 Paso 4: Crear Topics con Timestamps

Ahora puedes crear temas que apunten a momentos específicos del video:

### Ejemplo:

**Video:** "Gestión de Ventas Completo" (ID: 1a2B3c4D5e6F7g8H9i0J)

**Topics:**
1. **Code:** `1.11` | **Título:** "Toma de Pedido" | **Start:** 30s
2. **Code:** `1.12` | **Título:** "Facturación" | **Start:** 945s  (15min 45s)
3. **Code:** `1.13` | **Título:** "Cierre de Caja" | **Start:** 1690s  (28min 10s)

---

## 📌 Ejemplo Completo

### Tu video en Drive:
```
https://drive.google.com/file/d/1a2B3c4D5e6F7g8H9i0J/view?usp=sharing
```

### En el Admin del LMS:

**VideoAsset:**
- **Título:** Gestión de Ventas Completo
- **Plataforma:** Google Drive
- **ID Externo:** `1a2B3c4D5e6F7g8H9i0J`

**Topics:**
| Code | Título | Video | Start (seg) | Start (min:seg) |
|------|--------|-------|-------------|-----------------|
| 1.11 | Toma de Pedido | Gestión de Ventas... | 30 | 00:30 |
| 1.12 | Facturación | Gestión de Ventas... | 945 | 15:45 |
| 1.13 | Cierre | Gestión de Ventas... | 1690 | 28:10 |

---

## ⚠️ Limitación de Google Drive

> **IMPORTANTE:** Google Drive **NO soporta saltos automáticos a timestamps** en videos embebidos.
> 
> Esto significa que aunque especifiques `start_seconds`, el video siempre iniciará desde el principio.

**Recomendación:** Si necesitas saltos automáticos a timestamps, considera:
1. Subir los videos a **YouTube** (gratuito)
2. Usar **Vimeo**
3. Mantener Drive solo para almacenamiento y usar YouTube para reproducción

---

## 🔄 Conversión Rápida seg → min:seg

Para calcular el timestamp en segundos:

**Fórmula:** `(minutos × 60) + segundos`

**Ejemplos:**
- **04:20** → (4 × 60) + 20 = **240 segundos**
- **15:45** → (15 × 60) + 45 = **945 segundos**
- **28:10** → (28 × 60) + 10 = **1690 segundos**

O usa esta calculadora online: https://www.calculateme.com/time/minutes-seconds/to-seconds/

---

## 📞 ¿Necesitas Ayuda?

Si tienes problemas con los videos de Drive:

1. **Verifica que el video sea público** (enlace compartido)
2. **Prueba abriendo el embed directamente:**
   ```
   https://drive.google.com/file/d/TU_ID_AQUI/preview
   ```
3. **Considera usar YouTube** para mejor compatibilidad con timestamps

---

## ✨ Próximos Pasos

Una vez agregados los videos:

1. ✅ Ve a la página principal: http://127.0.0.1:8000
2. ✅ Busca por código, título o tag
3. ✅ Haz clic en un tema para ver el video
4. ✅ Navega entre temas con prev/next
5. ✅ Prueba el Modo Curso para ver todos los temas secuenciales

**¡Listo para comenzar!** 🚀
