FROM savonet/liquidsoap:v2.2.5

USER root

# Instala ferramentas essenciais e o Node.js como runtime de JS para o yt-dlp
RUN apt-get update && apt-get install -y ffmpeg curl nodejs python3 && \
    ln -s /usr/bin/nodejs /usr/bin/node || true && \
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
