# Template — Rapport de débogage par email

---

**À :** jean.technique@azuretech.fr
**De :** malik.cherfi@azuretech.fr
**Objet :** Rapport de correction — scripts d'analyse de logs Azure
**Date :** 21/05/2026

---

Bonjour Jean,

**1. Contexte**

J'ai travaillé avec flask nodejs et vscode, les erreurs se trouvé principalement côté serveur dans le fichier app.py et côté client dans le fichier app.js.
Le projet à pour but de prendre un fichier en paramètre, de dispatcher les messages dans différente clé en fonction du type du message ( côté de serveur ) et de l'envoyé au client pour qu'il affiche les logs.

---

**2. Bugs identifiés**

_Projet Python — `python-api/` :_

| #   | Fichier          | Ligne | Type d'erreur      | Description du problème                  |
| --- | ---------------- | ----- | ------------------ | ---------------------------------------- |
| 1   | requirements.txt | 2     | SyntaxError        | Erreur de syntaxe dans le mot flask      |
| 2   | app.py           | 18    | SyntaxError        | Il manque ":" pour définir la fonction   |
| 3   | app.py           | 54    | VariableNotDefined | La variable log_file n'était pas définie |
| 4   | app.py           | 35    | SyntaxError        | Le nom de la variable n'était pas le bon |
| 5   | config.json      | 6     | SyntaxError        | Le numéro du port n'était pas le bon     |

_Projet Node.js — `node-client/` :_

| #   | Fichier      | Ligne | Type d'erreur | Description du problème                              |
| --- | ------------ | ----- | ------------- | ---------------------------------------------------- |
| 1   | package.json | 10    | SyntaxError   | Erreur de syntaxe dans le nom de la dépendance axios |
| 2   | app.js       | 12,16 | SyntaxError   | Erreur de syntaxe dans le nom de la variable axios   |
| 3   | app.js       | 21    | SyntaxError   | Erreur dans le nom de l'objet                        |

---

**3. Corrections apportées**

- Bug 1 : J'ai enlevé le 's' en trop dans flassk car le nom correct est flask
- Bug 2 : J'ai ajouté ':' car pour définir une fonction dans Python il faut ajouter les ':'
- Bug 3 : J'ai importé le fichier server.log avec le nom de variable log_file
- Bug 4 : J'ai corrigé le nom de la variable pour qu'elle corresponde au tableau 'erreurs'
- Bug 5 : J'ai corrigé le numéro du port pour m'accorder à la doc ( 50001 => 5000 )
- Bug 6 : J'ai corrigé le nom la dépendance axios
- Bug 7 : J'ai corrigé le nom de la variable et de l'import de la dépendance axios ( nom de la variable doit être le même que la dépendance pour plus de lisibilité )
- Bug 8 : J'ai corrigé le nom de l'objet, le serveur renvoi un objet dans lequel il y a une clé appelé data et non body

---

**4. Tests de validation**

[Décrivez les commandes que vous avez exécutées pour confirmer que tout fonctionne.
Incluez le résultat attendu vs le résultat obtenu.]

- Commande testée : python3 app.py && node app.js
- Résultat obtenu :

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

--- Detail des avertissements ---
 > 2024-01-15 08:01:22 WARNING High memory usage detected: 78%
 > 2024-01-15 08:06:15 WARNING CPU usage spike detected: 92%
 > 2024-01-15 08:10:15 WARNING Disk space below threshold: 15% remaining on /dev/sda1
 > 2024-01-15 08:16:30 WARNING SSL certificate expires in 14 days for api.azuretech.fr
========================================
```

- Résultat attendu :

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

- Validation : ✅

---

**5. Lien vers la Pull Request**

https://github.com/DevSecOps-Simplon-Training/tp-collaboratif-git-dev-starter/pull/2

---

**6. Recommandations**

Toute les erreurs sont du à de la négligence, il est fortement conseillé de configurer eslint pour détecter le genre d'erreur quand une variable n'est pas défini ou qu'une fonction n'est pas bien écrite.

-
- ***

Cordialement,

Malik Cherfi
Développeur DevSecOps — Promotion Azure, Simplon
malik.cherfi@azuretech.fr
