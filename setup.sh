#!/bin/bash
mkdir -p ~/.streamlit/

echo "\
[general]
email = \"boyeelhadjiabdou@gmail.com\"
" > ~/.streamlit/credentials.toml

echo "\
[server]
headless = true
enableCORS=false
port = \$PORT
" > ~/.streamlit/config.toml
