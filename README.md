# 🌌 Stellar Finder (Démo – Projet en cours)

![Status](https://img.shields.io/badge/Status-en%20cours-yellow)
![Backend](https://img.shields.io/badge/Backend-Django-blue)
![Python](https://img.shields.io/badge/Python-3.12-blue)


**Stellar Finder** est une application web développée avec Django, conçue pour aider les astronomes amateurs et les astrophotographes à planifier leurs séances d'observation du ciel.  
Elle combine une carte du ciel interactive, des outils de cadrage optique et des prévisions météorologiques précises pour offrir une préparation optimale à toute session d'observation.

---

## 🚀 Fonctionnalités

### 🪐 Carte du ciel interactive
- Recherche d'objets célestes dans une vaste base de données (étoiles, planètes, etc.)
- Affichage des coordonnées et de la visibilité pour une date et un lieu choisis

### 📸 Planification des observations
- Visualisation du champ de vision selon la focale de l’utilisateur
- Aide à la composition d'image pour l'astrophotographie

### ☁️ Prévisions météorologiques
- Météo actuelle + prévisions sur 7 jours pour un lieu sélectionné
- Informations utiles : visibilité, température, humidité, éphémérides soleil et lune.

---

## 🛠️ Stack technique

- **Backend** : Python / Django
- **Frontend** : HTML / SCSS / JavaScript
- **API Météo** : OpenWeatherMap
- **Carte du ciel** : Aladin Sky Atlas
- **CI/CD** :
  - **GitHub Actions** : pour l'automatisation du build et du déploiement
  - **Docker** : pour la containerisation de l’application
  - **AWS ECR** : pour le stockage des images Docker
  - **AWS Elastic Beanstalk** : pour le déploiement automatisé sur un environnement scalable
  - **OVH** : pour la gestion du nom de domaine

---

## ⚙️ Déploiement et CI/CD (en cours de mise en place)

Le projet inclut une **pipeline CI/CD automatisée** visant à déployer l'application sur AWS via Docker et GitHub Actions.

**Docker** est utilisé pour assurer que l’application fonctionne de manière identique sur toutes les machines de développement et de production, en simplifiant le déploiement sur AWS.


### 🔄 Processus actuel :
1. **GitHub Actions** est configuré pour :
   - Créer une **image Docker** de l'application chaque fois qu'un commit est poussé.
   - Pousser l'image Docker sur **AWS Elastic Container Registry (ECR)**.
2. **AWS Elastic Beanstalk** reçoit l’image Docker et déploie l’application sur un environnement scalable.
3. Le site sera accessible via un **nom de domaine personnalisé** : stellarfinder.ovh

### 📅 Status :
- La pipeline CI/CD est en cours de finalisation et sera pleinement fonctionnelle prochainement.



