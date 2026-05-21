# Gestion des conflits Git — Étape 7

**Durée estimée :** 45 min
**Prérequis :** avoir terminé les étapes 1 à 6 (bugs corrigés, PR ouverte)

---

## Pourquoi les conflits arrivent-ils ?

En équipe, plusieurs développeurs travaillent en parallèle sur les mêmes fichiers.
Quand deux personnes modifient les mêmes lignes d'un fichier sur des branches différentes,
Git ne sait pas quelle version garder — il vous demande de trancher. C'est un **conflit de fusion**.

```
Branche fix/marie          Branche fix/karim
       │                          │
  modifie config.json        modifie config.json
  (même lignes)              (même lignes)
       │                          │
       └──────────┬───────────────┘
                  │
              CONFLIT
          Git ne peut pas
          merger seul
```

Ce n'est pas une erreur — c'est un mécanisme de sécurité. Git refuse d'écraser
le travail de quelqu'un sans votre accord explicite.

---

## Ce qui va se passer dans ce TP

1. Tout le monde a corrigé les bugs et ouvert une PR sur GitHub
2. Le formateur merge **la PR d'une seule personne** vers `main`
3. `main` est maintenant différent de votre branche locale
4. Quand vous essayez de mettre votre branche à jour → **conflit sur `config.json`**
5. Vous résolvez le conflit, poussez à nouveau → votre PR peut être mergée

---

## Étape 7.1 — Préparer le conflit : compléter config.json

Avant que le formateur merge la première PR, chaque apprenant doit
**ajouter son prénom** dans le tableau `"apprenants"` de `config.json`.

Ouvrez `config.json` et modifiez le tableau :

```json
{
  "projet": "TP-Git-Collaboratif",
  "promotion": "DevSecOps Azure — Simplon",
  "apprenants": ["Votre Prénom"],
  "api": {
    "port": 5000,
    "host": "localhost",
    "route": "/api/logs",
    "log_file": "server.log"
  }
}
```

Commitez cette modification :

```bash
git add config.json
git commit -m "chore: ajout prénom dans config.json + correction port"
git push origin fix/prenom-debug-python-node
```

---

## Étape 7.2 — Le formateur merge une PR (signal de départ)

Le formateur annonce quelle PR il merge sur `main`.
À partir de ce moment, `main` contient les corrections de cette personne —
y compris son prénom dans `config.json`.

Votre branche, elle, contient votre prénom.
Les deux versions sont incompatibles sur la même ligne → conflit garanti.

---

## Étape 7.3 — Récupérer les changements de main

```bash
# Récupérer l'état actuel du dépôt distant sans modifier vos fichiers
git fetch origin

# Vérifier la différence entre votre branche et main
git log --oneline origin/main..HEAD
```

---

## Étape 7.4 — Rebaser votre branche sur main

Le **rebase** réapplique vos commits par-dessus les derniers commits de `main`.
C'est la méthode préférée en DevOps car elle produit un historique linéaire et propre.

```bash
git rebase origin/main
```

Git va s'arrêter et afficher un message comme celui-ci :

```
CONFLICT (content): Merge conflict in config.json
error: could not apply abc1234... chore: ajout prénom dans config.json
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
```

---

## Étape 7.5 — Comprendre les marqueurs de conflit

Ouvrez `config.json` dans votre éditeur. Vous verrez quelque chose comme :

```json
{
  "projet": "TP-Git-Collaboratif",
  "promotion": "DevSecOps Azure — Simplon",
<<<<<<< HEAD
  "apprenants": ["Marie"],
=======
  "apprenants": ["Karim"],
>>>>>>> abc1234 (chore: ajout prénom dans config.json + correction port)
  "api": {
    "port": 5000,
```

**Décryptage des marqueurs :**

| Marqueur | Signification |
|----------|---------------|
| `<<<<<<< HEAD` | Début de VOTRE version (celle sur main après rebase) |
| `=======` | Séparateur entre les deux versions |
| `>>>>>>> abc1234` | Fin de VOTRE commit en cours d'application |

