#!/bin/sh

# Garante que o Deno está no PATH
export DENO_INSTALL="/root/.deno"
export PATH="$DENO_INSTALL/bin:$PATH"

# Decodifica cookies se a variável Base64 existir
if [ -n "$YT_COOKIES_BASE64" ] && [ ! -f "/data/cookies.txt" ]; then
    printf "%s" "$YT_COOKIES_BASE64" | base64 -d > /data/cookies.txt 2>/dev/null
fi

COOKIES=""
if [ -f "/data/cookies.txt" ]; then
    COOKIES="--cookies /data/cookies.txt"
fi

# Flags seguindo a Wiki do yt-dlp:
# --js-runtimes: Tenta Deno primeiro, depois Node
# --remote-components ejs:github: Baixa os scripts de desafio direto do GitHub
# --no-cache-dir: Evita problemas de escrita em VPS
exec /usr/bin/yt-dlp $COOKIES \
    --js-runtimes "deno,node" \
    --remote-components "ejs:github" \
    --no-cache-dir \
    --no-warnings \
    -f "bestaudio[ext=m4a]/bestaudio/best" \
    "$@"
