#!/bin/sh

# Arquivo para log de erros
LOG_FILE="/data/yt-dlp-errors.log"

# Decodifica cookies se a variável Base64 existir e o arquivo não
if [ -n "$YT_COOKIES_BASE64" ] && [ ! -f "/data/cookies.txt" ]; then
    printf "%s" "$YT_COOKIES_BASE64" | base64 -d > /data/cookies.txt 2>>$LOG_FILE
fi

# Prepara os argumentos de cookies
COOKIE_ARG=""
if [ -f "/data/cookies.txt" ]; then
    COOKIE_ARG="--cookies /data/cookies.txt"
fi

# Executa o yt-dlp repassando TODOS os argumentos do Liquidsoap ($@)
exec /usr/bin/yt-dlp $COOKIE_ARG "$@" 2>>$LOG_FILE
