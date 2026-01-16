# 🚛 ETS2 Radio System

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/)

Um sistema completo de rádio personalizada para o **Euro Truck Simulator 2**, integrando playlists do YouTube, bot de Discord e um painel administrativo web moderno.

---

## 🌟 Funcionalidades

- 🎵 **Streaming via Icecast/Liquidsoap**: Áudio de alta qualidade com transições crossfade.
- 🤖 **Integração com Discord**: Comandos Slash (/) para controlar a rádio diretamente do seu servidor.
- 🌐 **Painel Web**: Interface moderna para gerenciar a fila e pular músicas sem precisar do Discord.
- 🔄 **Fila Automática**: Nunca fica em silêncio. Se a fila manual esvaziar, o sistema toca músicas aleatórias de uma playlist padrão.
- 🛠️ **Bypass de Bloqueio**: Configurado com técnicas de impersonificação e suporte a cookies para evitar bloqueios do YouTube em servidores (VPS).

---

## 🚀 Tecnologias

- **Liquidsoap**: Motor de automação de áudio.
- **Icecast**: Servidor de streaming.
- **Flask**: API e Painel Web.
- **Discord.py**: Automação do bot.
- **yt-dlp**: Extração de áudio em tempo real.

---

## 🛠️ Instalação e Configuração

### 📋 Pré-requisitos

- Docker e Docker Compose instalados.
- Um Token de Bot no [Discord Developer Portal](https://discord.com/developers/applications).

### ⚙️ Passo a Passo

1. **Clone o projeto:**

   ```bash
   git clone https://github.com/pedrolvr9/ets2-radio.git
   cd ets2-radio
   ```

2. **Configure o ambiente:**

   ```bash
   cp .env.example .env
   ```

   Edite o `.env` e insira seu `DISCORD_TOKEN` e as senhas desejadas para o Icecast.

3. **(Opcional) Bypass de Cookies (Base64):**
   Se o YouTube bloquear seu servidor (erro: _Sign in to confirm you're not a bot_):
   - Exporte os cookies do YouTube (extensão "Get cookies.txt LOCALLY").
   - Converta o conteúdo do arquivo para Base64. 
     - No Linux/Mac: `cat cookies.txt | base64 -w 0`
     - No Windows (PowerShell): `[Convert]::ToBase64String([IO.File]::ReadAllBytes("cookies.txt"))`
   - Adicione o resultado na variável `YT_COOKIES_BASE64` no seu `.env` ou no painel do Coolify.
   - O sistema criará o arquivo `data/cookies.txt` automaticamente.

---

## 🏃 Como Executar

### Local / Desenvolvimento

```bash
docker-compose up --build
```

### Produção (Background)

```bash
docker-compose up -d --build
```

### 🔗 Acessos Rápidos

- **Painel Administrativo**: `http://localhost:24016`
- **Link do Stream (para o ETS2)**: `http://localhost:24015/ets2`
- **Admin do Icecast**: `http://localhost:24015` (User: `admin`)

---

## 🎮 Comandos do Discord

| Comando              | Descrição                                                   |
| :------------------- | :---------------------------------------------------------- |
| `/play <url>`        | Adiciona uma música ou playlist do YouTube à fila.          |
| `/skip`              | Pula a música que está tocando agora.                       |
| `/set_default <url>` | Define a playlist que tocará quando a rádio estiver ociosa. |

---

## 📁 Estrutura do Repositório

- `icecast/`: Configurações e Dockerfile do servidor de stream.
- `liquidsoap/`: Lógica da rádio, crossfade e processamento de áudio.
- `scripts/`: Backend Python (Bot Discord e Painel Flask).
- `data/`: Volume compartilhado para cookies, cache e logs.

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
