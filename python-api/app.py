from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Chargement de la configuration partagée (config.json à la racine du projet)
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# -------------------------------------------------------
# Analyse un fichier de logs serveur et retourne
# le nombre d'erreurs, warnings et infos détectés.
# -------------------------------------------------------

# BUG 2 — Il manque un caractère essentiel à la fin de cette ligne
# DEBUG : correction de syntaxe en ajoutant ":"
def parse_logs(filepath):
    erreurs = []
    warnings = []
    infos = []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # BUG 3 — Le nom de la variable utilisée ici ne correspond pas
            #         à celle déclarée plus haut dans cette fonction
            #DEBUG : correction "erreurs"-le nom de la variable déclaré- au lieu de "errors" 
            if "ERROR" in line:
                erreurs.append(line)
            elif "WARNING" in line:
                warnings.append(line)
            elif "INFO" in line:
                infos.append(line)

    return {
        "error_count": len(erreurs),
        "warning_count": len(warnings),
        "info_count": len(infos),
        "errors": erreurs,
        "warnings": warnings
    }


@app.route("/api/logs", methods=["GET"])
def get_logs():
    # BUG 4 — La variable passée en argument n'est définie nulle part
    #         Quel fichier de logs doit-on analyser ?
    # DEBUG : # Lecture du fichier de logs défini dans la configuration partagée "server.log"
    result = parse_logs(config["api"]["log_file"])
    return jsonify(result), 200


if __name__ == "__main__":
    # Le port est chargé depuis config.json
    # BUG 5 — Le port est défini dans config.json — est-il correct ?
    # DEBUG : le port est 5000 au lieu de 50001
    app.run(debug=True, port=config["api"]["port"])
