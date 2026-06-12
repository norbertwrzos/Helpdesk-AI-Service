#!/usr/bin/env bash
# generate_uml.sh — regeneruje pliki PNG dla wszystkich diagramów UML w docs/uml/
#
# Wymagania:
#   - Java 11+ w PATH
#   - plantuml.jar dostępny lokalnie lub w PATH
#
# Użycie:
#   bash scripts/generate_uml.sh [ścieżka_do_plantuml.jar]
#
# Przykład:
#   bash scripts/generate_uml.sh ~/tools/plantuml.jar
#
# Jeśli ścieżka do JAR nie zostanie podana, skrypt sprawdzi zmienną środowiskową
# PLANTUML_JAR lub spróbuje użyć komendy `plantuml` z PATH.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
UML_DIR="$REPO_ROOT/docs/uml"

# Ustal ścieżkę do PlantUML
PLANTUML_JAR="${1:-${PLANTUML_JAR:-}}"

if [ -n "$PLANTUML_JAR" ]; then
  RUN_CMD="java -jar $PLANTUML_JAR"
elif command -v plantuml &>/dev/null; then
  RUN_CMD="plantuml"
else
  echo "Błąd: nie znaleziono plantuml. Podaj ścieżkę do plantuml.jar jako argument lub ustaw zmienną PLANTUML_JAR." >&2
  exit 1
fi

echo "Generowanie plików PNG w: $UML_DIR"
echo "Używam: $RUN_CMD"
echo ""

for puml_file in "$UML_DIR"/*.puml; do
  base="$(basename "$puml_file" .puml)"
  echo "  -> $base.png"
  $RUN_CMD -tpng "$puml_file" -o "$UML_DIR"
done

echo ""
echo "Gotowe. Wygenerowane pliki:"
ls -lh "$UML_DIR"/*.png
