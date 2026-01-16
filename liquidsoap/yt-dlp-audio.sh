#!/bin/sh

# Decodifica cookies se a variável Base64 existir
if [ -n "$YT_COOKIES_BASE64" ] && [ ! -f "/data/cookies.txt" ]; then
    printf "%s" "$YT_COOKIES_BASE64" | base64 -d > /data/cookies.txt 2>/dev/null
fi

COOKIES=""
if [ -f "/data/cookies.txt" ]; then
    COOKIES="--cookies /data/cookies.txt"
fi

# Roda o yt-dlp sem precisar baixar componentes remotos (já estão embutidos)
# Usamos o formato m4a por ser extremamente leve e rápido de processar
exec /usr/bin/yt-dlp $COOKIES \
    --no-cache-dir \
    --no-warnings \
    -f "bestaudio[ext=m4a]/bestaudio/best" \
    "$@"
