# ETS2 Radio

Sistema de rádio personalizada para Euro Truck Simulator 2, com integração com Discord, Painel Web e suporte a playlists do YouTube via Liquidsoap e Icecast.

## 🚀 Tecnologias Utilizadas

- **Docker & Docker Compose**: Orquestração de containers.
- **Liquidsoap**: Motor de áudio para streaming e gerenciamento de filas.
- **Icecast**: Servidor de streaming de áudio.
- **Python (Discord.py & Flask)**: Bot para comandos e Painel Web para controle da rádio.
- **yt-dlp**: Para processar links do YouTube em tempo real.

## 📋 Pré-requisitos

- Docker e Docker Compose instalados.
- Token de Bot do Discord (opcional, mas recomendado para comandos via chat).

## 🛠️ Configuração

1. Clone o repositório:

   ```bash
   git clone <url-do-repositorio>
   cd ets2-radio
   ```

2. Crie o arquivo `.env` baseado no exemplo:
   ```bash
   cp .env.example .env
   ```

## 🚀 Como Rodar

### Modo Desenvolvimento / Local

Para rodar o projeto localmente e ver os logs em tempo real:

```bash
docker-compose up
```

- **Painel Web**: [http://localhost:24016](http://localhost:24016)
- **Stream de Áudio**: [http://localhost:24015/ets2](http://localhost:24015/ets2)
- **Admin Icecast**: [http://localhost:24015](http://localhost:24015) (User: `admin` / Pass: `hackme`)

### Modo Produção

Para rodar em background (detach mode):

```bash
docker-compose up -d
```

Para atualizar o sistema após mudanças no código:

```bash
docker-compose up -d --build
```

## 🎮 Comandos do Bot (Discord)

- `/play <url>`: Adiciona uma música ou playlist do YouTube à fila manual.
- `/skip`: Pula a música atual.
- `/set_default <url>`: Define a playlist padrão que toca quando a fila manual está vazia.

## 📁 Estrutura do Projeto

- `/icecast`: Configurações do servidor Icecast.
- `/liquidsoap`: Scripts de lógica da rádio e processamento de áudio.
- `/scripts`: Código fonte do Bot Discord e Painel Flask.
- `/data`: Volume persistente para cache e downloads temporários.
