#!/bin/bash
# setup.sh — Prépare le projet NexaCloud en une commande

set -e

VERT="\033[0;32m"
ROUGE="\033[0;31m"
CYAN="\033[0;36m"
JAUNE="\033[0;33m"
BOLD="\033[1m"
RESET="\033[0m"

info() { echo -e "${CYAN}[INFO]${RESET} $1"; }
ok()   { echo -e "${VERT}[OK]${RESET}   $1"; }
warn() { echo -e "${JAUNE}[WARN]${RESET} $1"; }
err()  { echo -e "${ROUGE}[ERR]${RESET}  $1"; exit 1; }

# ── Bannière (fournie) ────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${CYAN}============================================${RESET}"
echo -e "${BOLD}${CYAN}   SETUP NEXACLOUD — $(date '+%d/%m/%Y %H:%M')${RESET}"
echo -e "${BOLD}${CYAN}============================================${RESET}"
echo ""

# Chargement des variables du .env
export "$(grep -v '^#' .env | xargs)"

# ── 1. Vérification des prérequis ─────────────────────────────────────
info "Vérification des prérequis..."

# TODO: vérifiez que python3, node et npm sont installés
# Si l'une des commandes est absente, appelez err() pour stopper le script
# Indice : command -v python3 &>/dev/null vérifie si python3 existe
# Indice : l'opérateur || execute la commande à droite si celle de gauche échoue

# Cette fonction vérifie si une commande est installée
# Stoppe le script si elle ne l'est pas
verifier_commande() {
    for cmd in "$@"; do
      if ! command -v "$cmd" &>/dev/null; then
          err "Prérequis : $cmd manquant"
      fi
    done
}

verifier_commande "python3" "node" "npm"

ok "Prérequis : Python3, Node.js, npm présents"

# ── 2. Installation des dépendances Python ────────────────────────────
info "Installation des dépendances Python..."

# TODO: vérifiez si le fichier python-api/requirements.txt existe
# Si oui  → lancez pip install -r python-api/requirements.txt --quiet
#            puis affichez ok()
# Si non  → affichez warn() pour prévenir sans bloquer

requirements_file="python-api/requirements.txt"

if [ -f "$requirements_file" ]; then
    pip install -r $requirements_file --quiet
    ok "Requirements installés"
else
    warn "Fichier $requirements_file manquant"
fi

# ── 3. Installation des dépendances Node ─────────────────────────────
info "Installation des dépendances Node..."

# TODO: même logique pour node-client/package.json
# Si le fichier existe → cd node-client && npm install --silent && cd ..
# Indice : en Bash, on peut chaîner des commandes avec &&

package_file="node-client/package.json"

if [ -f "$package_file" ]; then
    cd node-client && npm install --silent && cd ..
    ok "Dépendances node installées"
else
    warn "Fichier $package_file manquant"
fi

# ── 4. Analyse des logs ───────────────────────────────────────────────
info "Analyse des logs..."

# TODO: vérifiez que $LOG existe, puis :
# - comptez les ERROR avec grep -c et stockez dans NB_ERR
# - comptez les CRITICAL avec grep -c et stockez dans NB_CRIT
# - affichez ok() avec les deux compteurs
# - si NB_CRIT > 0, affichez un message d'alerte rouge
#   et listez les lignes CRITICAL avec grep + une boucle while

if [ ! -f "$LOG" ]; then
    err "Fichier $LOG manquant"
fi

NB_ERR=$(grep -c "ERROR" "$LOG") 
NB_CRIT=$(grep -c "CRITICAL" "$LOG")

ok "$NB_ERR errors, $NB_CRIT criticals"

if [ "$NB_CRIT" -gt 0 ]; then
    echo -e "${ROUGE}!!! $NB_CRIT ERREURS CRITIQUES !!! ${RESET}"
    grep "CRITICAL" "$LOG" | while read -r error; do echo "$error"; done
fi

# ── 5. Message de fin (fourni) ────────────────────────────────────────
echo ""
echo -e "${BOLD}${VERT}============================================${RESET}"
echo -e "${BOLD}${VERT}   SETUP TERMINÉ AVEC SUCCÈS              ${RESET}"
echo -e "${BOLD}${VERT}============================================${RESET}"
echo ""
echo "  Lancer l'API Python  : cd python-api && python3 app.py"
echo "  Lancer le client Node: cd node-client && node app.js"
echo ""
