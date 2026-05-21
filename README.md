# TP Git Collaboratif — Débogage Full-Stack Python + Node.js

**Durée estimée :** 3h30
**Niveau :** Intermédiaire
**Effectif :** 12 apprenants

> Les ressources et explications complémentaires sont disponibles dans le fichier **[RESSOURCES.md](./RESSOURCES.md)**.

---

## Avant de commencer — Comprendre les outils utilisés

Si vous êtes en reconversion et que certains termes vous sont nouveaux, pas de panique. Voici l'essentiel à savoir avant de démarrer.

**Python** est un langage de programmation très utilisé en DevOps pour automatiser des tâches : analyser des fichiers, interagir avec des APIs, lancer des scripts de déploiement. Dans ce TP, un script Python est chargé de lire un fichier de logs et d'en extraire les informations importantes.

**Flask** est un framework Python qui permet de créer très simplement une API web. Concrètement, Flask transforme votre script Python en un petit serveur web que l'on peut interroger via une URL, comme on interrogerait un site. Ici, Flask va exposer les résultats de l'analyse des logs à l'adresse `http://localhost:5000/api/logs`.

**Node.js** est un environnement qui permet d'exécuter du JavaScript en dehors d'un navigateur, directement dans le terminal. Il est très utilisé pour créer des outils en ligne de commande, des serveurs web ou, comme dans ce TP, des scripts qui consomment des APIs.

**npm** (Node Package Manager) est le gestionnaire de paquets de Node.js. Il permet d'installer des bibliothèques tierces listées dans un fichier `package.json`, exactement comme `pip` installe les dépendances Python listées dans `requirements.txt`.

**Une API REST** est un service web qui reçoit des requêtes HTTP et retourne des données, généralement au format JSON. Dans ce TP, Python joue le rôle du serveur (il fournit les données) et Node.js joue le rôle du client (il demande les données et les affiche).

**Les logs serveur** sont des fichiers texte que les applications génèrent automatiquement pour enregistrer ce qui se passe : démarrages, erreurs, avertissements, requêtes reçues… En DevOps, analyser ces logs est une tâche quotidienne pour surveiller l'état d'une infrastructure.

---

## Contexte du TP

Vous êtes développeur·se DevOps chez **NexaCloud**.

Suite à une mise à jour en production, deux scripts critiques tombent en erreur :

- `python-api/app.py` — une API Flask qui lit les logs du serveur Azure et retourne une analyse JSON
- `node-client/app.js` — un client Node.js qui interroge cette API et affiche un rapport dans le terminal

Ces deux scripts **communiquent ensemble** : Node appelle Python via HTTP.
Aucun des deux ne fonctionnera correctement tant que tous les bugs ne sont pas corrigés.

Votre responsable technique vous demande de :
1. Cloner le dépôt sur votre machine
2. Reproduire les erreurs en exécutant les scripts
3. Identifier et corriger les bugs (8 au total)
4. Pousser vos corrections via une Pull Request
5. Envoyer un email de rapport à votre responsable

---

## Architecture du projet

```
[Fichier de logs Azure]
      server.log
          |
          v
  python-api/app.py          <- API Flask (port 5000)
  (lit les logs, compte       <- Lance avec : python app.py
   les ERROR / WARNING / INFO)
          |
          | HTTP GET /api/logs
          v
  node-client/app.js         <- Client Node.js
  (affiche le rapport         <- Lance avec : node app.js
   dans le terminal)
```

---

## Structure du dépôt

```
TP-Git-Collaboratif/
├── README.md                  <- Ce fichier
├── config.json                <- Configuration partagée Python + Node (contient un bug)
├── email-template.md          <- Template pour votre email de rapport
├── CONFLITS.md                <- Guide de résolution des conflits Git (étape 7)
├── CORRECTION_FORMATEUR.md    <- Réservé au formateur
├── python-api/
│   ├── app.py                 <- API Flask (contient des bugs)
│   ├── requirements.txt       <- Dépendances Python (contient un bug)
│   └── server.log             <- Fichier de logs Azure (ne pas modifier)
└── node-client/
    ├── app.js                 <- Client Node.js (contient des bugs)
    └── package.json           <- Dépendances Node (contient un bug)
```

---

## Prérequis

Avant de commencer, vérifiez que vous avez installé :

