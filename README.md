# MCP AIOps

![MCP Logo](https://via.placeholder.com/150x50?text=MCP+aiops) *placeholder for actual logo*

Este é um aiops para o Model Context Protocol (MCP) que fornece uma integração robusta com o Datadog através de interfaces web e CLI.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](pyproject.toml)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](docker-compose.yaml)

## 🌟 Funcionalidades

- Interface web interativa usando Streamlit
- Cliente CLI para interações via terminal
- Integração completa com Datadog
- Suporte a múltiplos modelos de LLM
- Comunicação em tempo real via SSE (Server-Sent Events)

## 🏗️ Arquitetura

O projeto é composto por dois componentes principais:

### Estrutura do Projeto

```
mcp-aiops/
├── clients/
│   ├── cli-chatbot/             # Cliente CLI para interação com o agente IA
│   └── ui-streamlit/            # Interface web interativa usando Streamlit
├── servers/
│   ├── mcp-datadog/             # Servidor MCP para integração com a API Datadog
│   ├── mcp-duckduckgo/          # Servidor MCP para busca de informações via DuckDuckGo
│   └── mcp-user-db/             # Servidor MCP para gerenciamento de usuários (exemplo)
├── docker-compose.yaml          # Configuração para orquestração de serviços Docker
├── LICENSE                      # Arquivo de licença do projeto
├── README.md                    # Este arquivo de documentação
└── docs/                        # Documentação adicional do projeto
    └── plan.md
```

### Clientes

1. **UI Streamlit** (`/clients/ui-streamlit/`)
   - Interface web interativa
   - Chat com agente IA
   - Histórico de conversas
   - Execução de ferramentas MCP
   - Configurações dinâmicas

2. **CLI Chatbot** (`/clients/cli-chatbot/`)
   - Interface em linha de comando
   - Mesmas funcionalidades da UI web

### Servidores

1. **MCP Datadog** (`/servers/mcp-datadog/`)
   - Integração com API Datadog
   - Monitoramento (APM, métricas, logs)
   - Gerenciamento de incidentes
   - SLOs e verificações de serviço
   - Administração (usuários, funções, tags)

2. **MCP DuckDuckGo** (`/servers/mcp-duckduckgo/`)
   - Integração com a API de busca DuckDuckGo
   - Ferramentas para busca de informações e extração de conteúdo de URLs

3. **MCP User DB** (`/servers/mcp-user-db/`)
   - Gerenciamento de usuários
   - Base de dados local

## 🚀 Instalação

### Início Rápido

Para colocar o projeto em funcionamento rapidamente, siga estes passos:

1. Clone o repositório:
   ```bash
   git clone <repository-url>
   cd mcp-aiops
   ```
2. Configure as variáveis de ambiente:
   ```bash
   cp servers/mcp-datadog/.env.template servers/mcp-datadog/.env
   cp clients/ui-streamlit/.env-examples clients/ui-streamlit/.env
   cp clients/cli-chatbot/.env-examples clients/cli-chatbot/.env
   # Edite os arquivos .env com suas credenciais e configurações
   ```
3. Inicie os serviços com Docker Compose:
   ```bash
   docker-compose up -d
   ```
4. Acesse a interface web em `http://localhost:8501` ou o cliente CLI em `clients/cli-chatbot/main.py`.

---

### Pré-requisitos

Certifique-se de ter os seguintes softwares instalados em sua máquina:

