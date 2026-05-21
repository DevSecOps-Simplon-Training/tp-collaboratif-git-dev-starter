from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Chargement de la configuration partagée (config.json à la racine du projet)
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# -------------------------------------------------------
# Analyse un fichier de logs serveur et retourne
# le nombre d'errors, warnings et infos détectés.
# -------------------------------------------------------

def parse_logs(filepath):
    errors = []
    warnings = []
    infos = []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "ERROR" in line:
                errors.append(line)
            elif "WARNING" in line:
                warnings.append(line)
            elif "INFO" in line:
                infos.append(line)

    return {
        "error_count": len(errors),
        "warning_count": len(warnings),
        "info_count": len(infos),
        "errors": errors,
        "warnings": warnings
    }

# Clé API attendue — en production, cette valeur viendrait
# d'une variable d'environnement Azure Key Vault, jamais en dur dans le code
API_KEY = "devsecops-simplon-2024"

def verifier_cle_api():
    cle = request.headers.get("X-API-Key")
    if cle != API_KEY:
        return jsonify({"erreur": "Clé API invalide ou manquante"}), 401
    return None

@app.route("/api/logs", methods=["GET"])
def get_logs():
    erreur = verifier_cle_api()
    if erreur:
        return erreur
    result = parse_logs("server.log")
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True, port=config["api"]["port"])
