import pytest
import os
import tempfile
from app import parse_logs

# -------------------------------------------------------
# Fixtures
# -------------------------------------------------------

@pytest.fixture
def log_file(tmp_path):
    """Crée un fichier de log temporaire avec contenu contrôlé."""
    def _make(content):
        f = tmp_path / "test.log"
        f.write_text(content)
        return str(f)
    return _make


# -------------------------------------------------------
# Tests — comptage par niveau
# -------------------------------------------------------

def test_compte_les_errors(log_file):
    f = log_file(
        "2024-01-15 08:02:45 ERROR Failed to connect\n"
        "2024-01-15 08:05:33 ERROR Auth failed\n"
    )
    result = parse_logs(f)
    assert result["error_count"] == 2

def test_compte_les_warnings(log_file):
    f = log_file(
        "2024-01-15 08:01:22 WARNING High memory: 78%\n"
        "2024-01-15 08:06:15 WARNING CPU spike: 92%\n"
        "2024-01-15 08:16:30 WARNING SSL expires soon\n"
    )
    result = parse_logs(f)
    assert result["warning_count"] == 3

def test_compte_les_infos(log_file):
    f = log_file(
        "2024-01-15 08:00:01 INFO Application started\n"
        "2024-01-15 08:03:10 INFO Request processed\n"
    )
    result = parse_logs(f)
    assert result["info_count"] == 2


# -------------------------------------------------------
# Tests — contenu des listes
# -------------------------------------------------------

def test_errors_contient_les_lignes(log_file):
    ligne = "2024-01-15 08:02:45 ERROR Failed to connect"
    f = log_file(ligne + "\n")
    result = parse_logs(f)
    assert ligne in result["errors"]

def test_warnings_contient_les_lignes(log_file):
    ligne = "2024-01-15 08:01:22 WARNING High memory: 78%"
    f = log_file(ligne + "\n")
    result = parse_logs(f)
    assert ligne in result["warnings"]

def test_infos_non_incluses_dans_la_reponse(log_file):
    """Les infos sont comptées mais pas exposées dans la liste."""
    f = log_file("2024-01-15 08:00:01 INFO Application started\n")
    result = parse_logs(f)
    assert "infos" not in result


# -------------------------------------------------------
# Tests — cas limites
# -------------------------------------------------------

def test_fichier_vide(log_file):
    f = log_file("")
    result = parse_logs(f)
    assert result == {"error_count": 0, "warning_count": 0, "info_count": 0,
                      "errors": [], "warnings": []}

def test_ignore_les_lignes_vides(log_file):
    f = log_file("\n\n2024-01-15 08:00:01 INFO App started\n\n")
    result = parse_logs(f)
    assert result["info_count"] == 1

def test_lignes_sans_niveau_connue_ignorees(log_file):
    f = log_file("2024-01-15 08:00:01 DEBUG Something happened\n")
    result = parse_logs(f)
    assert result["error_count"] == 0
    assert result["warning_count"] == 0
    assert result["info_count"] == 0

def test_mix_de_niveaux(log_file):
    f = log_file(
        "2024-01-15 08:00:01 INFO Start\n"
        "2024-01-15 08:01:22 WARNING Memory high\n"
        "2024-01-15 08:02:45 ERROR Crash\n"
    )
    result = parse_logs(f)
    assert result["error_count"] == 1
    assert result["warning_count"] == 1
    assert result["info_count"] == 1