```bash
python --version    # Python 3.8 ou supérieur
node --version      # Node.js 18 ou supérieur
npm --version       # npm 9 ou supérieur
git --version       # Git 2.x
```

---

## Étapes du TP

### Étape 1 — Setup Git (15 min)

**1.1 — Cloner le dépôt**

```bash
git clone <URL_DU_REPO_FOURNIE_PAR_LE_FORMATEUR>
cd TP-Git-Collaboratif
```

**1.2 — Créer votre branche de travail**

Respectez impérativement cette convention de nommage :

```bash
git checkout -b fix/prenom-debug-python-node
# Exemple : git checkout -b fix/alderic-debug-python-node
```

**1.3 — Vérifier que votre branche est active**

```bash
git branch
# La branche active est précédée d'une étoile (*)
```

---

### Étape 2 — Débogage Python (60 min)

> Consigne : lancez les commandes, lisez attentivement les messages d'erreur,
> corrigez UN bug à la fois, relancez après chaque correction.

**2.1 — Installer les dépendances Python**

Placez-vous dans le dossier `python-api/` :

```bash
cd python-api
pip install -r requirements.txt
```

Si une erreur apparaît ici, lisez le message. Ouvrez `requirements.txt` et cherchez ce qui est incorrect.

**2.2 — Lancer l'API Flask**

```bash
python app.py
```

Chaque message d'erreur vous indique :
- Le **type d'erreur** (SyntaxError, NameError, FileNotFoundError…)
- Le **fichier** concerné
- Le **numéro de ligne** précis

Notez chaque erreur dans le template email au fur et à mesure.

**2.3 — Vérifier que l'API répond correctement**

Une fois tous les bugs Python corrigés, vous devriez voir :

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Testez l'API avec curl (dans un autre terminal) :

```bash
curl http://localhost:5000/api/logs
```

Résultat attendu — un JSON de cette forme :

```json
{
  "error_count": 5,
  "errors": ["..."],
  "info_count": 10,
  "warning_count": 4,
  "warnings": ["..."]
}
```

---

### Étape 3 — Débogage Node.js (50 min)

> Laissez l'API Python en cours d'exécution dans votre premier terminal.
> Ouvrez un second terminal pour cette étape.

**3.1 — Installer les dépendances Node**

```bash
cd node-client
npm install
```

Si npm affiche une erreur ou un avertissement "404 Not Found", examinez `package.json`.
Le nom du paquet dans `dependencies` est-il correct ?

**3.2 — Lancer le client Node**

```bash
node app.js
```

Analysez chaque message d'erreur. Node.js vous indique le type d'erreur et la ligne.
Corrigez un bug à la fois, relancez après chaque correction.

**3.3 — Résultat attendu quand tout fonctionne**

```
========================================
   RAPPORT D'ANALYSE DES LOGS AZURE
========================================
  Erreurs detectees  : 5
  Avertissements     : 4
  Messages info      : 10

--- Detail des erreurs ---
 > 2024-01-15 08:02:45 ERROR Failed to connect to Azure Storage: connection timeout
 > 2024-01-15 08:05:33 ERROR Authentication failed for service account: deploy_svc
 > 2024-01-15 08:07:42 ERROR Database query timeout after 30s on table: audit_logs
 > 2024-01-15 08:09:00 ERROR Max retries exceeded - Azure Storage service unavailable
 > 2024-01-15 08:12:45 ERROR Backup failed: insufficient permissions on /var/backup/azure
========================================
```

---

### Étape 4 — Test de communication complète (20 min)

Vérifiez que les deux projets fonctionnent ensemble :

1. Terminal 1 : `cd python-api && python app.py`
2. Terminal 2 : `cd node-client && node app.js`
3. Le rapport complet doit s'afficher dans le terminal 2

Si Node affiche `Erreur de connexion à l'API Python`, vérifiez que :
- L'API Python est bien démarrée (terminal 1)
- Les ports correspondent entre `app.py` et `app.js`

---

### Étape 5 — Rédiger l'email de rapport (20 min)

Ouvrez le fichier `email-template.md` et complétez chaque section :
- Contexte de l'incident
- Tableau des bugs identifiés (fichier, ligne, type, description)
- Corrections apportées avec justification
- Tests de validation réalisés
- Lien vers votre Pull Request
- Recommandations pour éviter ces bugs à l'avenir

---

### Étape 6 — Pull Request (15 min)

**6.1 — Commiter vos corrections**

