# Projet Dashboard

Application dashboard avec un backend Python (FastAPI) et un frontend React (Vite + Tailwind).

## Prérequis
- Python 3.x
- Node.js & npm

## 1. Installation & Lancement du Backend

Le backend gère l'API, la base de données et l'authentification.

### Installation
Ouvrez un terminal dans le dossier dashboard_back :

```bash
cd dashboard_back

python -m venv venv

# Windows :
venv\Scripts\activate
# Mac/Linux :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration (.env)

Créez un fichier .env dans le dossier dashboard_back et ajoutez vos clés :

```txt
SECRET_KEY=...
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:5173

GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback

OPENWEATHER_API_KEY=...

...
```

### Lancer le serveur

Toujours dans dashboard_back :

```Bash
uvicorn app.main:app --reload
```

Le backend sera accessible sur : http://127.0.0.1:8000

La documentation API (Swagger) : http://127.0.0.1:8000/docs

## 2. Installation & Lancement du Frontend

Le frontend est l'interface utilisateur en React.

### Installation

Ouvrez un nouveau terminal dans le dossier dashboard_front :

```Bash
cd dashboard_front

npm install
```

### Lancer le site

Toujours dans dashboard_front :

```Bash
npm run dev
```

Le site sera accessible sur : http://localhost:5173

### Fonctionnalités

Authentification : Inscription/Connexion par Email ou OAuth (Google/GitHub).

Widgets :
- Météo (nécessite une ville).
- Google gmail et calendrier.
- Github Profile et Issues d'un repo.
- Image du jour de la Nasa.
- Image de chat aléatoire.


Mise à jour : Rafraîchissement automatique des données toutes les 30 secondes.