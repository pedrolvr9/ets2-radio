FROM savonet/liquidsoap:v2.2.5

USER root

# Instala yt-dlp e outras ferramentas
RUN apt-get update && apt-get install -y yt-dlp ffmpeg curl nodejs && rm -rf /var/lib/apt/lists/*

WORKDIR /radio

# Copia scripts
COPY yt-dlp-audio.sh /usr/local/bin/yt-dlp-audio
RUN chmod +x /usr/local/bin/yt-dlp-audio

# Copia configuração
COPY radio.liq /radio/radio.liq

CMD ["liquidsoap", "/radio/radio.liq"]
