# Template — Rapport de débogage par email

> Complétez chaque section entre crochets [ ]. Supprimez les instructions en italique avant d'envoyer.

---

**À :** responsable.technique@azuretech.fr
**De :** [Adrien.Sigur@azuretech.fr]
**Objet :** [ "Rapport de corrections de bug  — scripts d'analyse de logs Azure"]
**Date :** [21/05/2026]

---

Bonjour Mr Hoarau Alderich ,

**1. Contexte**

[Décrivez en 2-3 phrases : quel projet, quels scripts étaient en erreur, dans quel environnement vous avez travaillé]

Un projet pour récupérer des logs 

---

**2. Bugs identifiés**

*Projet Python — `python-api/` :*

| # | Fichier | Ligne | Type d'erreur | Description du problème |
|---|---------|-------|---------------|--------------------------|
| 1 | requirement.txt | 2  | faute de frappe | écrit flaskk au lieu de flask |
| 2 | app.py | 18 | oubli deux points | oubli de : pour la fonction parse_logs
| 3 | app.py| 31 | faute de frappe | écrit errors.append(line) au lieu de erreurs.line() |
| 4 | app.py | 46 | variable inexistante | variable log_file en paramètre mais inexistance ajout de l'ouverture du fichier server.log et création de la variable|
| 5 | config.json| 6 | ajout d'un numéro en trop | Flask tourne normalement sur le port 5000 mais il était sur le port 50001 |

*Projet Node.js — `node-client/` :*

| # | Fichier | Ligne | Type d'erreur | Description du problème |
|---|---------|-------|---------------|--------------------------|
| 1 | app.js| 12| faute de frappe| axioss au lieu de axios|
| 2 | app.js| 21 | mauvais paramètre | response.body au lieu de response.data |
| 3 | package.json| |oubli de dépendance | oubli d'installation de axios avec npm|

---

**3. Corrections apportées**

[Pour chaque bug, expliquez en une phrase ce que vous avez changé ET pourquoi c'est correct.]

- Bug 1 : Faute d'orthographe sur l'importation de la librairie flaskk au lieu de flask 
- Bug 2 : Oubli d'un : pour la fonction parse_logs dans le fichier app.py
- Bug 3 : faute de frappe écrit errors.append a la place de erreurs.append
- Bug 4 : oubli d'ouvrir le fichier server.log et de crée la variable log_file
- Bug 5 : Mauvais port flask 50001 au lieu du port 5000
- Bug 6 : Mauvais nom du module axioss au lieu de axios
- Bug 7 : Mauvaise propriété accés des données avec responce.data non response.body
- Bug 8 : Install axios

---

**4. Tests de validation**

[Décrivez les commandes que vous avez exécutées pour confirmer que tout fonctionne.
Incluez le résultat attendu vs le résultat obtenu.]

BACKEND-PYTHON

- Commande testée : python ./app.py
- Résultat obtenu :

 {
  "error_count": 5,
  "errors": [
    "2024-01-15 08:02:45 ERROR Failed to connect to Azure Storage: connection timeout",
    "2024-01-15 08:05:33 ERROR Authentication failed for service account: deploy_svc",
    "2024-01-15 08:07:42 ERROR Database query timeout after 30s on table: audit_logs",
    "2024-01-15 08:09:00 ERROR Max retries exceeded - Azure Storage service unavailable",
    "2024-01-15 08:12:45 ERROR Backup failed: insufficient permissions on /var/backup/azure"
  ],
  "info_count": 10,
  "warning_count": 4,
  "warnings": [
    "2024-01-15 08:01:22 WARNING High memory usage detected: 78%",
    "2024-01-15 08:06:15 WARNING CPU usage spike detected: 92%",
    "2024-01-15 08:10:15 WARNING Disk space below threshold: 15% remaining on /dev/sda1",
    "2024-01-15 08:16:30 WARNING SSL certificate expires in 14 days for api.azuretech.fr"
  ]
 }

- Résultat attendu :

{
  "error_count": 5,
  "errors": ["..."],
  "info_count": 10,
  "warning_count": 4,
  "warnings": ["..."]
}
- Validation : ✅ 

FRONT-END JAVASCRIPT 

Commande testée : node ./app.js

- Résultat obtenu :
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

- Résultat attendu :

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

- Validation ✅ 


---

**5. Lien vers la Pull Request**

https://github.com/DevSecOps-Simplon-Training/tp-collaboratif-git-dev-starter/compare/fix/Adrien-debug-python-node?expand=1

---

**6. Recommandations**

[Proposez 1 ou 2 bonnes pratiques à adopter pour éviter ce type de bug à l'avenir.]

- Faire attention au mélange français anglais 
- bien regarder si l'ont n'oublie pas un : 

---

Cordialement,

[Adrien Sigur]
Développeur DevSecOps — Promotion Azure, Simplon
[votre.email@azuretech.fr]
