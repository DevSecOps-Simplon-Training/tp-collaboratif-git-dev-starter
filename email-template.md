# Template — Rapport de débogage par email

> Complétez chaque section entre crochets [ ]. Supprimez les instructions en italique avant d'envoyer.

---

**À :** responsable.technique@azuretech.fr
**De :** leith.zniber@azuretech.fr
**Objet :** [À compléter — soyez précis et professionnel, ex: "Rapport de correction — scripts d'analyse de logs Azure"]
**Date :** 21/05/2029

---

Bonjour responsable.technique,

**1. Contexte**

Pour la partie de rapports des logs il y avait quelques bugs sur l'API python et le client Node qui affiche le dit rapport, pour info j'utilise ces versions sur mon environement : Python 3.14.5, node v24.15.0, npm 11.12.1 .
Les bugs sont à présent résolus

---

**2. Bugs identifiés**

*Projet Python — `python-api/` :*

| # | Fichier | Ligne | Type d'erreur | Description du problème |
|---|---------|-------|---------------|--------------------------|
| 1 |requirements.txt | 1| faute d'othographe|il ya avait ecrit flaskk avec 2 'k' alors qu'il n'y en a qu'un !!!!!! c'est 'flask' mais c'est pas grave ça arrive les erreurs d'inattention  |
| 2 | app.py | 19 | syntaxe | il manquait les ':' à la fin du def, le dev code sur notepad ?? normalement l'IDE montre l'erreur ici |
| 3 | app.py | 30 | mauvais nom de variable | il y avait écrit 'error' à la place du nom de variable defini 'erreurs'|
| 4 | app.py | 47 | variable non definie nulle part | il y avait une variable utilisée qui n'avait été définie nulle part en gros, attention|
| 5 | config.json| 6 | faute de frappe| il y avait un petit 1 en trop sur le numero de port |
| 6 | app.py| 37 | erreur de type| si la list 'erreurs' reste vide python la considere de type Nonetype ne peut pas appliquer len() dessus |

*Projet Node.js — `node-client/` :*

| # | Fichier | Ligne | Type d'erreur | Description du problème |
|---|---------|-------|---------------|--------------------------|
| 1 | package.json | 10 | faute d'orthographe | encore ?? la derniere lettre ecrite deux fois comme pour le requirement.txt de python, ça fait beaucoup là non ?|
| 2 | app.js | 10 | faute d'orthographe | pareil |
| 3 | app.js | 16 | mauvais objet| l'objet 'body' existe pas sur 'answer' dans axios, l'equivalent c'est 'data' |

---

**3. Corrections apportées**

[Pour chaque bug, expliquez en une phrase ce que vous avez changé ET pourquoi c'est correct.]

- Bug 1 : corrigé la faute d'orthographe (enlever un 'k')
- Bug 2 : corrigé la syntaxe (ajouté un ':' à la fin de la ligne)
- Bug 3 : corrigé le nom de la variable (remplacé 'error' par 'erreurs')
- Bug 4 : ajouté la definition de la variable manquante ('log_file = "./server.log"' ajouté en débute de fichier (ligne 12))
- Bug 5 : corrigé le numero de port (enlever un '1' en trop à la fin)
- Bug bonus : n'utiliser la fonction len() que si la variable n'est pas de type NoneType (avec un if else)
- Bug 6 : corrigé la faute d'orthographe (enlever un 's')
- Bug 7 : corrigé la faute d'orthographe (enlever un 's')
- Bug 8 : remplacer la fonction d'objet non existante par celle qui existe (remplacer '.body' par '.data')

---

**4. Tests de validation**

[Décrivez les commandes que vous avez exécutées pour confirmer que tout fonctionne.
Incluez le résultat attendu vs le résultat obtenu.]

- Commande testée : ```python app.py``` ```curl http://localhost:5000/api/logs``` ```node app.js```
- Résultat obtenu : tout marche (j'ai un peu la flemme de faire les copier coller)
- Résultat attendu : tout marche
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

Leith Zniber
Développeur DevSecOps — Promotion Azure, Simplon
[votre.email@azuretech.fr]
