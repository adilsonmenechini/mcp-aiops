# MCP AIOps

<div align="center">

![MCP AIOps](https://via.placeholder.com/200x80/1f77b4/ffffff?text=MCP+AIOps)

**Plataforma AIOps robusta baseada no Model Context Protocol (MCP)**  
*Integração completa com Datadog, DuckDuckGo e múltiplos LLMs*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://modelcontextprotocol.io/)
[![Datadog](https://img.shields.io/badge/Datadog-80%2B%20tools-purple.svg)](servers/mcp-datadog/)

</div>

## 🚀 Quick Start

Escolha seu modo de operação e execute:

```bash
# Modo UI (Interface Web Streamlit)
make start client=ui

# Modo CLI (Terminal Interativo)  
make start client=cli

# Apenas servidores MCP (para desenvolvimento)
make tools client=ui  # ou client=cli
```

Acesse:
- **Interface Web**: http://localhost:8501
- **CLI**: Execute `make host` para modo interativo

## 📋 Pré-requisitos

| Software | Versão | Instalação |
|----------|--------|------------|
| **Python** | 3.12+ | [Download](https://www.python.org/downloads/) |
| **Docker** | 20.10+ | [Install](https://docs.docker.com/get-started/) |
| **Docker Compose** | 2.0+ | [Install](https://docs.docker.com/compose/install/) |
| **Make** | Qualquer | `apt install make` / `brew install make` |

## 🏗️ Arquitetura

### Visão Geral do MCP Protocol

```
┌─────────────────┐    MCP     ┌──────────────────┐    API    ┌─────────────┐
│   LLM Client    │◄──────────►│   MCP Server     │◄─────────►│  External   │
│  (UI/CLI)       │  Protocol  │  (Datadog/DDG)   │   Calls   │   Service   │
└─────────────────┘            └──────────────────┘           └─────────────┘
```

### Componentes do Sistema

```
mcp-aiops/
├── clients/                     # Interfaces de usuário
│   ├── cli-chatbot/            # 🖥️  Terminal interativo
│   └── ui-streamlit/           # 🌐 Interface web
├── servers/                     # Servidores MCP
│   ├── mcp-datadog/            # 📊 80+ ferramentas Datadog
│   ├── mcp-duckduckgo/         # 🔍 Busca e extração web
│   └── mcp-user-db/            # 👥 Gerenciamento usuários
├── common/                      # Configurações compartilhadas
│   ├── docker-compose-cli.yaml # 🐳 Compose para CLI
│   ├── docker-compose-ui.yaml  # 🐳 Compose para UI
│   └── docs.md                 # 📚 Documentação comum
└── Makefile                    # 🛠️  Automação de comandos
```

### Fluxo de Dados

1. **Cliente** (UI/CLI) envia requisição via MCP Protocol
2. **Servidor MCP** processa e chama APIs externas (Datadog, DuckDuckGo)
3. **Resposta** é formatada e retornada ao cliente
4. **LLM** processa a resposta e gera insights

## 💻 Instalação

### Método 1: Docker (Recomendado)

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/adilsonmenechini/mcp-aiops.git
   cd mcp-aiops
   ```

2. **Configure variáveis de ambiente**:
   ```bash
   # Datadog
   cp servers/mcp-datadog/.env.template servers/mcp-datadog/.env
   
   # UI Streamlit  
   cp clients/ui-streamlit/.env-examples clients/ui-streamlit/.env
   
   # CLI Chatbot
   cp clients/cli-chatbot/.env-examples clients/cli-chatbot/.env
   ```

3. **Edite os arquivos .env** com suas credenciais:
   ```bash
   # servers/mcp-datadog/.env
   DATADOG_API_KEY=sua_api_key_aqui
   DATADOG_APP_KEY=sua_app_key_aqui
   
   # clients/*/env (escolha um LLM)
   LLM_PROVIDER=gemini  # ou anthropic, ollama
   GOOGLE_API_KEY=sua_api_key_aqui
   ```

4. **Inicie o sistema**:
   ```bash
   make start client=ui    # Interface web
   # ou
   make start client=cli   # Terminal
   ```

### Método 2: Desenvolvimento Local

1. **Instale dependências Python**:
   ```bash
   # Com uv (recomendado)
   pip install uv
   cd clients/ui-streamlit && uv sync
   cd clients/cli-chatbot && uv sync
   cd servers/mcp-datadog && uv sync
   
   # Ou com pip tradicional
   pip install -r clients/ui-streamlit/requirements.txt
   ```

2. **Execute servidores MCP**:
   ```bash
   make tools client=ui  # Inicia apenas os servidores
   ```

3. **Execute cliente manualmente**:
   ```bash
   # UI
   cd clients/ui-streamlit && streamlit run app.py
   
   # CLI  
   cd clients/cli-chatbot && python main.py
   ```

## 🎯 Uso

### Interface Web (Streamlit)

1. **Acesse**: http://localhost:8501
2. **Configure LLM** na sidebar
3. **Digite comandos** no chat:
   ```
   Liste todos os monitores do Datadog
   Busque informações sobre "kubernetes monitoring"
   Crie um monitor para CPU alta
   ```

### Cliente CLI

1. **Modo interativo**:
   ```bash
   make host  # Abre terminal dentro do container
   ```

2. **Comandos disponíveis**:
   ```bash
   # Ajuda
   /help
   
   # Listar ferramentas
   /tools
   
   # Limpar histórico
   /clear
   
   # Exemplos de uso
   tools datadog list_monitors
   tools datadog create_monitor --name "High CPU" --query "avg(last_5m):avg:system.cpu.user{*} > 90"
   tools duckduckgo search --query "datadog best practices"
   ```

### Comandos Makefile

```bash
# Gerenciamento de serviços
make start client=ui|cli     # Inicia cliente + servidores
make tools client=ui|cli     # Apenas servidores MCP
make stop client=ui|cli      # Para tudo
make logs client=ui|cli      # Visualiza logs
make clean                   # Remove containers e volumes

# Desenvolvimento
make host                    # CLI interativo
make test client=cli         # Testa cliente CLI
```

## 🔧 Ferramentas Disponíveis

### 📊 Datadog (80+ Ferramentas)

<details>
<summary><strong>Monitoramento & APM</strong></summary>

- **APM**: `list_apm_traces`, `get_apm_trace_details`, `query_apm_errors`, `query_apm_latency`
- **Métricas**: `query_metrics`, `list_metrics`, `query_p99_latency`, `query_error_rate`
- **Traces**: `list_traces`, `get_trace_details`, `summarize_traces`
- **Hosts**: `list_hosts`, `get_host_totals`, `mute_host`, `unmute_host`

</details>

<details>
<summary><strong>Alertas & Incidentes</strong></summary>

- **Monitores**: `create_monitor`, `delete_monitor`, `get_monitor_status`, `update_monitor`
- **Alertas**: `mute_alert`, `unmute_alert`
- **Incidentes**: `search_incidents`, `list_incidents`, `get_incident`, `update_incident`
- **Downtime**: `create_downtime`, `update_downtime`, `cancel_downtime`

</details>

<details>
<summary><strong>Administração</strong></summary>

- **Usuários**: `list_users`, `get_user`
- **Funções**: `list_roles`, `create_role`, `delete_role`, `update_role`
- **Tags**: `list_host_tags`, `add_host_tags`, `delete_host_tags`
- **Dashboards**: `list_dashboards`, `list_prompts`

</details>

<details>
<summary><strong>SLOs & Qualidade</strong></summary>

- **SLOs**: `list_slos`, `get_slo`, `delete_slo`
- **Service Checks**: `submit_service_check`, `list_service_checks`
- **Dependencies**: `list_service_dependencies`, `create_service_dependency`
- **Root Cause**: `analyze_service_with_apm`

</details>

### 🔍 DuckDuckGo

- **`search`**: Busca informações na web
- **`fetch_content`**: Extrai conteúdo de URLs específicas

### 👥 User DB

- Gerenciamento local de usuários (exemplo/desenvolvimento)

## ⚙️ Configuração

### LLM Providers

#### Google Gemini (Recomendado)
```bash
LLM_PROVIDER=gemini
GOOGLE_API_KEY=sua_api_key
GOOGLE_MODEL=gemini-2.0-flash  # ou gemini-1.5-pro
```

#### Anthropic Claude
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sua_api_key
ANTHROPIC_MODEL=claude-3-5-sonnet-20240620
```

#### Ollama (Local)
```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
# Certifique-se que Ollama está rodando localmente
```

### Configurações Avançadas

#### Parâmetros do Modelo
```bash
LLM_TEMPERATURE=0.5          # Criatividade (0.0-1.0)
LLM_MAX_TOKENS=4096          # Tokens máximos por resposta
LLM_TOP_K=2                  # Top-K sampling
LLM_TOP_P=0.5                # Top-P sampling
LLM_MAX_RETRIES=3            # Tentativas em caso de erro
LLM_RETRY_DELAY_SECONDS=2.0  # Delay entre tentativas
```

#### Logs
```bash
LOG_LEVEL=ERROR  # DEBUG, INFO, WARNING, ERROR
```

### Portas de Serviço

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| UI Streamlit | 8501 | Interface web |
| MCP Datadog | 8101 | Servidor Datadog |
| MCP DuckDuckGo | 8102 | Servidor DuckDuckGo |

## 🐛 Troubleshooting

### Problemas Comuns

#### Docker não inicia
```bash
# Verificar se Docker está rodando
docker --version
docker-compose --version

# Limpar containers antigos
make clean
```

#### Erro de permissão Docker
```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

#### Variáveis de ambiente não carregam
```bash
# Verificar se arquivos .env existem
ls -la clients/ui-streamlit/.env
ls -la servers/mcp-datadog/.env

# Verificar formato (sem espaços)
cat servers/mcp-datadog/.env
```

#### LLM não responde
```bash
# Verificar API keys
echo $GOOGLE_API_KEY
echo $ANTHROPIC_API_KEY

# Testar conectividade
curl -H "Authorization: Bearer $GOOGLE_API_KEY" \
     https://generativelanguage.googleapis.com/v1/models
```

#### Servidores MCP não conectam
```bash
# Verificar logs
make logs client=ui

# Verificar portas
netstat -tlnp | grep 810
docker ps
```

### Logs e Debug

```bash
# Logs em tempo real
make logs client=ui

# Logs específicos de um serviço
docker logs mcpdatadog
docker logs mcpduckduckgo

# Debug modo verboso
LOG_LEVEL=DEBUG make start client=ui
```

## 🤝 Contribuindo

### Desenvolvimento Local

1. **Fork e clone**:
   ```bash
   git clone https://github.com/seu-usuario/mcp-aiops.git
   cd mcp-aiops
   ```

2. **Configurar ambiente**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows
   
   pip install uv
   ```

3. **Instalar dependências**:
   ```bash
   cd clients/ui-streamlit && uv sync
   cd ../cli-chatbot && uv sync
   cd ../../servers/mcp-datadog && uv sync
   ```

4. **Executar testes**:
   ```bash
   make test client=cli
   ```

### Adicionando Novos Servidores MCP

1. **Criar estrutura**:
   ```bash
   mkdir servers/mcp-novoservico
   cd servers/mcp-novoservico
   ```

2. **Implementar servidor**:
   ```python
   # server.py
   from mcp.server import Server
   
   server = Server("novo-servico")
   
   @server.tool()
   async def minha_ferramenta():
       return "Resultado"
   ```

3. **Adicionar ao docker-compose**:
   ```yaml
   novoservico:
     build: ./servers/mcp-novoservico
     ports:
       - "8103:8000"
   ```

### Padrões de Código

- **Python 3.12+** com type hints
- **Async/await** para operações I/O
- **Pydantic** para validação de dados
- **Docstrings** para todas as funções públicas
- **Error handling** robusto

### Commits

```bash
git commit -m "feat: adiciona integração com Grafana"
git commit -m "fix: corrige timeout em queries longas"
git commit -m "docs: atualiza README com novos exemplos"
```

## 📚 Documentação Adicional

- [Documentação Datadog](servers/mcp-datadog/docs/modules.md) - 80+ ferramentas detalhadas
- [MCP Protocol](https://modelcontextprotocol.io/) - Especificação oficial
- [Datadog API](https://docs.datadoghq.com/api/) - Referência da API

## 🗺️ Roadmap

### Em Desenvolvimento
- [ ] Integração com Grafana
- [ ] Suporte a Prometheus
- [ ] Dashboard customizável
- [ ] Autenticação OAuth

### Planejado
- [ ] Integração com AWS CloudWatch
- [ ] Suporte a Kubernetes
- [ ] Alertas via Slack/Teams
- [ ] Exportação de relatórios PDF
- [ ] API REST para integração externa

### Futuro
- [ ] Machine Learning para detecção de anomalias
- [ ] Integração com Terraform
- [ ] Suporte multi-tenant
- [ ] Interface mobile

## 📊 Status do Projeto

- ✅ **Core MCP Protocol** - Implementado
- ✅ **Datadog Integration** - 80+ ferramentas
- ✅ **Multi-LLM Support** - Gemini, Claude, Ollama
- ✅ **Docker Deployment** - Produção ready
- ✅ **CLI & Web UI** - Interfaces completas
- 🔄 **Documentation** - Em progresso
- 🔄 **Testing Suite** - Em desenvolvimento

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

```
MIT License - Copyright (c) 2025 MCP AIOps Contributors
```

---

<div align="center">

**Desenvolvido com ❤️ usando MCP Protocol**

[Reportar Bug](https://github.com/adilsonmenechini/mcp-aiops/issues) • 
[Solicitar Feature](https://github.com/adilsonmenechini/mcp-aiops/issues) • 
[Contribuir](CONTRIBUTING.md)

</div>
