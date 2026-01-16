FROM savonet/liquidsoap:v2.2.5

USER root

# Instala ferramentas essenciais, Python e Node.js
RUN apt-get update && apt-get install -y curl ffmpeg python3 python3-pip python3-venv nodejs unzip git && \
    # Cria um ambiente virtual
    python3 -m venv /opt/yt-dlp-env && \
    # Instala o yt-dlp e o yt-dlp-ejs diretamente do MASTER do GitHub (Fix para issue #13930)
    /opt/yt-dlp-env/bin/pip install -U "git+https://github.com/yt-dlp/yt-dlp.git@master" "yt-dlp-ejs" && \
    # Cria o link simbólico
    ln -s /opt/yt-dlp-env/bin/yt-dlp /usr/bin/yt-dlp && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /radio

# Copia scripts
COPY yt-dlp-audio.sh /usr/local/bin/yt-dlp-audio
RUN chmod +x /usr/local/bin/yt-dlp-audio

# Copia configuração
COPY radio.liq /radio/radio.liq

CMD ["liquidsoap", "/radio/radio.liq"]
