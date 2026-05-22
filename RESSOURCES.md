# Ressources utiles — TP Git Collaboratif

Ce fichier regroupe toutes les ressources pour vous aider pendant et après le TP.
N'hésitez pas à y revenir à tout moment.

---

## Python

**Comprendre les messages d'erreur Python**
Quand Python plante, il affiche un "traceback" : lisez-le de bas en haut. La dernière ligne indique le type d'erreur et le message, les lignes au-dessus montrent le chemin qui y a mené.

- [Types d'erreurs Python — documentation officielle (français)](https://docs.python.org/fr/3/tutorial/errors.html)
- [Comprendre un traceback Python — RealPython (anglais)](https://realpython.com/python-traceback/)

Les erreurs les plus fréquentes que vous rencontrerez :

- `SyntaxError` — le code n'est pas valide syntaxiquement (parenthèse manquante, deux-points oublié…)
- `NameError` — vous utilisez une variable ou une fonction qui n'a pas été définie
- `FileNotFoundError` — le fichier demandé n'existe pas à l'emplacement indiqué
- `ModuleNotFoundError` — un paquet importé n'est pas installé

---

## Flask

Flask est le framework Python utilisé pour créer l'API de ce TP.

- [Documentation officielle Flask (anglais)](https://flask.palletsprojects.com/en/3.0.x/)
- [Tutoriel Flask pour débutants — OpenClassrooms (français)](https://openclassrooms.com/fr/courses/4425066-concevez-un-site-avec-flask)

Commandes utiles :

```bash
# Installer Flask
pip install flask

# Lancer une application Flask
python app.py

# Tester une route depuis le terminal
curl http://localhost:5000/api/logs
```

---

## Node.js et npm

Node.js permet d'exécuter du JavaScript dans le terminal. npm est son gestionnaire de paquets.

- [Documentation officielle Node.js (français)](https://nodejs.org/fr/docs)
- [Guide npm pour débutants (français)](https://docs.npmjs.com/about-npm)

Commandes utiles :

```bash
# Vérifier la version installée
node --version
npm --version

# Installer les dépendances d'un projet (lit package.json)
npm install

# Lancer un script Node
node app.js

# Lancer via le script "start" défini dans package.json
npm start
```

Erreurs fréquentes sous Node.js :

- `Cannot find module 'xxx'` — le paquet n'est pas installé ou son nom est incorrect dans `require()`
- `TypeError: Cannot read properties of undefined` — vous essayez d'accéder à une propriété d'une variable qui vaut `undefined`
- `ECONNREFUSED` — le client ne peut pas se connecter au serveur (serveur non démarré ou mauvais port)

---

## Codes HTTP

Quand Node.js appelle l'API Python, la réponse contient toujours un code HTTP (200, 404, 500…).
Le guide complet avec les explications et les cas concrets de ce TP est dans **[CODES-HTTP.md](./CODES-HTTP.md)**.

---

## Axios

Axios est la bibliothèque Node.js utilisée dans ce TP pour faire des requêtes HTTP vers l'API Python.

- [Documentation Axios — réponse d'une requête](https://axios-http.com/docs/res_schema)

Structure d'une réponse Axios :

```javascript
const response = await axios.get('http://localhost:5000/api/logs');
// Les données retournées par le serveur sont dans :
response.data        // <- c'est ici que se trouve le JSON
response.status      // <- code HTTP (200, 404, 500...)
response.headers     // <- en-têtes HTTP
```

---

## Git et GitHub

**Conventions de nommage des branches**

Dans ce TP, la convention est : `fix/prenom-description`
Exemples : `fix/marie-debug-python`, `fix/kevin-correction-node`

**Messages de commit — Conventional Commits**
Un bon message de commit suit ce format : `type: description courte`

- `fix:` — correction d'un bug
- `feat:` — ajout d'une nouvelle fonctionnalité
- `docs:` — modification de documentation
- `chore:` — tâche de maintenance (mise à jour de dépendances…)

Exemples : `fix: correction du port Flask dans app.py` ou `fix: remplacement axioss par axios`

Ressources Git :
- [Conventional Commits (français)](https://www.conventionalcommits.org/fr/v1.0.0/)
- [Créer une Pull Request sur GitHub (français)](https://docs.github.com/fr/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
- [Comprendre Git — série complète par Grafikart (vidéo français)](https://www.youtube.com/playlist?list=PLjwdMgw5TTLXuY5i7RW0QqGdW0NZntqiP)

---

## Vidéos recommandées (français)

Ces vidéos ont été sélectionnées par votre formateur pour accompagner la formation.

**Git & GitHub — bases**
- [Apprendre GIT en 1 heure (2025)](https://www.youtube.com/watch?v=_WBBiGiCOEA)
- [Formation Git complète — Grafikart](https://www.youtube.com/playlist?list=PLjwdMgw5TTLXuY5i7RW0QqGdW0NZntqiP)
- [Débuter avec Git et GitHub en 30 min](https://www.youtube.com/watch?v=hPfgekYUKgk)

**Gitflow et DevOps**
- [Devenir DevOps — Git et Gitflow — Xavki](https://www.youtube.com/watch?v=ro3ouEyzFzY)
- [Pipeline DevOps — Gitflow en pratique — Xavki](https://www.youtube.com/watch?v=pXWU0iNubk0)
- [Comprendre Git Flow — Grafikart](https://www.youtube.com/watch?v=ZQAQ4HcskAY)

---

## Glossaire rapide

| Terme | Définition simple |
|-------|-------------------|
| API | Service web qui reçoit des requêtes et retourne des données (souvent en JSON) |
| JSON | Format de données texte, lisible par les humains et les machines |
| Framework | Boîte à outils qui facilite le développement (Flask, Express…) |
| Dépendance | Bibliothèque externe dont votre projet a besoin pour fonctionner |
| Port | Numéro qui identifie un service sur une machine (ex: port 5000 pour Flask) |
| Localhost | Désigne votre propre machine (équivalent à 127.0.0.1) |
| Log | Fichier texte enregistrant les événements d'une application |
| Pull Request | Proposition de fusion d'une branche vers une autre, avec revue de code |
| Traceback | Message d'erreur Python qui montre la chaîne d'appels ayant mené à l'erreur |
