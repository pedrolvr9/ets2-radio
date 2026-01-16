import discord
from discord.ext import commands, tasks
from discord import app_commands
import yt_dlp
import telnetlib
import os
from dotenv import load_dotenv
import asyncio
import random
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
LIQUIDSOAP_HOST = os.getenv('LIQUIDSOAP_HOST', 'liquidsoap')
LIQUIDSOAP_PORT = int(os.getenv('LIQUIDSOAP_PORT', 1234))

# Variáveis para a playlist padrão
default_playlist_url = "https://www.youtube.com/playlist?list=PL-hBYtIlbWfumHH0X7TJuD7eKXpgHwhKT"
cached_default_urls = []

# --- Configuração Flask ---
app = Flask(__name__)
CORS(app)

async def init_default_playlist():
    global cached_default_urls
    if default_playlist_url:
        print(f"Iniciando busca da playlist padrão: {default_playlist_url}", flush=True)
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(default_playlist_url, download=False))
            if 'entries' in data:
                cached_default_urls = [e.get('url') for e in data['entries'] if e and e.get('url')]
                print(f"✅ Playlist padrão carregada com {len(cached_default_urls)} músicas.", flush=True)
        except Exception as e:
            print(f"Erro ao carregar playlist padrão: {e}", flush=True)

def send_to_liquidsoap(command):
    try:
        tn = telnetlib.Telnet(LIQUIDSOAP_HOST, LIQUIDSOAP_PORT, timeout=5)
        tn.write(f"{command}\n".encode('utf-8'))
        tn.write(b"quit\n")
        response = tn.read_all().decode('utf-8')
        tn.close()
        return response
    except Exception as e:
        return f"Error connecting to Liquidsoap: {e}"

def push_url_to_liquidsoap(url, queue="manual_queue"):
    # Se for um link direto do googlevideo, ignoramos pois ele expira e é amarrado ao IP
    if "googlevideo.com" in url:
        print(f"⚠️ Aviso: Link direto do googlevideo detectado e ignorado ({queue}).")
        return "Error: direct link"

    # Força o uso do protocolo youtube-dl para links do YouTube
    if "youtube.com" in url or "youtu.be" in url:
        if not url.startswith("youtube-dl:"):
            url = f"youtube-dl:{url}"
    
    print(f"Pushing to Liquidsoap ({queue}): {url}", flush=True)
    return send_to_liquidsoap(f"{queue}.push {url}")

async def check_queue_background_task():
    global cached_default_urls
    print("Iniciando tarefa de background para verificação da fila...", flush=True)
    while True:
        if default_playlist_url and cached_default_urls:
            try:
                res = send_to_liquidsoap("auto_queue.queue")
                # Se não houver erro de conexão
                if not res.startswith("Error"):
                    # Conta o número de IDs na fila automática
                    ids = []
                    for line in res.split('\n'):
                        line = line.strip()
                        if line and line not in ["END", "Bye!"]:
                            ids.extend(line.split())
                    
                    # Preenche a fila automática até ter 5 músicas
                    while len(ids) < 5:
                        next_url = random.choice(cached_default_urls)
                        push_url_to_liquidsoap(next_url, queue="auto_queue")
                        print(f"Repovoando fila automática com: {next_url}", flush=True)
                        ids.append("new_id")
            except Exception as e:
                print(f"Erro no loop de fila: {e}", flush=True)
        await asyncio.sleep(30)

# --- Bot Discord ---
class RadioBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        if TOKEN and TOKEN != "seu_token_aqui":
            await self.tree.sync()
            # Inicia a tarefa de background no loop do bot
            self.loop.create_task(check_queue_background_task())
            print(f"Synced slash commands and started background loops for {self.user}")
        else:
            print("AVISO: DISCORD_TOKEN não configurado. Bot do Discord desativado.")

bot = RadioBot()

# --- Shared Logic ---
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': False,
    'quiet': True,
    'extract_flat': True, # Garante que pegamos apenas o link do YouTube, não o link direto resolvido
}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

async def process_play_request(url):
    try:
        # Usa o executor padrão para não travar o loop de eventos
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if 'entries' in data:
            count = 0
            for entry in data['entries']:
                if entry:
                    m_url = entry.get('url')
                    # Se o m_url for um link direto (googlevideo), tentamos pegar o original ou web_url
                    original_url = entry.get('webpage_url') or m_url
                    if original_url:
                        push_url_to_liquidsoap(original_url)
                        count += 1
            return {"status": "success", "message": f"✅ Adicionadas {count} músicas à fila!"}
        else:
            original_url = data.get('webpage_url') or url
            push_url_to_liquidsoap(original_url)
            return {"status": "success", "message": f"✅ Adicionada à fila: **{data.get('title')}**"}
    except Exception as e:
        return {"status": "error", "message": f"❌ Erro: {str(e)}"}

