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
# Agora forçamos o nosso formato ideal
exec /usr/bin/yt-dlp -f "bestaudio/best" "${args[@]}"
