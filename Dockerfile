FROM python:3.12-alpine


RUN apt-get update && apt-get upgrade -y && apt-get clean
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

# Collecte les fichiers statiques
RUN python src/manage.py collectstatic --noinput

ENV DJANGO_ENV=production
EXPOSE 8000

# Définir les variables d'env
ENV DJANGO_ENV=development

CMD ["gunicorn", "stellarfinder.wsgi:application", "--chdir", "src", "--bind", "0.0.0.0:8000"]

