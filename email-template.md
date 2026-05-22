# Template — Rapport de débogage par email

---

**À :** responsable.technique@azuretech.fr
**De :** melvin.petit31@gmail.com
**Objet :** Rapport de correction — scripts d'analyse de logs Azure
**Date :** 21 mai 2026

---

Bonjour Responsable,

**1. Contexte**

Ce rapport concerne le projet **TP-Git-Collaboratif** (DevSecOps Azure — Simplon), composé de deux parties : une **API Python** (Flask) située dans `python-api/` qui analyse les fichiers de logs serveur, et un **client Node.js** dans `node-client/` qui interroge cette API et affiche un rapport. Les scripts étaient en erreur en environnement local avec des bugs de syntaxe, de configuration et de dépendances.

---

**2. Bugs identifiés**

*Projet Python — `python-api/` :*

1. **requirements.txt (ligne 2)** — Nom de package incorrect
   - Erreur : `flaskk==3.0.0` au lieu de `flask==3.0.0`

2. **app.py (ligne 19)** — Syntaxe
   - Erreur : Manque le caractère `:` à la fin de la définition de fonction `def parse_logs(filepath)`

3. **app.py (ligne 32)** — Variable mal nommée
   - Erreur : Utilisation de `errors.append()` alors que la liste était déclarée sous le nom `erreurs`

4. **app.py (ligne 49)** — Variable non définie
   - Erreur : La variable `log_file` était définie hors de toute fonction, inaccessible dans `get_logs()`

5. **config.json (lignes 5-6)** — Configuration incorrecte
   - Erreur : Port `50001` et host `localhost` ne correspondaient pas à la configuration de l'API

*Projet Node.js — `node-client/` :*

6. **package.json (ligne 10)** — Nom de package incorrect
   - Erreur : `axioss` au lieu de `axios`

7. **app.js (ligne 20)** — Propriété incorrecte
   - Erreur : Utilisation de `response.body` alors qu'axios utilise `response.data`

---

**3. Corrections apportées**

- **Bug 1** : Corrigé `flaskk` → `flask` dans requirements.txt pour installer le bon package Flask
- **Bug 2** : Ajout du `:` manquant à `def parse_logs(filepath):` pour une syntaxe Python valide
- **Bug 3** : Uniformisé l'utilisation de `erreurs` (au lieu de `errors`) pour correspondre à la déclaration de variable
- **Bug 4** : Déplacé `log_file = config["api"]["log_file"]` avant la définition de fonction pour le rendre accessible dans`get_logs()`
- **Bug 5** : Corrigé le port de `50001` à `5000` et l'host de `localhost` à `127.0.0.1` dans config.json pour une compatibilité universelle
- **Bug 6** : Corrigé `axioss` → `axios` dans package.json et dans l'import du code
- **Bug 7** : Remplacé `response.body` par `response.data` conformément à la documentation axios
- **Bug 8** : Exécuté `npm install` pour installer physiquement la dépendance axios dans node_modules

---

**4. Tests de validation**

- **Commande testée** : `cd python-api && python app.py` puis `cd ../node-client && node app.js`
- **Résultat obtenu** : L'API Python démarre sur le port 5000, le client Node.js se connecte avec succès et affiche le rapport d'analyse des logs avec les comptes d'erreurs, avertissements et infos
- **Résultat attendu** : Affichage du rapport complet des logs Azure
- **Validation** : ✅

---

**5. Lien vers la Pull Request**

[À compléter avec l'URL de votre PR GitHub]

---

**6. Recommandations**

- **Vérifier systématiquement les noms des packages** avant de les ajouter aux fichiers de dépendances (requirements.txt, package.json)
- **Utiliser des linters** (pylint pour Python, ESLint pour Node.js) pour détecter les erreurs de syntaxe avant l'exécution
- **Centraliser la configuration** dans config.json et toujours y faire référence plutôt que de dupliquer les valeurs

---

Cordialement,

Melvin Petit
Développeur DevSecOps — Promotion Azure, Simplon
melvin.petit31@gmail.com
