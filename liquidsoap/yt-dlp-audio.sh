#!/bin/bash

# Decodifica cookies em Base64 se a variável existir e o arquivo ainda não existir
if [ -n "$YT_COOKIES_BASE64" ] && [ ! -f "/data/cookies.txt" ]; then
    echo "$YT_COOKIES_BASE64" | base64 -d > /data/cookies.txt 2>/dev/null
fi

# O Liquidsoap envia argumentos como -q -f best --no-playlist etc.
# Queremos substituir o "-f best" por "-f bestaudio/best" para garantir qualidade e evitar erros de formato.

final_args=()
skip=0

for arg in "$@"; do
    if [ $skip -eq 1 ]; then
        skip=0
        continue
    fi
    if [ "$arg" == "-f" ]; then
        final_args+=("-f")
        final_args+=("bestaudio/best")
        skip=1
    else
        final_args+=("$arg")
    fi
done

# Se não houver cookies, roda normal. Se houver, usa.
if [ -f "/data/cookies.txt" ]; then
    exec /usr/bin/yt-dlp --cookies /data/cookies.txt "${final_args[@]}"
else
    exec /usr/bin/yt-dlp "${final_args[@]}"
fi