> Les deux versions ont corrigé le port à 5000 — c'est cohérent.
> Le seul vrai conflit est sur les prénoms : chacun n'a ajouté que le sien.

---

## Étape 7.6 — Résoudre le conflit

La résolution correcte ici est de **garder les deux prénoms**.
Supprimez les marqueurs et fusionnez manuellement le contenu :

```json
{
  "projet": "TP-Git-Collaboratif",
  "promotion": "DevSecOps Azure — Simplon",
  "apprenants": ["Marie", "Karim"],
  "api": {
    "port": 5000,
    "host": "localhost",
    "route": "/api/logs",
    "log_file": "server.log"
  }
}
```

> Règle d'or : un conflit résolu ne doit contenir aucun marqueur
> (`<<<<<<<`, `=======`, `>>>>>>>`). S'il en reste un, le fichier est invalide.

---

## Étape 7.7 — Valider et continuer le rebase

```bash
# Vérifier que config.json ne contient plus de marqueurs
cat config.json

# Marquer le conflit comme résolu
git add config.json

# Continuer le rebase
git rebase --continue
```

Git vous demandera éventuellement de valider le message de commit (éditeur qui s'ouvre) — vous pouvez le laisser tel quel et fermer.

---

## Étape 7.8 — Pousser la branche mise à jour

Après un rebase, l'historique de votre branche a changé.
Il faut forcer le push — en utilisant `--force-with-lease` qui est plus sûr
que `--force` car il vérifie que personne d'autre n'a pushé entre-temps.

```bash
git push --force-with-lease origin fix/prenom-debug-python-node
```

Votre PR sur GitHub se mettra à jour automatiquement.

---

## Rebase vs Merge — quelle différence ?

Il existe deux façons d'intégrer les changements de `main` dans votre branche :

**`git rebase origin/main`** (recommandé en équipe)
- Réapplique vos commits par-dessus `main`
- Historique linéaire, plus lisible
- Nécessite un `push --force-with-lease`

**`git merge origin/main`** (plus simple à apprendre)
- Crée un commit de fusion supplémentaire
- Historique non-linéaire mais plus sûr pour les débutants
- Push normal possible

```
Avant rebase / merge :

main :    A --- B --- C  (commit de Karim)
                          \
votre branche :            D  (votre commit)

Après REBASE :
main :    A --- B --- C --- D'  (votre commit réappliqué)

Après MERGE :
main :    A --- B --- C ------- M  (commit de merge)
                          \   /
votre branche :            D
```

Pour ce TP, les deux approches sont acceptées.
En entreprise, la convention dépend de l'équipe — demandez toujours avant de pousser.

---

## Commandes de secours

Si vous êtes bloqué et voulez tout annuler :

```bash
# Annuler le rebase en cours et revenir à l'état avant
git rebase --abort

# Voir l'état actuel des fichiers en conflit
git status

# Voir les différences dans un fichier conflictuel
git diff config.json
```

---

## Résumé des commandes

```bash
git fetch origin                          # Récupérer les changements distants
git rebase origin/main                    # Rebaser sur main (peut créer un conflit)
# → éditer les fichiers conflictuels
git add config.json                       # Marquer comme résolu
git rebase --continue                     # Continuer le rebase
git push --force-with-lease origin <branche>  # Pousser la branche mise à jour
```

---

## Bonnes pratiques à retenir

**Faites des petits commits fréquents** — moins de risque de conflits massifs.

**Rebasez régulièrement** — ne laissez pas votre branche diverger trop longtemps de `main`. Plus vous attendez, plus la résolution sera complexe.

**Communiquez** — si vous savez que vous allez modifier un fichier critique partagé, prévenez l'équipe pour éviter de travailler simultanément sur les mêmes lignes.

**Ne forcez jamais sur `main`** — le `push --force` n'est acceptable que sur votre propre branche de travail. Sur `main`, c'est une faute grave en équipe.
