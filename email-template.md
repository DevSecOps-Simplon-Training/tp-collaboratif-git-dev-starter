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

[Décrivez en 2-3 phrases : quel projet, quels scripts étaient en erreur, dans quel environnement vous avez travaillé]

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

- Bug 1 :
- Bug 2 :
- Bug 3 :
- Bug 4 :
- Bug 5 :
- Bug 6 :
- Bug 7 :
- Bug 8 :

---

**4. Tests de validation**

[Décrivez les commandes que vous avez exécutées pour confirmer que tout fonctionne.
Incluez le résultat attendu vs le résultat obtenu.]

- Commande testée :
- Résultat obtenu :
- Résultat attendu :
- Validation : ✅ / ❌

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
