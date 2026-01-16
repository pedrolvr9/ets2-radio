#!/bin/bash
# Remove "-f" e o valor seguinte (que o Liquidsoap envia como "best")
args=()
skip_next=false
for arg in "$@"; do
    if [ "$skip_next" = true ]; then
        skip_next=false
        continue
    fi
    if [ "$arg" = "-f" ]; then
        skip_next=true
        continue
    fi
    args+=("$arg")
done
# Decodifica cookies em Base64 se a variável existir
if [ -n "$YT_COOKIES_BASE64" ]; then
    echo "Decodificando cookies do YouTube..."
    echo "$YT_COOKIES_BASE64" | base64 -d > /data/cookies.txt
fi

# Agora forçamos o nosso formato ideal
if [ -f "/data/cookies.txt" ]; then
    exec /usr/bin/yt-dlp --cookies /data/cookies.txt -f "bestaudio/best" "${args[@]}"
else
    exec /usr/bin/yt-dlp -f "bestaudio/best" "${args[@]}"
fi