# --- Rotas Flask ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/play', methods=['POST'])
def api_play():
    url = request.json.get('url')
    if not url:
        return jsonify({"status": "error", "message": "URL não fornecida"}), 400
    
    # Executa a lógica de processamento
    try:
        data = ytdl.extract_info(url, download=False)
        if 'entries' in data:
            count = 0
            for entry in data['entries']:
                if entry:
                    original_url = entry.get('webpage_url') or entry.get('url')
                    if original_url:
                        push_url_to_liquidsoap(original_url)
                        count += 1
            return jsonify({"status": "success", "message": f"Adicionadas {count} músicas da playlist!"})
        else:
            original_url = data.get('webpage_url') or url
            push_url_to_liquidsoap(original_url)
            return jsonify({"status": "success", "message": f"Adicionada: {data.get('title')}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/skip', methods=['POST'])
def api_skip():
    send_to_liquidsoap("ets2_radio.skip")
    return jsonify({"status": "success", "message": "Comando de pular enviado!"})

def parse_liquidsoap_metadata(data):
    metadata = {}
    for line in data.split('\n'):
        if '=' in line:
            parts = line.split('=', 1)
            key = parts[0].strip()
            value = parts[1].strip().strip('"')
            metadata[key] = value
    return metadata

@app.route('/api/now_playing')
def api_now_playing():
    # Primeiro, pegamos o ID que está tocando agora
    on_air_res = send_to_liquidsoap("request.on_air")
    if not on_air_res or on_air_res.strip().startswith("Error"):
        return jsonify({"status": "error", "message": "Erro ao conectar com Liquidsoap."})
    
    # Limpa o ID
    rid = on_air_res.replace("END", "").replace("Bye!", "").strip()
    
    if rid and rid.isdigit():
        # Busca metadados específicos desse ID
        meta_res = send_to_liquidsoap(f"request.metadata {rid}")
        metadata = parse_liquidsoap_metadata(meta_res)
        if metadata:
            return jsonify({"status": "success", "metadata": metadata, "id": rid})
    
    # Fallback para o método anterior caso não consiga o ID
    res = send_to_liquidsoap("ets2_radio.metadata")
    parts = res.split('---')
    for part in parts:
        if '=' in part:
            metadata = parse_liquidsoap_metadata(part)
            if metadata:
                return jsonify({"status": "success", "metadata": metadata})
    
    return jsonify({"status": "success", "metadata": {"title": "Playlist Padrão"}})

@app.route('/api/queue')
def api_queue():
    # Pega o que está tocando para filtrar da fila
    on_air_res = send_to_liquidsoap("request.on_air")
    current_rid = on_air_res.replace("END", "").replace("Bye!", "").strip()

    # Busca IDs de ambas as filas
    res_manual = send_to_liquidsoap("manual_queue.queue")
    res_auto = send_to_liquidsoap("auto_queue.queue")
    
    if res_manual.startswith("Error") or res_auto.startswith("Error"):
        return jsonify({"queue": [], "status": "error"})
    
    def get_ids(res):
        ids = []
        for line in res.split('\n'):
            line = line.strip()
            if line and line not in ["END", "Bye!"]:
                ids.extend(line.split())
        return ids

    manual_ids = get_ids(res_manual)
    auto_ids = get_ids(res_auto)
    
    # Prioriza manual_ids
    all_ids = manual_ids + auto_ids
    
    queue_data = []
    for rid in all_ids:
        # Se for o mesmo ID que está tocando, pula (já está no "No Ar")
        if rid == current_rid:
            continue
            
        meta_res = send_to_liquidsoap(f"request.metadata {rid}")
        meta = parse_liquidsoap_metadata(meta_res)
        
        title = meta.get("title")
        if not title or title == "":
            uri = meta.get("initial_uri", "")
            title = uri.replace("youtube-dl:", "") if uri else "Carregando..."
            
        queue_data.append({
            "id": rid,
            "title": title,
            "is_manual": rid in manual_ids,
            "uri": meta.get("initial_uri", "Desconhecido")
        })
    
    return jsonify({"queue": queue_data, "status": "success"})

# --- Comandos Discord ---
@bot.tree.command(name='skip', description='Pula a música atual')
async def discord_skip(interaction: discord.Interaction):
    send_to_liquidsoap("ets2_radio.skip")
    await interaction.response.send_message("⏭️ Pulando para a próxima música...")

@bot.tree.command(name='play', description='Adiciona uma música na fila')
async def discord_play(interaction: discord.Interaction, url: str):
    await interaction.response.send_message("🔍 Processando...")
    result = await process_play_request(url)
    await interaction.edit_original_response(content=result['message'])

@bot.tree.command(name='set_default', description='Define playlist padrão')
async def discord_set_default(interaction: discord.Interaction, url: str):
    global default_playlist_url, cached_default_urls
    await interaction.response.send_message(f"⚙️ Configurando...")
    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if 'entries' in data:
            default_playlist_url = url
            cached_default_urls = [e.get('url') for e in data['entries'] if e and e.get('url')]
            await interaction.edit_original_response(content=f"✅ Playlist padrão definida!")
        else:
            await interaction.edit_original_response(content="❌ URL deve ser uma playlist.")
    except Exception as e:
        await interaction.edit_original_response(content=f"❌ Erro: {str(e)}")

# --- Inicialização ---
def run_flask():
    app.run(host='0.0.0.0', port=8080)

async def main():
    # Inicia carga da playlist em background
    asyncio.create_task(init_default_playlist())
    # Inicia tarefa de verificação da fila em background
    asyncio.create_task(check_queue_background_task())

    if TOKEN:
        try:
            await bot.start(TOKEN)
        except discord.errors.LoginFailure:
            print("❌ Erro: DISCORD_TOKEN inválido. O bot do Discord não será iniciado.", flush=True)
            print("Iniciando apenas tarefas de background e Painel Web...", flush=True)
            while True: await asyncio.sleep(3600)
        except Exception as e:
            print(f"❌ Erro ao iniciar o bot: {e}", flush=True)
            while True: await asyncio.sleep(3600)
    else:
        print("Bot do Discord desativado (Token não configurado). Iniciando apenas Painel Web e tarefas de fundo...", flush=True)
        while True: await asyncio.sleep(3600)

if __name__ == '__main__':
    # Inicia Flask em uma thread separada
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Normaliza o TOKEN
    if not TOKEN or TOKEN.strip() in ["", "seu_token_aqui", "COLE_SEU_TOKEN_AQUI"]:
        TOKEN = None

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
