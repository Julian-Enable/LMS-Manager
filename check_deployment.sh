#!/bin/bash
# Script de verificación pre-deployment
# Ejecuta este script antes de hacer deploy para asegurar que todo está configurado

echo "🔍 Verificando configuración de producción..."

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de errores
ERRORS=0

# 1. Verificar archivos requeridos
echo -e "\n📁 Verificando archivos requeridos..."
required_files=("requirements.txt" "Procfile" "runtime.txt" "manage.py" ".gitignore")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file existe"
    else
        echo -e "${RED}✗${NC} $file NO EXISTE"
        ((ERRORS++))
    fi
done

# 2. Verificar que .env no esté en el repo
echo -e "\n🔒 Verificando seguridad..."
if [ -f ".env" ]; then
    if git ls-files --error-unmatch .env > /dev/null 2>&1; then
        echo -e "${RED}✗${NC} ¡PELIGRO! .env está en el repositorio Git"
        echo -e "   Ejecuta: git rm --cached .env"
        ((ERRORS++))
    else
        echo -e "${GREEN}✓${NC} .env no está en Git"
    fi
else
    echo -e "${YELLOW}⚠${NC} .env no existe (OK para producción)"
fi

# 3. Verificar SECRET_KEY en .env.example
echo -e "\n🔑 Verificando SECRET_KEY..."
if grep -q "CHANGE_THIS" .env.production.example 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} Recuerda cambiar SECRET_KEY en producción"
else
    echo -e "${GREEN}✓${NC} .env.production.example OK"
fi

# 4. Verificar dependencias Python
echo -e "\n📦 Verificando dependencias..."
if pip list | grep -q "Django"; then
    echo -e "${GREEN}✓${NC} Django instalado"
else
    echo -e "${RED}✗${NC} Django NO instalado"
    ((ERRORS++))
fi

if pip list | grep -q "gunicorn"; then
    echo -e "${GREEN}✓${NC} Gunicorn instalado"
else
    echo -e "${RED}✗${NC} Gunicorn NO instalado"
    ((ERRORS++))
fi

# 5. Verificar migraciones pendientes
echo -e "\n🗄️  Verificando migraciones..."
python manage.py makemigrations --check --dry-run > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} No hay migraciones pendientes"
else
    echo -e "${YELLOW}⚠${NC} Hay migraciones pendientes. Ejecuta: python manage.py makemigrations"
fi

# 6. Verificar configuración de collectstatic
echo -e "\n📂 Verificando archivos estáticos..."
if [ -d "staticfiles" ]; then
    echo -e "${GREEN}✓${NC} Directorio staticfiles existe"
else
    echo -e "${YELLOW}⚠${NC} Directorio staticfiles no existe (se creará en deploy)"
fi

# 7. Verificar Git
echo -e "\n📝 Verificando Git..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Repositorio Git inicializado"
    
    if git remote -v | grep -q "origin"; then
        echo -e "${GREEN}✓${NC} Remote origin configurado"
    else
        echo -e "${YELLOW}⚠${NC} Remote origin NO configurado"
        echo -e "   Ejecuta: git remote add origin <URL>"
    fi
else
    echo -e "${RED}✗${NC} NO es un repositorio Git"
    echo -e "   Ejecuta: git init"
    ((ERRORS++))
fi

# Resumen
echo -e "\n" "="*50
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Todo listo para deployment!${NC}"
    echo -e "\nPróximos pasos:"
    echo -e "1. git add ."
    echo -e "2. git commit -m 'Ready for production'"
    echo -e "3. git push origin main"
    echo -e "4. Configurar variables en Railway"
    exit 0
else
    echo -e "${RED}❌ Se encontraron $ERRORS errores${NC}"
    echo -e "\nCorrige los errores antes de hacer deployment"
    exit 1
fi
