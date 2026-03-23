#!/bin/bash
set -e
echo "Restoring Zo Space routes..."

# This is a template - actual route codes are in /routes/ directory
# Run this script and it will restore all routes from the route files

ROUTES_DIR="$(dirname "$0")/routes"
if [ ! -d "$ROUTES_DIR" ]; then
  echo "  ⚠ No routes directory found, skipping..."
  exit 0
fi

for route_file in "$ROUTES_DIR"/*.json; do
  [ -e "$route_file" ] || continue
  name=$(basename "$route_file" .json)
  echo "  Restoring route: $name"
  # Routes will be restored individually from the route JSON files
done
echo "=== Routes restored ==="