```bash
cd ..   # Revenir à la racine du projet
git add .
git status  # Vérifiez les fichiers modifiés
git commit -m "fix: correction des 8 bugs Python et Node - analyse logs Azure"
```

**6.2 — Pousser votre branche**

```bash
git push origin fix/prenom-debug-python-node
```

**6.3 — Ouvrir une Pull Request sur GitHub**

1. Rendez-vous sur le dépôt GitHub
2. Cliquez sur "Compare & pull request"
3. Titre de la PR : `fix: débogage API Python + client Node - <votre prénom>`
4. Description : collez un résumé des bugs corrigés
5. Soumettez la PR

**6.4 — Réviser la PR d'un·e camarade**

Trouvez la PR d'un·e autre apprenant·e et ajoutez au minimum un commentaire constructif.

---

### Étape 7 — Gestion des conflits Git (45 min)

> Cette étape se fait **en groupe**, une fois que tout le monde a ouvert sa PR.
> Le formateur merge la PR d'une première personne sur `main`, puis chacun doit
> mettre sa branche à jour et résoudre le conflit qui en résulte.

Le guide complet pas à pas est dans le fichier **[CONFLITS.md](./CONFLITS.md)**.

En résumé, vous allez :
1. Ajouter votre prénom dans le tableau `"apprenants"` de `config.json`
2. Commiter et pousser cette modification
3. Attendre que le formateur merge une première PR sur `main`
4. Récupérer les changements et rebaser votre branche : `git rebase origin/main`
5. Résoudre le conflit dans `config.json` (garder tous les prénoms + le bon port)
6. Continuer le rebase et forcer le push : `git push --force-with-lease`


---

## Pour aller plus loin — Profils avancés

> Cette section est destinée aux apprenants qui ont terminé les 6 étapes principales avant la fin du TP.
> Les trois défis suivants sont indépendants — vous pouvez les traiter dans l'ordre de votre choix.
> Ils correspondent directement aux modules Azure qui arrivent dans la suite de la formation.

---

### Défi 1 — Conteneuriser les deux services avec Docker

**Objectif :** packager l'API Python et le client Node dans des conteneurs Docker, puis les faire communiquer via Docker Compose. C'est la base du déploiement sur Azure Container Apps.

**Branche à créer :** `feat/prenom-docker`

**1.1 — Créer le Dockerfile pour l'API Python**

Créez le fichier `python-api/Dockerfile` :

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

**1.2 — Créer le Dockerfile pour le client Node**

Créez le fichier `node-client/Dockerfile` :

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

CMD ["node", "app.js"]
```

**1.3 — Créer le fichier docker-compose.yml**

Créez `docker-compose.yml` à la racine du projet :

```yaml
version: '3.8'

services:
  python-api:
    build: ./python-api
    ports:
      - "5000:5000"
    container_name: log-analyser-api

  node-client:
    build: ./node-client
    depends_on:
      - python-api
    container_name: log-analyser-client
```

> Attention : quand Node tourne dans un conteneur, `localhost` ne désigne plus votre machine mais le conteneur lui-même. Il faudra adapter l'URL dans `app.js` pour utiliser le nom du service Docker (`python-api`) à la place de `localhost`. C'est le principe de la communication inter-conteneurs.

**1.4 — Lancer les deux services**

```bash
docker-compose up --build
```

**Résultat attendu :** le rapport des logs s'affiche dans les logs du conteneur `node-client`.

---

### Défi 2 — Ajouter un pipeline CI avec GitHub Actions

**Objectif :** créer un workflow GitHub Actions qui vérifie automatiquement que le code s'installe et démarre sans erreur à chaque push ou Pull Request.

> **CI ou CD ?** Ce pipeline couvre uniquement la partie **CI (Intégration Continue)** : il vérifie que le code est valide. Il tourne entièrement sur les serveurs de GitHub — aucun abonnement Azure n'est nécessaire. La partie **CD (Déploiement Continu)** vers Azure App Service ou Azure Container Apps sera ajoutée dans le module Azure DevOps de la formation, quand vous aurez accès à un abonnement Azure.
>
> Retenez la distinction : **CI = vérifier le code** (GitHub suffit) — **CD = déployer le code** (Azure intervient ici).

**Branche à créer :** `feat/prenom-github-actions`

**2.1 — Créer la structure du workflow**

```bash
mkdir -p .github/workflows
```

Créez le fichier `.github/workflows/ci.yml` :

```yaml
name: CI — Vérification API Python

