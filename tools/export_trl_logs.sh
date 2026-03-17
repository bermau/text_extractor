#!/usr/bin/env bash


# répertoire des logs
REP_LOG="/mips/glims10/log/trl"

# fichier de sortie
FICHIER_SORTIE="/mips/messages/tempo_bma/tous_les_log.txt"

# aller dans le répertoire
cd "$REP_LOG" || exit 1

# lister récursivement et enregistrer
ls -ltR | grep -v '^d' | grep -v '^total' > "$FICHIER_SORTIE"

echo "Liste sauvegardée dans $FICHIER_SORTIE"