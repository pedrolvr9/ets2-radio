#!/bin/sh

YTDLP="/usr/bin/yt-dlp"
LOG_FILE="/data/yt-dlp-errors.log"

# Decodifica cookies se a variável Base64 existir e o arquivo não
if [ -n "$YT_COOKIES_BASE64" ] && [ ! -f "/data/cookies.txt" ]; then
    printf "%s" "$YT_COOKIES_BASE64" | base64 -d > /data/cookies.txt 2>>$LOG_FILE
fi

COOKIE_ARG=""
if [ -f "/data/cookies.txt" ]; then
    COOKIE_ARG="--cookies /data/cookies.txt"
fi

# O Liquidsoap envia argumentos como: -q -f best --no-continue --no-playlist -o '...' -- 'URL'
# Precisamos remover o "-f best" para o yt-dlp não reclamar e usar nosso formato ideal.
FINAL_ARGS=""
SKIP=0
for arg in "$@"; do
    if [ $SKIP -eq 1 ]; then SKIP=0; continue; fi
    if [ "$arg" = "-f" ]; then SKIP=1; continue; fi
    # Adiciona o argumento à lista, protegendo espaços
    FINAL_ARGS="$FINAL_ARGS \"$arg\""
done

# Executa com o formato de áudio correto e ignorando erros de SSL que ocorrem em algumas VPS
eval exec $YTDLP $COOKIE_ARG -f \"bestaudio/best\" --no-check-certificates $FINAL_ARGS 2>>$LOG_FILE
