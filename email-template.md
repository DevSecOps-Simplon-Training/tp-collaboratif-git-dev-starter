# Template — Rapport de débogage par email

> Complétez chaque section entre crochets [ ]. Supprimez les instructions en italique avant d'envoyer.

---

**À :** responsable.technique@azuretech.fr
**De :** aicha.elouadi@azuretech.fr
**Objet :** Rapport de correction — scripts d'analyse de logs Azure
**Date :** 21/05/2026

---

Bonjour Aldéric,

**1. Contexte**

Le projet Python présentait plusieurs bugs empêchant la communication entre l'API Python Flask et le client Node.js
Tu trouveras ci-dessous le listing de l'ensemble des bugs détéctés. 
---

**2. Bugs identifiés**

*Projet Python — `python-api/` :*

| # | Fichier | Ligne | Type d'erreur | Description du problème |
|---|---------|-------|---------------|--------------------------|
| 1 | app.py  | 18    | Syntaxe/variable non définie| |log_file absent dans get_logs()|
| 2 | app.py  | 31    | Mauvais nom de la variable|errors/erreurs : incoherent|
| 3 | app.py  | 50    | variable non définie| log_file absent dans get_logs()|
| 4 | app.py  | 50    | Fichier introuvable| serveur.log non trouvé|
| 5 | app.py  | 57    | Port incorrect|Port Flask different du client Node|

*Projet Node.js — `node-client/` :*

| # | Fichier | Ligne | Type d'erreur | Description du problème |
|---|---------|-------|---------------|--------------------------|
| 1 |app.js   |12     |dépendance incorrecte |mauvaise version axios |
| 2 |app.js   |12     |module introuvable | axios non installé|
| 3 |app.js   |21     |erreur nom fichier | .body au lieu de .data|

---

**3. Corrections apportées**

[Pour chaque bug, expliquez en une phrase ce que vous avez changé ET pourquoi c'est correct.]

- Bug 1 : correction de la syntaxe
- Bug 2 : correction du nom de la variable 
- Bug 3 : ajout de la variable log_files
- Bug 4 : correction du chemin/fichier serveur.log
- Bug 5 : correction du port Flask dans app.py
- Bug 6 : correction de la dépendance axios
- Bug 7 : installation de la dépendance Node.js avec nom install
- Bug 8 : remplacement de response.body par reponse.data

---

**4. Tests de validation**

[Décrivez les commandes que vous avez exécutées pour confirmer que tout fonctionne.
Incluez le résultat attendu vs le résultat obtenu.]

- Commande testée : 
python app.py
curl http://127.0.0.1:5000/api/logs
node app.js
- Résultat obtenu : le serveur Flask demarre correctement, le client node affiche le rapport d'analyse des logs azure et des erreurs
- Résultat attendu : communication entre Node-client et python-api , et afficher le rapport des logs
- Validation : ✅ 

---

**5. Lien vers la Pull Request**

[Insérez ici l'URL complète de votre PR GitHub]

---

**6. Recommandations**

[Proposez 1 ou 2 bonnes pratiques à adopter pour éviter ce type de bug à l'avenir.]

-
-

---

Cordialement,

[Prénom Nom]
Développeur DevSecOps — Promotion Azure, Simplon
[votre.email@azuretech.fr]
