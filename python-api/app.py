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
# le nombre d'errors, warnings et infos détectés.
# -------------------------------------------------------

def parse_logs(filepath):
    criticals = []
    errors = []
    warnings = []
    infos = []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "CRITICAL" in line:
                criticals.append(line)
            elif "ERROR" in line:
                errors.append(line)
            elif "WARNING" in line:
                warnings.append(line)
            elif "INFO" in line:
                infos.append(line)

    return {
        "critical_count": len(criticals),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "info_count": len(infos),
        "criticals": criticals,
        "errors": errors,
        "warnings": warnings
    }


@app.route("/api/logs", methods=["GET"])
def get_logs():
    result = parse_logs(config["api"]["log_file"])
    return jsonify(result), 200

@app.route("/api/stats", methods=["GET"])
def get_stats():

    result = parse_logs(config["api"]["log_file"])

    critical_count = result["critical_count"]
    errors_count = result["errors_count"]
    warning_count = result["warning_count"]
    infos_count = result["infos_count"]

    total = critical_count + error_count + warning_count + info_count
    
    return jsonify({
        "critical_count": critical_count,
        "error_count":    error_count,
        "warning_count":  warning_count,
        "info_count":     info_count,
        "total":          total
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=config["api"]["port"])
