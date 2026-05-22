# python-api — README Tests

API Flask d'analyse de logs Azure. Ce document explique comment lancer la suite de tests unitaires et ce qu'elle couvre.

---

## Prérequis

- Python 3.8+
- `pip`

---

## Installation

```bash
# Depuis le dossier python-api/
pip install flask pytest
```

---

## Lancer les tests

```bash
# Depuis le dossier python-api/
python -m pytest tests/ -v
```

L'option `-v` affiche le nom de chaque test et son résultat. Sans elle, pytest affiche uniquement un résumé.

Résultat attendu :

```
tests/test_parse_logs.py::test_compte_les_errors                     PASSED
tests/test_parse_logs.py::test_compte_les_warnings                   PASSED
tests/test_parse_logs.py::test_compte_les_infos                      PASSED
tests/test_parse_logs.py::test_errors_contient_les_lignes            PASSED
tests/test_parse_logs.py::test_warnings_contient_les_lignes          PASSED
tests/test_parse_logs.py::test_infos_non_incluses_dans_la_reponse    PASSED
tests/test_parse_logs.py::test_fichier_vide                          PASSED
tests/test_parse_logs.py::test_ignore_les_lignes_vides               PASSED
tests/test_parse_logs.py::test_lignes_sans_niveau_connue_ignorees    PASSED
tests/test_parse_logs.py::test_mix_de_niveaux                        PASSED

10 passed in 0.02s
```

---

## Structure des fichiers de test

```
python-api/
├── app.py
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── conftest.py          ← mock du config.json au chargement du module
    └── test_parse_logs.py   ← 10 tests unitaires sur parse_logs()
```

### Rôle de `conftest.py`

`app.py` ouvre `config.json` dès son import (au niveau module). `conftest.py` intercepte cet appel avant que pytest ne charge les tests, en substituant un faux fichier de configuration en mémoire. Sans lui, pytest échoue au démarrage avec un `FileNotFoundError`.

---

## Ce que les tests couvrent

Les tests ciblent la fonction `parse_logs(filepath)` définie dans `app.py`. Elle lit un fichier de logs ligne par ligne et retourne un dictionnaire comptant et listant les événements par niveau.

### Comptage par niveau (3 tests)

| Test | Ce qu'il vérifie |
|---|---|
| `test_compte_les_errors` | `error_count` est égal au nombre de lignes contenant `ERROR` |
| `test_compte_les_warnings` | `warning_count` est égal au nombre de lignes contenant `WARNING` |
| `test_compte_les_infos` | `info_count` est égal au nombre de lignes contenant `INFO` |

Chaque test passe un fichier temporaire avec uniquement le niveau concerné pour isoler le comportement.

### Contenu des listes retournées (3 tests)

| Test | Ce qu'il vérifie |
|---|---|
| `test_errors_contient_les_lignes` | La liste `errors` contient bien la ligne brute du fichier |
| `test_warnings_contient_les_lignes` | La liste `warnings` contient bien la ligne brute du fichier |
| `test_infos_non_incluses_dans_la_reponse` | La clé `infos` n'existe pas dans le dictionnaire retourné (les infos sont comptées mais non exposées) |

### Cas limites (4 tests)

| Test | Ce qu'il vérifie |
|---|---|
| `test_fichier_vide` | Un fichier vide retourne tous les compteurs à 0 et les listes vides |
| `test_ignore_les_lignes_vides` | Les lignes vides dans le fichier ne faussent pas les compteurs |
| `test_lignes_sans_niveau_connue_ignorees` | Une ligne avec un niveau inconnu (`DEBUG`, `TRACE`…) n'est comptabilisée nulle part |
| `test_mix_de_niveaux` | Un fichier mixte `ERROR` + `WARNING` + `INFO` est correctement ventilé dans les trois compteurs |

---

## Ce qui n'est pas encore testé

- La route HTTP `/api/logs` (test d'intégration Flask avec `app.test_client()`)
- Le comportement si le fichier de logs est absent ou illisible
- Les lignes contenant plusieurs niveaux dans la même ligne (ex. `ERROR WARNING …`)
