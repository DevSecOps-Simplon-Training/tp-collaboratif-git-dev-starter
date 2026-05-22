# TP Git — Workflow collaboratif en groupes

**Durée estimée :** 4h30 à 5h  
**Prérequis :** avoir terminé le TP Git Collaboratif (bugs corrigés, PR mergées dans `main`)  
**Effectif :** 3 groupes

---

## Objectifs de la journée

Hier vous avez corrigé des bugs et découvert les conflits Git. Aujourd'hui vous travaillez comme une vraie équipe produit : chaque groupe développe une fonctionnalité différente sur la même base de code, ouvre une Pull Request, se fait relire par les autres, puis tout le monde merge ensemble et résout les conflits en direct.

À la fin de la journée, `main` contient les contributions des trois groupes et l'application fonctionne avec toutes les nouvelles fonctionnalités.

---

## Organisation des groupes

Le formateur annonce la composition des groupes en début de séance.

| Groupe | Responsabilité |
|--------|----------------|
| Groupe 1 | Amélioration de l'affichage terminal + `config.json` |
| Groupe 2 | Nouvel endpoint `/api/health` + `config.json` |
| Groupe 3 | Nouveau niveau de log + endpoint `/api/stats` + affichage |

> Chaque groupe travaille sur des fichiers différents pendant le développement.
> Les conflits arrivent au moment des merges — c'est voulu et prévu.

---

## Étape 0 — Setup initial (tout le monde, 15 min)

Avant de commencer, récupérez l'état actuel de `main` :

```bash
git checkout main
git pull origin main
```

Vérifiez que l'application fonctionne sur votre machine avant de toucher quoi que ce soit :

```bash
# Terminal 1
cd python-api
python app.py

# Terminal 2
cd node-client
node app.js
```

Le rapport doit s'afficher correctement. Si ce n'est pas le cas, prévenez le formateur avant de continuer.

---

## Groupe 1 — Amélioration de l'affichage

**Fichiers à modifier :** `node-client/app.js` et `config.json`  
**Branche à créer :** `feat/groupe1-affichage-terminal`

### Contexte

Le rapport affiché dans le terminal est fonctionnel mais austère. Votre mission : le rendre plus lisible avec des couleurs, ajouter la date de génération, et afficher la version de l'application.

### Étape 1.1 — Créer votre branche

Depuis `main` à jour :

```bash
git checkout -b feat/groupe1-affichage-terminal
```

### Étape 1.2 — Ajouter la version dans config.json

Ouvrez `config.json` et ajoutez le champ `"version"` après `"projet"` :

```json
{
  "projet": "TP-Git-Collaboratif",
  "version": "1.1.0",
  "promotion": "DevSecOps Azure — Simplon",
  "apprenants": ["..."],
  "api": {
    "port": 5000,
    "host": "localhost",
    "route": "/api/logs",
    "log_file": "server.log"
  }
}
```

### Étape 1.3 — Améliorer l'affichage dans app.js

Ouvrez `node-client/app.js`. Remplacez le contenu par la version améliorée ci-dessous.

Les couleurs utilisent des **codes ANSI** — ce sont des séquences de caractères spéciaux que le terminal interprète comme des couleurs. Aucune nouvelle dépendance à installer.

```javascript
const path = require('path');
const axios = require('axios');

const config = require(path.join(__dirname, '..', 'config.json'));
const API_URL = `http://${config.api.host}:${config.api.port}${config.api.route}`;

// Codes de couleur ANSI pour le terminal
const RESET  = '\x1b[0m';
const BOLD   = '\x1b[1m';
const CYAN   = '\x1b[36m';
const RED    = '\x1b[31m';
const YELLOW = '\x1b[33m';
const GREEN  = '\x1b[32m';

async function getLogs() {
    try {
        const response = await axios.get(API_URL);
        const data = response.data;

        // Date et heure de génération du rapport
        const maintenant = new Date().toLocaleString('fr-FR');

        console.log('');
        console.log(BOLD + CYAN + '========================================' + RESET);
        console.log(BOLD + CYAN + '   RAPPORT D\'ANALYSE DES LOGS AZURE    ' + RESET);
        console.log(BOLD + CYAN + '========================================' + RESET);
        console.log(`  Version            : ${config.version || 'N/A'}`);
        console.log(`  Rapport généré le  : ${maintenant}`);
        console.log(BOLD + RED    + `  Erreurs détectées  : ${data.error_count}`   + RESET);
        console.log(BOLD + YELLOW + `  Avertissements     : ${data.warning_count}` + RESET);
        console.log(BOLD + GREEN  + `  Messages info      : ${data.info_count}`    + RESET);
        console.log('');
        console.log(RED + '--- Détail des erreurs ---' + RESET);
        data.errors.forEach(err => console.log(RED + ` > ${err}` + RESET));
        console.log('');
        console.log(YELLOW + '--- Détail des avertissements ---' + RESET);
        data.warnings.forEach(warn => console.log(YELLOW + ` > ${warn}` + RESET));
        console.log(CYAN + '========================================\n' + RESET);

    } catch (error) {
        console.error('Erreur de connexion à l\'API Python :', error.message);
    }
}

