FROM savonet/liquidsoap:v2.2.5

USER root

# Instala ferramentas essenciais, Python e Node.js
RUN apt-get update && apt-get install -y curl ffmpeg python3 python3-pip python3-venv nodejs unzip && \
    # Cria um ambiente virtual e instala o yt-dlp com EJS embutido (Opção 1 da Wiki)
    python3 -m venv /opt/yt-dlp-env && \
    /opt/yt-dlp-env/bin/pip install -U "yt-dlp[default]" && \
    # Cria um link simbólico para o yt-dlp ficar acessível globalmente
    ln -s /opt/yt-dlp-env/bin/yt-dlp /usr/bin/yt-dlp && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /radio

# Copia scripts
COPY yt-dlp-audio.sh /usr/local/bin/yt-dlp-audio
RUN chmod +x /usr/local/bin/yt-dlp-audio

# Copia configuração
COPY radio.liq /radio/radio.liq

CMD ["liquidsoap", "/radio/radio.liq"]
