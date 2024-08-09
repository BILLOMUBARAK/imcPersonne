# Dockerfile for Flask application

# Utiliser l'image de base Python 3.9 slim
FROM python:3.9-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires (par exemple, main.py, requirements.txt)
COPY main.py .
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Copier les fichiers HTML et CSS
COPY templates/formulaireQuestion.html ./templates/

# Commande par défaut pour exécuter l'application
CMD ["python", "main.py"]
