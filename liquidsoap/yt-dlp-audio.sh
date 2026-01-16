#!/bin/sh

# Decodifica cookies se a variável existir (Base64)
if [ -n "$YT_COOKIES_BASE64" ] && [ ! -f "/data/cookies.txt" ]; then
    printf "%s" "$YT_COOKIES_BASE64" | base64 -d > /data/cookies.txt 2>/dev/null
fi

# Prepara cookies
COOKIES_ARG=""
if [ -f "/data/cookies.txt" ]; then
    COOKIES_ARG="--cookies /data/cookies.txt"
fi

# Parsing de argumentos para extrair o output path (-o)
TARGET_PATH=""
CLEANED_ARGS=""
SKIP_NEXT=0

for arg in "$@"; do
    if [ $SKIP_NEXT -eq 1 ]; then
        SKIP_NEXT=0
        continue
    fi
    
    # Remove o -f best do Liquidsoap para deixar o Master decidir (Fix issue #13930)
    if [ "$arg" = "-f" ]; then
        SKIP_NEXT=1
        continue
    fi
    
    if [ "$arg" = "-o" ]; then
        IS_O=1
        CLEANED_ARGS="$CLEANED_ARGS \"$arg\""
        continue
    fi
    
    if [ "$IS_O" = "1" ]; then
        TARGET_PATH=$(echo "$arg" | sed "s/'//g; s/\"//g")
        IS_O=0
    fi
    
    CLEANED_ARGS="$CLEANED_ARGS \"$arg\""
done

# Rodamos o yt-dlp MASTER
# Redirecionamos stdout/stderr para /dev/null para não sujar os metadados do Liquidsoap
eval /usr/bin/yt-dlp $COOKIES_ARG \
    --js-runtimes node \
    --no-cache-dir \
    --no-warnings \
    --no-check-certificates \
    --force-overwrites \
    --no-part \
    -f \"bestaudio/best\" \
    $CLEANED_ARGS > /dev/null 2>&1

# Corrigindo o problema de extensão (webm/m4a) que o Master impõe:
if [ -n "$TARGET_PATH" ] && [ ! -f "$TARGET_PATH" ]; then
    # Procura arquivos que comecem com o nome base gerado pelo Liquidsoap
    for f in "$TARGET_PATH"*; do
        if [ -f "$f" ]; then
            mv "$f" "$TARGET_PATH"
            break
        fi
    done
fi