getLogs();
```

### Étape 1.4 — Tester en local

```bash
# Terminal 1 — lancer l'API (si elle n'est pas déjà active)
cd python-api && python app.py

# Terminal 2 — tester l'affichage coloré
cd node-client && node app.js
```

Le rapport doit maintenant afficher les erreurs en rouge, les warnings en jaune, les infos en vert, avec la date et la version.

### Étape 1.5 — Commiter et pousser

```bash
git add config.json node-client/app.js
git status   # vérifiez que seuls ces deux fichiers apparaissent
git commit -m "feat: ajout couleurs terminal, date et version dans le rapport"
git push origin feat/groupe1-affichage-terminal
```

### Étape 1.6 — Ouvrir la Pull Request

Sur GitHub :
1. Cliquez sur **Compare & pull request**
2. Titre : `feat: amélioration affichage terminal — groupe 1`
3. Description : expliquez en 3-4 lignes ce que vous avez ajouté et pourquoi
4. Assignez l'expert comme reviewer
5. Soumettez la PR — **ne mergez pas vous-même**

---

## Groupe 2 — Endpoint /api/health

**Fichiers à modifier :** `python-api/app.py` et `config.json`  
**Branche à créer :** `feat/groupe2-health-endpoint`

### Contexte

En production, les systèmes de supervision (comme Azure Monitor) envoient régulièrement des requêtes à un endpoint `/api/health` pour vérifier qu'un service est vivant. Si l'endpoint ne répond pas, une alerte est déclenchée. Votre mission : créer cet endpoint sur l'API Python.

### Étape 2.1 — Créer votre branche

```bash
git checkout -b feat/groupe2-health-endpoint
```

### Étape 2.2 — Ajouter la version dans config.json

Même modification que le Groupe 1 — ajoutez `"version": "1.1.0"` dans `config.json` :

```json
{
  "projet": "TP-Git-Collaboratif",
  "version": "1.1.0",
  ...
}
```

> Vous et le Groupe 1 modifiez la même ligne de `config.json`.
> Ce conflit sera résolu ensemble lors de la cérémonie de merge — c'est normal.

### Étape 2.3 — Ajouter l'endpoint /api/health dans app.py

Ouvrez `python-api/app.py`. Ajoutez cette nouvelle route **après la route `/api/logs` existante** :

```python
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": config["projet"],
        "version": config.get("version", "1.0.0"),
        "port": config["api"]["port"]
    }), 200
```

N'oubliez pas que `config` est déjà chargé en haut du fichier — vous n'avez rien à importer de plus.

### Étape 2.4 — Tester en local

```bash
cd python-api && python app.py
```

Dans un autre terminal :

```bash
curl http://localhost:5000/api/health
```

Résultat attendu :

```json
{
  "port": 5000,
  "service": "TP-Git-Collaboratif",
  "status": "ok",
  "version": "1.1.0"
}
```

### Étape 2.5 — Commiter et pousser

```bash
git add python-api/app.py config.json
git commit -m "feat: ajout endpoint /api/health avec version et statut du service"
git push origin feat/groupe2-health-endpoint
```

### Étape 2.6 — Ouvrir la Pull Request

Sur GitHub :
1. Titre : `feat: endpoint /api/health — groupe 2`
2. Description : expliquez ce qu'est un health check et pourquoi c'est utile en production

---

## Groupe 3 — Logs CRITICAL et endpoint /api/stats

**Fichiers à modifier :** `python-api/app.py`, `python-api/server.log`, `node-client/app.js`  
**Branche à créer :** `feat/groupe3-critical-stats`

### Contexte

L'API actuelle détecte trois niveaux de logs : ERROR, WARNING, INFO. En production Azure, il existe un quatrième niveau : CRITICAL — des erreurs si graves qu'elles nécessitent une intervention immédiate. Votre mission : ajouter ce niveau de détection, créer un endpoint `/api/stats` (compteurs uniquement, sans le détail), et mettre à jour le client Node pour afficher les nouvelles données.

### Étape 3.1 — Créer votre branche

```bash
git checkout -b feat/groupe3-critical-stats
```

### Étape 3.2 — Ajouter des entrées CRITICAL dans server.log

Ouvrez `python-api/server.log` et ajoutez ces lignes à la fin :

```
2024-01-15 08:18:00 CRITICAL Database connection pool exhausted — all 20 connections in use
2024-01-15 08:19:30 CRITICAL Azure Key Vault unreachable — secrets cannot be retrieved
2024-01-15 08:21:00 CRITICAL Disk full on /var/log — logging suspended
```

### Étape 3.3 — Modifier parse_logs() pour détecter CRITICAL

Dans `python-api/app.py`, modifiez la fonction `parse_logs` pour ajouter la détection des lignes CRITICAL :

```python
def parse_logs(filepath):
    erreurs = []
    warnings = []
    infos = []
    critiques = []          # nouveau

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "CRITICAL" in line:
                critiques.append(line)  # nouveau — avant ERROR pour éviter les faux positifs
            elif "ERROR" in line:
                erreurs.append(line)
            elif "WARNING" in line:
                warnings.append(line)
            elif "INFO" in line:
                infos.append(line)

    return {
        "critical_count": len(critiques),   # nouveau
        "error_count": len(erreurs),
        "warning_count": len(warnings),
        "info_count": len(infos),
        "criticals": critiques,             # nouveau
        "errors": erreurs,
        "warnings": warnings
    }
