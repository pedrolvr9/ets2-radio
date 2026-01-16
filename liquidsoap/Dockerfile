FROM savonet/liquidsoap:v2.2.5

USER root

# Instala Node.js 20 (Nodesource) e ferramentas essenciais
RUN apt-get update && apt-get install -y curl ffmpeg python3 && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/bin/yt-dlp && \
    chmod a+rx /usr/bin/yt-dlp && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /radio

# Copia scripts
COPY yt-dlp-audio.sh /usr/local/bin/yt-dlp-audio
RUN chmod +x /usr/local/bin/yt-dlp-audio

# Copia configuração
COPY radio.liq /radio/radio.liq

CMD ["liquidsoap", "/radio/radio.liq"]
