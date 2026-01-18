#!/bin/bash
# Docker-based GitBook server script

cd "$(dirname "$0")"

echo "Starting GitBook with Docker..."
echo "Documentation will be available at http://localhost:4000"

# Install GitBook plugins
docker run --rm -v "$PWD:/gitbook" billryan/gitbook gitbook install

# Serve GitBook
docker run --rm -v "$PWD:/gitbook" -p 4000:4000 billryan/gitbook gitbook serve
