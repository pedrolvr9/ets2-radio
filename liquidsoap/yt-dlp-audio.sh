#!/bin/sh

# Se houver cookies em Base64, decodifica
if [ -n "$YT_COOKIES_BASE64" ] && [ ! -f "/data/cookies.txt" ]; then
    printf "%s" "$YT_COOKIES_BASE64" | base64 -d > /data/cookies.txt 2>/dev/null
fi

# Parâmetros de otimização:
# --no-cache-dir: evita IO lento em VPS
# -f "ba[ext=m4a]/ba/b": pega o áudio m4a que já está pronto no YouTube (não precisa de ffmpeg)
# --no-warnings: evita que o Liquidsoap confunda avisos com erros

COOKIES=""
if [ -f "/data/cookies.txt" ]; then
    COOKIES="--cookies /data/cookies.txt"
fi

exec /usr/bin/yt-dlp $COOKIES --no-cache-dir --no-warnings -f "bestaudio[ext=m4a]/bestaudio/best" "$@"
