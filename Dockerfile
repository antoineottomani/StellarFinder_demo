FROM python:3.13-alpine

# Installer les dépendances système nécessaires
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Définir le dossier de travail
WORKDIR /app

# Copier tout le projet dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Ajoute src au PYTHONPATH pour que Python trouve les modules
ENV PYTHONPATH="/app/src"

# Définir les variables d'environnement
ENV DJANGO_ENV=production
EXPOSE 8000

# Copier le script d'entrée
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Le conteneur démarrera via ce script
ENTRYPOINT ["/entrypoint.sh"]