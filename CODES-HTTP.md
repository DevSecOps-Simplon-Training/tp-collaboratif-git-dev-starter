# Les codes HTTP — Guide pratique DevOps

Quand votre client Node.js appelle l'API Python, les deux programmes communiquent via HTTP.
Chaque réponse contient un **code à 3 chiffres** qui indique si la requête a réussi ou échoué.

Le premier chiffre indique la catégorie :
- **2xx** — Succès
- **4xx** — Erreur due au client (mauvaise requête, mauvaise URL, pas autorisé…)
- **5xx** — Erreur due au serveur (le code a planté, la base de données est inaccessible…)

---

## 2xx — Succès

### 200 OK
La requête a réussi. C'est la réponse attendue quand tout fonctionne.

```
GET /api/logs → 200 OK
{ "error_count": 5, "warning_count": 4 ... }
```

Dans ce TP, c'est le code que retourne Flask quand les logs sont analysés sans erreur.

### 201 Created
La ressource a été créée avec succès. Utilisé en réponse à une requête POST qui crée un objet (un utilisateur, un ticket, un déploiement…). Vous ne le verrez pas dans ce TP, mais vous le croiserez souvent dans des APIs Azure.

### 204 No Content
La requête a réussi mais le serveur ne retourne rien. Courant pour les requêtes de suppression (DELETE).

---

## 4xx — Erreur côté client

Ces erreurs signifient que **vous avez fait quelque chose d'incorrect** dans votre requête.

### 400 Bad Request
La requête est malformée — paramètre manquant, format incorrect, JSON invalide.

```
Exemple : vous envoyez un JSON avec une virgule en trop
→ 400 Bad Request : "invalid JSON body"
```

### 401 Unauthorized
Vous n'êtes pas authentifié. Le serveur vous demande de vous identifier avant d'accéder à cette ressource.

```
Exemple : appel à une API Azure sans token d'authentification
→ 401 Unauthorized : "Missing or invalid Bearer token"
```

### 403 Forbidden
Vous êtes authentifié, mais vous n'avez pas les droits pour cette action. Contrairement au 401, s'identifier à nouveau ne changera rien.

```
Exemple : un compte de service sans les permissions RBAC Azure nécessaires
→ 403 Forbidden : "Insufficient permissions on resource group"
```

> En DevSecOps, 401 et 403 sont des codes à surveiller de près dans les logs : une accumulation peut signaler une tentative d'intrusion.

### 404 Not Found
La ressource demandée n'existe pas à cette URL.

```
Exemple : curl http://localhost:5000/api/log  (sans 's')
→ 404 Not Found
```

C'est une erreur fréquente quand on tape mal une route Flask. Vérifiez l'URL et le décorateur `@app.route()` dans le code.

### 405 Method Not Allowed
Vous utilisez la mauvaise méthode HTTP (GET, POST, PUT, DELETE…).

```
Exemple : envoyer un POST sur une route qui n'accepte que GET
→ 405 Method Not Allowed
```

### 422 Unprocessable Entity
La requête est bien formée mais les données envoyées sont sémantiquement incorrectes.

```
Exemple : envoyer un champ "age" avec la valeur "bonjour" au lieu d'un nombre
→ 422 Unprocessable Entity
```

---

## 5xx — Erreur côté serveur

Ces erreurs signifient que **le serveur a rencontré un problème**. Ce n'est pas de votre faute en tant que client — c'est le code serveur qui a planté.

### 500 Internal Server Error
Le serveur a rencontré une erreur inattendue. C'est le code générique quand une exception Python non gérée survient dans Flask.

```
Exemple : votre app.py a un bug Python non corrigé
→ 500 Internal Server Error
```

Dans ce TP, si vous voyez un 500, cela signifie que l'API Flask tourne mais qu'elle plante au moment de traiter la requête. Lisez les logs dans le terminal où Python s'exécute — l'erreur Python y sera affichée.

### 502 Bad Gateway
Un serveur intermédiaire (proxy, load balancer) n'a pas pu obtenir de réponse valide du serveur en amont.

```
Exemple courant : votre conteneur Docker ou pod Kubernetes a planté,
mais le load balancer Azure est toujours actif
→ 502 Bad Gateway
```

### 503 Service Unavailable
Le serveur est temporairement indisponible — surchargé ou en cours de maintenance.

```
Exemple : Azure App Service redémarre après un déploiement
→ 503 Service Unavailable (pendant quelques secondes)
```

### 504 Gateway Timeout
Le serveur intermédiaire n'a pas reçu de réponse du serveur en amont dans le temps imparti.

```
Exemple : une requête à une base de données Azure SQL prend trop longtemps
→ 504 Gateway Timeout
```

---

## Erreurs de connexion Node.js — avant même le code HTTP

Certaines erreurs surviennent avant qu'une réponse HTTP soit reçue. Vous les verrez dans le terminal Node sous forme de codes d'erreur système.

### ECONNREFUSED
Le serveur n'accepte aucune connexion sur ce port. Cela signifie que le serveur n'est pas démarré, ou que vous utilisez le mauvais port.

```
Error: connect ECONNREFUSED 127.0.0.1:5001
→ L'API Python n'est pas démarrée, ou elle écoute sur un autre port
```

C'est l'erreur que vous obtiendrez dans ce TP si le bug du port (5001 vs 5000) n'est pas corrigé.

### ENOTFOUND
Le nom de domaine ne peut pas être résolu — l'adresse n'existe pas sur le réseau.

```
Error: getaddrinfo ENOTFOUND mon-api.azuretech.fr
→ L'URL est incorrecte ou le service n'est pas déployé
```

### ETIMEDOUT
La connexion a été tentée mais aucune réponse n'est arrivée dans le délai imparti.

```
Error: connect ETIMEDOUT
→ Le serveur existe mais ne répond pas (pare-feu, surcharge, réseau lent)
```

---

## Résumé visuel

```
Requête HTTP
     │
     ├── 2xx ──► Succès            ✅  Tout va bien
     │
     ├── 4xx ──► Erreur client     ⚠️  Vérifiez votre requête (URL, méthode, auth)
     │
     ├── 5xx ──► Erreur serveur    ❌  Le serveur a planté — lisez ses logs
     │
     └── ERR_ ──► Pas de réponse   🔌  Le serveur est inaccessible (port, réseau)
```

---

## Dans Azure, où voir ces codes ?

En production sur Azure, ces codes apparaissent dans plusieurs endroits :

- **Azure Monitor** — tableau de bord des codes HTTP par période
- **Application Insights** — détail requête par requête avec la durée
- **Log Analytics** — requêtes KQL pour filtrer les 5xx ou les 4xx
- **Azure API Management** — gateway qui centralise tous les appels API et leurs codes de retour

Apprendre à lire ces codes maintenant, c'est poser les bases de la surveillance d'infrastructure que vous pratiquerez tout au long de cette formation.