```

> Pourquoi tester CRITICAL avant ERROR ? Parce que la chaîne "CRITICAL" ne contient pas "ERROR", mais si un jour une ligne contient les deux mots, l'ordre de priorité est clair.

### Étape 3.4 — Ajouter l'endpoint /api/stats

Ajoutez cette route dans `app.py` après la route `/api/logs` :

```python
@app.route("/api/stats", methods=["GET"])
def get_stats():
    result = parse_logs(config["api"]["log_file"])
    return jsonify({
        "critical_count": result["critical_count"],
        "error_count":    result["error_count"],
        "warning_count":  result["warning_count"],
        "info_count":     result["info_count"],
        "total":          result["critical_count"] + result["error_count"]
                          + result["warning_count"] + result["info_count"]
    }), 200
```

### Étape 3.5 — Mettre à jour le client Node

Dans `node-client/app.js`, modifiez la fonction `getLogs` pour afficher les CRITICAL :

```javascript
const path = require('path');
const axios = require('axios');

const config = require(path.join(__dirname, '..', 'config.json'));
const API_URL = `http://${config.api.host}:${config.api.port}${config.api.route}`;

async function getLogs() {
    try {
        const response = await axios.get(API_URL);
        const data = response.data;

        console.log('\n========================================');
        console.log('   RAPPORT D\'ANALYSE DES LOGS AZURE    ');
        console.log('========================================');
        if (data.critical_count > 0) {
            console.log(`  !! CRITIQUE !!     : ${data.critical_count}`);
        }
        console.log(`  Erreurs détectées  : ${data.error_count}`);
        console.log(`  Avertissements     : ${data.warning_count}`);
        console.log(`  Messages info      : ${data.info_count}`);

        if (data.criticals && data.criticals.length > 0) {
            console.log('\n--- Incidents critiques ---');
            data.criticals.forEach(c => console.log(` !! ${c}`));
        }
        console.log('\n--- Détail des erreurs ---');
        data.errors.forEach(err => console.log(` > ${err}`));
        console.log('\n--- Détail des avertissements ---');
        data.warnings.forEach(warn => console.log(` > ${warn}`));
        console.log('========================================\n');

    } catch (error) {
        console.error('Erreur de connexion à l\'API Python :', error.message);
    }
}

getLogs();
```

### Étape 3.6 — Tester en local

```bash
# Vérifier le parsing CRITICAL
cd python-api && python app.py

# Dans un autre terminal
curl http://localhost:5000/api/logs    # doit inclure critical_count et criticals
curl http://localhost:5000/api/stats   # doit retourner uniquement les compteurs

