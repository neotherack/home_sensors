#!/bin/bash
set -e
read -s -p "Password de admin de Grafana: " PASS
echo

# Borrar SA anterior si existe
curl -sk -X DELETE "https://grafana.franvallejo.es/api/serviceaccounts/2" -u "admin:$PASS"

# Crear SA nuevo con Editor (permisos API mínimos)
SA=$(curl -sk -X POST -H "Content-Type: application/json" \
  -d '{"name":"home_sensors_readonly","role":"Editor"}' \
  "https://grafana.franvallejo.es/api/serviceaccounts" \
  -u "admin:$PASS")
SA_ID=$(echo "$SA" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])" 2>/dev/null)

# Crear token
curl -sk -X POST "https://grafana.franvallejo.es/api/serviceaccounts/$SA_ID/tokens" \
  -H "Content-Type: application/json" \
  -d '{"name":"api-token"}' \
  -u "admin:$PASS"

unset PASS
