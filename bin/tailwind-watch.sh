#!/usr/bin/env bash

cd "$(dirname "$0")/.." || exit 1
tailwindcss -i web/tailwind/input.css --watch \
            -o web/static/css/core.css \
            -c web/tailwind/tailwind.config.js
