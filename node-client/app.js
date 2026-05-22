const path = require('path');
const axios = require('axios');
const { clear } = require('console');

const config = require(path.join(__dirname, '..', 'config.json'));
const API_URL = `http://${config.api.host}:${config.api.port}${config.api.route}`;

/*
 * This script retrieves log summaries from a Python API and prints
 * a colored, human-readable Azure log analysis report to the terminal.
 * It fetches counts for errors/warnings/info and lists detailed messages,
 * highlighting important patterns (errors in red, warnings in yellow).
 */

// Codes de couleur ANSI pour le terminal
const RESET  = '\x1b[0m';
const BOLD   = '\x1b[1m';
const CYAN   = '\x1b[36m';
const RED    = '\x1b[31m';
const YELLOW = '\x1b[33m';
const GREEN  = '\x1b[32m';
const WHITE  = '\x1b[37m'

console.clear()

const RED_WORDS = /Azure Storage|Authentication failed|Database|timeout|insufficient permissions/i;
const LOG_LIST  = /Azure Storage|Authentication failed|Database|timeout|insufficient permissions|High memory|CPU usage|Disk space|SSL certificate/gi;

function highlightLog(text) {
    return text.replace(LOG_LIST, match =>
        RED_WORDS.test(match) ? RED + match + RESET : YELLOW + match + RESET
    );
}

async function getLogs() {
    try {
        const response = await axios.get(API_URL);
        const data = response.data;

        const now = new Date().toLocaleString('fr-FR');


        console.log('');
        console.log(BOLD + CYAN + '┌──────────────────────────────────────┐' + RESET);
        console.log(BOLD + CYAN + '│' + WHITE + '       AZURE LOG ANALYSIS REPORT      ' + CYAN + '│' + RESET);
        console.log(BOLD + CYAN + '├──────────────────────────────────────┘' + RESET);
        console.log(CYAN + '│  Version            : ' + WHITE + `${config.version || 'N/A'}` + RESET);
        console.log(CYAN + '│  Report generated at: ' + WHITE + `${now}` + RESET);
        console.log(CYAN + '│' + RESET);
        console.log(CYAN + '│  Errors detected    : ' + WHITE + `${data.error_count}`   + RESET);
        console.log(CYAN + '│  Warnings           : ' + WHITE + `${data.warning_count}` + RESET);
        console.log(CYAN + '│  Info messages      : ' + WHITE + `${data.info_count}`    + RESET);
        console.log(CYAN + '│' + RESET);
        console.log(CYAN + '│' + RED + '  --- Error details ---' + RESET);
        console.log(CYAN + '│' + RESET);
        data.errors.forEach(err => console.log(CYAN + '│  ' + RED + '> ' + RESET + highlightLog(err)));
        console.log(CYAN + '│' + RESET);
        console.log(CYAN + '│' + YELLOW + '  --- Warning details ---' + RESET);
        console.log(CYAN + '│' + RESET);
        data.warnings.forEach(warn => console.log(CYAN + '│  ' + YELLOW + '> ' + RESET + highlightLog(warn)));
        console.log(CYAN + '│' + RESET);

    } catch (error) {
        console.error('Failed to connect to Python API:', error.message);
    }
}

getLogs();