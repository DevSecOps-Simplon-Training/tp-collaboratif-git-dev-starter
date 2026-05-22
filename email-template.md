# Template — Rapport de débogage par email

**À :** responsable.technique@azuretech.fr
**De :** nathan.tesseyre@azuretech.fr
**Objet :** Rapport de correction — scripts Python API et Node client
**Date :** 21/05/2026

---

Bonjour [Prénom du responsable],

## 1. Contexte

Dans le cadre du TP collaboratif Git, j'ai travaillé sur la branche `fix/nathan-debug-python-node`. J'ai identifié et corrigé plusieurs bugs dans les projets `python-api/` et `node-client/`. Les corrections ont été commitées et pushées sur GitHub.

---

## 2. Bugs identifiés

**Projet Python — `python-api/` :**

| # | Fichier | Ligne | Type d'erreur | Description du problème |
|---|---------|-------|---------------|--------------------------|
| 1 | `requirements.txt` | [1] | Typo | Nom du package `flaskk` au lieu de `flask` |
| 2 | `app.py` | [18] | SyntaxError | Deux-points manquant dans un bloc |
| 3 | `app.py` | [18] | Nommage | Variable `erreurs` en français au lieu de `errors` |
| 4 | `app.py` | [45] | Bug | Variable de nom de fichier log non instanciée |
| 5 | `config.json` | [6] | Config | Mauvais port pour l'API |

**Projet Node.js — `node-client/` :**

| # | Fichier | Ligne | Type d'erreur | Description du problème |
|---|---------|-------|---------------|--------------------------|
| 1 | `package.json` | [10] | Typo | Nom de la dépendance axios mal orthographié |
| 2 | `app.js` | [16] | Typo | Import axios mal orthographié |
| 3 | `app.js` | [10] | Convention | Utilisation de `response.body` au lieu de `response.data` |

---

## 3. Corrections apportées

- **Bug 1 :** Corrigé `flaskk` en `flask` dans `requirements.txt` — le nom du package doit correspondre exactement à celui publié sur PyPI.
- **Bug 2 :** Ajouté le deux-points manquant dans `app.py` — Python requiert `:` pour définir les blocs `if`, `def`, `for`, etc.
- **Bug 3 :** Renommé la variable `erreurs` en `errors` dans `app.py` — convention de nommage en anglais pour la cohérence du code.
- **Bug 4 :** Remplacé la variable non instanciée par le nom du fichier log en dur dans `app.py` — évite un `NameError` à l'exécution.
- **Bug 5 :** Mis à jour le port de l'API dans `config.json` — le port configuré ne correspondait pas à celui utilisé par l'application.
- **Bug 6 :** Corrigé le nom de la dépendance axios dans `package.json` — le mauvais nom empêchait l'installation via `npm install`.
- **Bug 7 :** Corrigé la typo dans l'import axios dans `app.js` — un import mal orthographié provoque un `Cannot find module` à l'exécution.
- **Bug 8 :** Remplacé `response.body` par `response.data` dans `app.js` — axios expose la réponse sous `data`, pas `body` (convention de la librairie).

---

## 4. Tests de validation

| Commande testée | Résultat obtenu | Résultat attendu | Validation |
|----------------|-----------------|------------------|------------|
| `pip install -r requirements.txt` | Installation réussie sans erreur | Installation réussie sans erreur | ✅ |
| `npm install` | Installation des dépendances sans erreur | Installation des dépendances sans erreur | ✅ |
| `node app.js` | Rapport d'analyse reçu | Rapport d'analyse reçu | ✅ |

---

## 5. Lien vers la Pull Request

https://github.com/DevSecOps-Simplon-Training/tp-collaboratif-git-dev-starter/pull/1

---

## 6. Recommandations

- Utiliser un `.gitignore` préconfiguré dès l'initialisation du projet (via [gitignore.io](https://www.toptal.com/developers/gitignore) ou `gh repo create`) pour ne pas oublier `node_modules/`, `.venv/`, etc.
- Utiliser un linter (`flake8` pour Python, `eslint` pour Node.js) pour détecter les typos et erreurs de syntaxe avant le commit.

---

Cordialement,

**Nathan Tesseyre**
Développeur DevSecOps — Promotion Azure, Simplon
nathan.tesseyre@azuretech.fr