cd node-client && node app.js          # doit afficher les incidents critiques
```

### Étape 3.7 — Commiter et pousser

```bash
git add python-api/app.py python-api/server.log node-client/app.js
git commit -m "feat: ajout niveau CRITICAL, endpoint /api/stats et affichage client"
git push origin feat/groupe3-critical-stats
```

### Étape 3.8 — Ouvrir la Pull Request

Sur GitHub :
1. Titre : `feat: logs CRITICAL + endpoint /api/stats — groupe 3`
2. Description : expliquez pourquoi le niveau CRITICAL est distinct d'ERROR, et à quoi sert `/api/stats` par rapport à `/api/logs`

---

## Cérémonie de merge (tout le monde, 1h15)

Une fois que les trois PRs sont ouvertes et reviewées, la cérémonie commence.
**Tout le monde regarde** — chaque groupe présente son travail avant que l'expert merge.

### Merge 1 — Groupe 1 (15 min)

Un membre du Groupe 1 vient au tableau (ou partage son écran) et explique en 2 minutes :
- Ce que vous avez ajouté et pourquoi
- Comment fonctionnent les codes ANSI

L'expert approuve et merge la PR. Pas de conflit à ce stade — c'est le premier merge.

Tout le monde récupère le nouveau `main` :

```bash
git checkout main
git pull origin main
```

### Merge 2 — Groupe 2 (25 min)

Un membre du Groupe 2 explique :
- Ce qu'est un health check et son rôle en production
- Ce que retourne votre endpoint

L'expert tente le merge. **Un conflit apparaît sur `config.json`** — les deux groupes ont ajouté `"version": "1.1.0"` au même endroit.

Un membre du Groupe 1 et un membre du Groupe 2 résolvent le conflit ensemble :

```bash
git checkout feat/groupe2-health-endpoint
git rebase origin/main
# → conflit sur config.json
```

Le conflit ressemblera à ceci :

```
<<<<<<< HEAD
  "version": "1.1.0",
=======
  "version": "1.1.0",
>>>>>>> feat/groupe2-health-endpoint
```

Les deux groupes ont écrit exactement la même valeur — la résolution est simple : garder une seule ligne, supprimer les marqueurs.

```bash
git add config.json
git rebase --continue
git push --force-with-lease origin feat/groupe2-health-endpoint
```

L'expert merge. Tout le monde récupère `main` :

```bash
git checkout main
git pull origin main
```

### Merge 3 — Groupe 3 (35 min)

Un membre du Groupe 3 explique :
- Ce qu'est le niveau CRITICAL et pourquoi avant ERROR dans le parsing
- La différence entre `/api/logs` et `/api/stats`

L'expert tente le merge. **Deux conflits apparaissent :**
- `app.py` — modifié par le Groupe 2 (health) et le Groupe 3 (CRITICAL + stats)
- `app.js` — modifié par le Groupe 1 (couleurs) et le Groupe 3 (affichage CRITICAL)

**Résolution du conflit sur app.py** — un membre du Groupe 2 et un membre du Groupe 3 ensemble :

```bash
git checkout feat/groupe3-critical-stats
git rebase origin/main
```

La résolution consiste à garder les deux modifications : la route `/api/health` du Groupe 2 ET les modifications de `parse_logs()` + la route `/api/stats` du Groupe 3.

**Résolution du conflit sur app.js** — un membre du Groupe 1 et un membre du Groupe 3 ensemble :

La résolution consiste à garder les couleurs ANSI du Groupe 1 ET l'affichage des CRITICAL du Groupe 3. Ce conflit est plus délicat — lisez attentivement les deux versions avant de trancher.

```bash
git add python-api/app.py node-client/app.js
git rebase --continue
git push --force-with-lease origin feat/groupe3-critical-stats
```

L'expert merge. `main` contient maintenant les trois contributions.

---

## Test final (tout le monde, 15 min)

Tout le monde récupère le `main` final et teste l'application complète :

```bash
git checkout main
git pull origin main

# Terminal 1
cd python-api && python app.py

# Terminal 2 — tester les trois endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/stats
curl http://localhost:5000/api/logs

# Terminal 3 — rapport complet
cd node-client && node app.js
```

**Résultat attendu :**

- `/api/health` retourne `{"status": "ok", "version": "1.1.0", ...}`
- `/api/stats` retourne les 4 compteurs dont `critical_count: 3`
- Le rapport terminal affiche les couleurs, la date, la version et les incidents critiques

Si quelque chose ne fonctionne pas, c'est le groupe responsable du fichier concerné qui débogue — avec l'aide des autres.

---

## Critères d'évaluation

| Critère | Points |
|---------|--------|
| Branche nommée correctement | 1 pt |
| Fonctionnalité développée et testée en local | 4 pts |
| Message de commit conventionnel et descriptif | 2 pts |
| PR ouverte avec description compréhensible | 2 pts |
| Participation active à la revue de code d'un autre groupe | 2 pts |
| Conflit résolu sans perte de fonctionnalité | 3 pts |
| Capacité à expliquer son code lors de la cérémonie | 3 pts |
| Test final réussi sur `main` | 3 pts |
| **Total** | **20 pts** |
