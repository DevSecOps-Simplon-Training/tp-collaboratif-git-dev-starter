# Rapport de débogage par email

---

**À :** responsable.technique@azuretech.fr
**De :** [saidi.mohamed.nom@azuretech.fr]
**Objet :** Rapport de correction — scripts d'analyse de logs Azure
**Date :** 21 mai 2026

---

Bonjour,

**1. Contexte**

Dans le cadre du projet NexaCloud, deux scripts critiques avaient des erreurs suite à une mise à jour en production : `python-api/app.py` et `node-client/app.js`. 
J'ai travaillé en local sur Windows avec Python 3.12 et Node.js 24, sur la branche `fix/mohamed-debug-python-node`.

---

**2. Bugs identifiés**

*Projet Python — `python-api/` :*

| # | Fichier | Ligne | Type d'erreur | Description du problème |
|---|---------|-------|---------------|--------------------------|
| 1 | `requirements.txt` | 2 | Nom de paquet incorrect | `flaskk` n'existe pas sur PyPI |
| 2 | `app.py` | 18 | SyntaxError | `:` manquant à la fin de `def parse_logs(filepath)` |
| 3 | `app.py` | ~30 | NameError | Variable `errors` utilisée à la place de `erreurs` dans `parse_logs` |
| 4 | `app.py` | 50 | NameError | Variable `log_file` non définie utilisée à la place de `"server.log"` |
| 5 | `config.json` | — | Mauvaise configuration | Port `50001` au lieu de `5000` |

*Projet Node.js — `node-client/` :*

| # | Fichier | Ligne | Type d'erreur | Description du problème |
|---|---------|-------|---------------|--------------------------|
| 1 | `package.json` | — | Nom de paquet incorrect | `axioss` n'existe pas sur npm |
| 2 | `app.js` | 12 | MODULE_NOT_FOUND | `require('axioss')` — même faute de frappe que dans package.json |
| 3 | `app.js` | 21 | Mauvaise propriété axios | `response.body` n'existe pas dans axios, la bonne propriété est `response.data` |

---

**3. Corrections apportées**

- Bug 1 : `requirements.txt` — corrigé `flaskk==3.0.0` en `flask==3.0.0` car le nom officiel du paquet sur PyPI est `flask`.
- Bug 2 : `app.py` ligne 18 — ajouté `:` en fin de `def parse_logs(filepath):` car toute définition de fonction Python requiert ça.
- Bug 3 : `app.py` — corrigé `errors` en `erreurs` pour correspondre au nom de variable déclaré en début de fonction.
- Bug 4 : `app.py` ligne 50 — remplacé la variable indéfinie `log_file` par la chaîne `"server.log"`, nom réel du fichier de logs dans le dossier.
- Bug 5 : `config.json` — corrigé le port `50001` en `5000`, valeur attendue par l'architecture du projet et par le client Node.
- Bug 6 : `package.json` — corrigé `"axioss"` en `"axios"` car c'est le nom exact du paquet HTTP sur npm.
- Bug 7 : `app.js` ligne 12 — corrigé `require('axioss')` en `require('axios')` pour correspondre au paquet installé.
- Bug 8 : `app.js` ligne 21 — remplacé `response.body` par `response.data` car dans axios, les données de la réponse serveur sont accessibles via `.data` (cf. documentation officielle axios-http.com/docs/res_schema).

---

**4. Tests de validation**

- Commande testée : `curl http://localhost:5000/api/logs`
- Résultat obtenu : JSON avec `error_count: 5`, `warning_count: 4`, `info_count: 10`
- Résultat attendu : identique
- Validation : ✅

- Commande testée : `node app.js`
- Résultat obtenu : rapport complet affiché dans le terminal avec les 5 erreurs et 4 avertissements détaillés
- Résultat attendu : identique
- Validation : ✅

---

**5. Lien vers la Pull Request**

[À insérer après ouverture de la PR sur GitHub — étape 6 du TP]

---

**6. Recommandations**

- Mettre en place un pipeline CI (GitHub Actions) qui installe les dépendances et vérifie la syntaxe à chaque push — cela aurait détecté les bugs `flaskk` et `axioss` immédiatement sans avoir à lancer les scripts manuellement.
- Ne jamais hardcoder les noms de fichiers ou de variables sans les tester : utiliser des variables d'environnement ou un fichier de config versionné et validé pour éviter les incohérences de port ou de chemin.

---

Cordialement,

[Mohamed Saidi]
Développeur DevSecOps — Promotion Azure, Simplon
[saidi.mohamed.nom@azuretech.fr]
