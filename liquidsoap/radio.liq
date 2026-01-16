# --- CONFIGURAÇÕES GERAIS ---
settings.log.stdout := true
settings.log.file := false
settings.init.allow_root := true
settings.protocol.youtube_dl.timeout := 600.0
settings.protocol.youtube_dl.path := "/usr/local/bin/yt-dlp-audio"

# Carregar senhas do ambiente
icecast_password = os.getenv("ICECAST_SOURCE_PASSWORD")
icecast_password = if icecast_password == "" then "hackme" else icecast_password end

# Habilitar controle via telnet (porta interna para o bot)
settings.server.telnet := true
settings.server.telnet.bind_addr := "0.0.0.0"
settings.server.telnet.port := 1234

# --- FONTES DE ÁUDIO ---

# Fila para pedidos MANUAIS (Prioridade Máxima)
manual_queue = request.queue(id="manual_queue")

# Fila para músicas AUTOMÁTICAS (Playlist Padrão)
auto_queue = request.queue(id="auto_queue")

# Prioriza a fila manual. 
# track_sensitive=false permite que mude para a fila manual assim que uma música entrar,
# interrompendo a música da fila automática se necessário.
radio = fallback(id="radio_main", track_sensitive=false, [manual_queue, auto_queue, blank()])

# Aplica crossfade
radio = crossfade(radio, duration=6.0)

# Torna a rádio infalível
radio = mksafe(radio)

output.icecast(
  %mp3(bitrate=320),
  host="icecast",
  port=9090,
  password=icecast_password,
  mount="/ets2",
  name="Minha Rádio ETS2",
  description="YouTube Playlist Shuffle + Crossfade",
  genre="Game",
  id="ets2_radio",
  radio
)