| Software | Versão Mínima | Link |
|----------|--------------|------|
| Docker | 20.10+ | [Download](https://www.docker.com/get-started) |
| Docker Compose | 2.0+ | [Install](https://docs.docker.com/compose/install/) |
| Python | 3.9+ | [Download](https://www.python.org/downloads/) |
| pip | 22.0+ | [Install](https://pip.pypa.io/en/stable/installation/) |
| uv (opcional) | 0.1+ | [Install](https://github.com/astral-sh/uv) |

> **Note**: O `uv` é recomendado para um gerenciamento de dependências mais rápido e eficiente.

### Passos de Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd mcp-aiops
```

2. Configure as variáveis de ambiente:

### Configuração de Variáveis de Ambiente

O projeto utiliza arquivos `.env` para gerenciar variáveis de ambiente. Siga os passos abaixo para configurá-los:

1. **Servidor MCP Datadog**:
   - Copie o arquivo de exemplo:
     ```bash
     cp servers/mcp-datadog/.env.template servers/mcp-datadog/.env
     ```
   - Edite `servers/mcp-datadog/.env` e preencha com suas credenciais do Datadog:
     ```
     DATADOG_API_KEY=sua_api_key_aqui
     DATADOG_APP_KEY=sua_app_key_aqui
     DATADOG_SITE=datadoghq.com # ou datadoghq.eu, etc.
     ```

2. **Cliente UI Streamlit**:
   - Copie o arquivo de exemplo:
     ```bash
     cp clients/ui-streamlit/.env-examples clients/ui-streamlit/.env
     ```
   - Edite `clients/ui-streamlit/.env` e configure conforme necessário. Exemplo:
     ```
     LLM_PROVIDER=gemini
     GOOGLE_API_KEY=sua_api_key_do_google_aqui
     GOOGLE_MODEL=gemini-1.5-flash # Ou outro modelo preferido
     ```

3. **Cliente CLI Chatbot**:
   - Copie o arquivo de exemplo:
     ```bash
     cp clients/cli-chatbot/.env-examples clients/cli-chatbot/.env
     ```
   - Edite `clients/cli-chatbot/.env` e configure conforme necessário. Exemplo:
     ```
     LLM_PROVIDER=gemini
     GOOGLE_API_KEY=sua_api_key_do_google_aqui
     GOOGLE_MODEL=gemini-1.5-flash # Ou outro modelo preferido
     ```

> **Importante**: Nunca exponha suas chaves de API em repositórios públicos.

3. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Instale as dependências do projeto**:

   Recomendado (com `uv`):
   ```bash
   uv sync
   ```

   Alternativo (com `pip`):
   ```bash
   pip install -r requirements.txt
   ```

5. **Inicie os serviços usando Docker Compose**:
   ```bash
   docker-compose up -d
   ```
   Para verificar o status dos contêineres:
   ```bash
   docker-compose ps
   ```
   Para parar os serviços:
   ```bash
   docker-compose down
   ```

## 💻 Uso

### Interface Web

1. Acesse a interface web em `http://localhost:8501`
2. Use o chat para interagir com o agente
3. Execute ferramentas do Datadog através dos comandos

**Comandos básicos:**
- `/help` - Mostra ajuda
- `/tools` - Lista ferramentas disponíveis
- `/clear` - Limpa o histórico

### Cliente CLI

1. Execute o cliente CLI:
```bash
cd clients/cli-chatbot
python main.py
```

2. Digite seus comandos no terminal

**Exemplos de comandos:**
```bash
# Listar todos os monitores
tools datadog list_monitors

# Criar um novo monitor
tools datadog create_monitor --name "High CPU Usage" --query "avg(last_5m):avg:system.cpu.user{*} > 90"
```

## 🔧 Ferramentas Disponíveis

### Monitoramento
- APM (Application Performance Monitoring)
- Métricas e dashboards
- Logs e traces
- Hosts e serviços

### Gerenciamento de Incidentes
- Criação e gestão de alertas
- Gerenciamento de incidentes
- Análise de causa raiz
- Downtime programado

### SLOs e Qualidade
- Definição e monitoramento de SLOs
- Verificações de serviço
- Gestão de dependências
- Métricas de latência e erro

### Administração
- Gestão de usuários e funções
- Gerenciamento de tags
- Políticas de configuração
- Métricas de uso

### DuckDuckGo
- Busca de informações (`search`)
- Extração de conteúdo de URLs (`fetch_content`)

## 🔌 Portas

- UI Streamlit: 8501
- Servidor MCP Datadog: 8101
- Servidor MCP DuckDuckGo: 8000

## 📚 Documentação

A documentação completa das ferramentas do Datadog está disponível em `/servers/mcp-datadog/docs/modules.md`.

## 🤝 Contribuindo

Sua contribuição é muito bem-vinda! Para contribuir com o projeto, siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma nova branch para sua feature ou correção de bug:
   ```bash
   git checkout -b feature/sua-feature-incrivel
   # ou
   git checkout -b bugfix/correcao-de-bug
   ```
3. Faça suas alterações e commite-as com mensagens claras e descritivas:
   ```bash
   git commit -m 'feat: Adiciona nova funcionalidade X' # para features
   # ou
   git commit -m 'fix: Corrige problema Y' # para correções
   ```
4. Envie suas alterações para o seu fork:
   ```bash
   git push origin feature/sua-feature-incrivel
   ```
5. Abra um Pull Request para a branch `main` deste repositório, descrevendo suas alterações e o problema que elas resolvem.

### Extensibilidade

O projeto é projetado para ser extensível. Você pode adicionar novos servidores MCP ou clientes seguindo a estrutura existente:

- **Novos Servidores MCP**: Crie um novo diretório em `servers/` e implemente sua lógica de integração com APIs externas, seguindo o padrão dos servidores `mcp-datadog` ou `mcp-duckduckgo`.
- **Novos Clientes**: Crie um novo diretório em `clients/` e desenvolva sua interface (web, desktop, etc.) para interagir com os servidores MCP, utilizando a arquitetura de comunicação existente.

## 🛠 Troubleshooting

### Problemas com Docker
- **Erro de permissão**: Se encontrar erros de permissão com Docker, adicione seu usuário ao grupo docker:
  ```bash
  sudo usermod -aG docker $USER
  newgrp docker
  ```

### Problemas com variáveis de ambiente
- Certifique-se de que todos os arquivos `.env` foram criados corretamente
- Verifique se as variáveis estão no formato `VAR=valor` sem espaços

### Problemas com dependências Python
- Se encontrar erros com `uv`, tente usar `pip`:
  ```bash
  pip install -r requirements.txt
  ```

## 🗺 Roadmap

### Próximos recursos planejados

- [ ] Integração com Grafana
- [ ] Suporte a autenticação OAuth
- [ ] Dashboard de métricas customizável
- [ ] Exportação de relatórios em PDF
- [ ] Suporte a múltiplos idiomas

### Melhorias futuras

- Melhor documentação da API
- Testes automatizados
- Otimização de performance

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.