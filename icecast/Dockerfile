FROM moul/icecast

# Copia o template para dentro da imagem
COPY icecast.xml /usr/share/icecast/icecast.xml.tmpl

# Define o entrypoint para processar as variáveis e iniciar o icecast2
ENTRYPOINT ["sh", "-c", "sed \"s/@ICECAST_SOURCE_PASSWORD@/$ICECAST_SOURCE_PASSWORD/g; s/@ICECAST_ADMIN_PASSWORD@/$ICECAST_ADMIN_PASSWORD/g\" /usr/share/icecast/icecast.xml.tmpl > /etc/icecast2/icecast.xml && exec icecast2 -c /etc/icecast2/icecast.xml"]