on:
  push:
    branches: [ main, 'fix/**', 'feat/**' ]
  pull_request:
    branches: [ main ]

jobs:
  test-python-api:
    runs-on: ubuntu-latest

    steps:
      - name: Récupérer le code
        uses: actions/checkout@v4

      - name: Installer Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Installer les dépendances
        run: |
          cd python-api
          pip install -r requirements.txt

      - name: Vérifier que Flask démarre sans erreur
        run: |
          cd python-api
          timeout 5 python app.py || true
          echo "Vérification terminée"

  test-node-client:
    runs-on: ubuntu-latest

    steps:
      - name: Récupérer le code
        uses: actions/checkout@v4

      - name: Installer Node.js 18
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Installer les dépendances npm
        run: |
          cd node-client
          npm install

      - name: Vérifier la syntaxe JavaScript
        run: |
          cd node-client
          node --check app.js
          echo "Syntaxe JavaScript valide"
```

**2.2 — Pousser et observer**

```bash
git add .github/
git commit -m "ci: ajout pipeline GitHub Actions vérification Python et Node"
git push origin feat/prenom-github-actions
```

Rendez-vous dans l'onglet **Actions** de votre dépôt GitHub pour observer le pipeline s'exécuter en temps réel.

**Questions de réflexion :**

1. Que se passe-t-il si vous pushez volontairement un bug dans `app.py` (par exemple, remettez `flaskk` dans `requirements.txt`) ? Le pipeline détecte-t-il l'erreur ?
2. Comment configurer GitHub pour qu'une PR ne puisse pas être fusionnée si le pipeline échoue ? (Indice : Settings → Branches → Branch protection rules)
3. Quelle étape faudrait-il ajouter à ce pipeline pour déployer automatiquement l'API sur Azure App Service ? Que vous manque-t-il actuellement pour pouvoir le faire ? (Cette question sera répondue dans le module Azure DevOps de la formation.)

---

### Défi 3 — Sécuriser la communication entre les deux services

**Objectif :** ajouter une couche de sécurité entre Node et Flask — une clé API simple en header HTTP. Sans cette clé, l'API refuse de répondre. C'est l'introduction au principe d'authentification entre microservices, fondamental en DevSecOps.

**Branche à créer :** `feat/prenom-securite-api`

**3.1 — Côté Python : vérifier la clé API dans chaque requête**

Modifiez `python-api/app.py` pour ajouter la vérification :

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Clé API attendue — en production, cette valeur viendrait
# d'une variable d'environnement Azure Key Vault, jamais en dur dans le code
API_KEY = "devsecops-simplon-2024"

def verifier_cle_api():
    cle = request.headers.get("X-API-Key")
    if cle != API_KEY:
        return jsonify({"erreur": "Clé API invalide ou manquante"}), 401
    return None

@app.route("/api/logs", methods=["GET"])
def get_logs():
    erreur = verifier_cle_api()
    if erreur:
        return erreur
    result = parse_logs("server.log")
    return jsonify(result), 200
```

**3.2 — Côté Node : envoyer la clé dans les headers**

Modifiez `node-client/app.js` pour inclure la clé dans chaque requête :

```javascript
const response = await axios.get(API_URL, {
    headers: {
        'X-API-Key': 'devsecops-simplon-2024'
    }
});
```

**3.3 — Tester que la sécurité fonctionne**

Testez d'abord sans la clé :

```bash
curl http://localhost:5000/api/logs
# Attendu → 401 Unauthorized
```

Puis avec la bonne clé :

```bash
curl http://localhost:5000/api/logs -H "X-API-Key: devsecops-simplon-2024"
# Attendu → 200 OK avec les données JSON
```

**3.4 — Réflexion sécurité (à noter dans votre commit)**

Ajoutez un commentaire dans votre code qui répond à cette question : pourquoi ne faut-il **jamais** stocker une clé API directement dans le code source ? Quelle alternative Azure propose-t-elle pour stocker ces secrets de façon sécurisée ?

> Indice : cherchez "Azure Key Vault" dans la documentation Azure.


---

## Ressources utiles

Toutes les ressources (documentation, vidéos, guides) sont regroupées dans le fichier **[RESSOURCES.md](./RESSOURCES.md)**.
