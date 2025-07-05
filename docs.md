## 🖥️ Cliente CLI (Command Line Interface)

### Características Principais

- __Interface em Terminal__: Interação direta via linha de comando
- __Modo Interativo__: Chat conversacional no terminal
- __Ideal para__: Desenvolvedores, administradores de sistema, automação
- __Tecnologias__: Python 3.12+, MCP Protocol, múltiplos LLMs

### Funcionalidades

- Chat interativo com agente IA
- Execução direta de comandos MCP
- Suporte a múltiplos LLMs (Gemini, Claude, Ollama)
- Histórico de conversas
- Comandos especiais (/help, /tools, /clear)

### Vantagens

- __Performance__: Menor overhead, execução mais rápida
- __Automação__: Fácil integração com scripts e pipelines
- __Recursos__: Consome menos memória e CPU
- __Flexibilidade__: Ideal para uso em servidores remotos via SSH

### Casos de Uso

- Monitoramento automatizado via scripts
- Integração com pipelines CI/CD
- Administração remota de sistemas
- Desenvolvimento e debugging de ferramentas MCP

## 🌐 Cliente UI (User Interface - Streamlit)

### Características Principais

- __Interface Web__: Acesso via navegador
- __Visual Intuitivo__: Interface gráfica amigável
- __Ideal para__: Usuários finais, analistas, apresentações
- __Tecnologias__: Streamlit, Python 3.12+, componentes visuais

### Funcionalidades

- Interface web responsiva
- Chat visual com histórico
- Configuração dinâmica de LLMs via sidebar
- Visualização de resultados em tabelas e gráficos
- Upload de arquivos e documentos
- Exportação de dados

### Vantagens

- __Usabilidade__: Interface intuitiva para usuários não-técnicos
- __Visualização__: Gráficos, tabelas e dashboards integrados
- __Colaboração__: Fácil compartilhamento de sessões
- __Acessibilidade__: Acesso via qualquer navegador

### Casos de Uso

- Análise exploratória de dados do Datadog
- Apresentações e demonstrações
- Uso por equipes não-técnicas
- Dashboards personalizados

## 🔄 Comparação Técnica

| Aspecto | CLI | UI (Streamlit) |
|---------|-----|----------------|
| Inicialização | make start client=cli | make start client=ui |
| Acesso | Terminal interativo | http://localhost:8501 |
| Recursos | Baixo consumo | Médio consumo |
| Configuração | Arquivo .env | Interface + .env |
| Automação | Excelente | Limitada |
| Visualização | Texto | Gráficos + Texto |

## 🚀 Como Escolher

### Use o __Cliente CLI__ quando:

- Você é desenvolvedor ou administrador de sistema
- Precisa de automação e integração com scripts
- Trabalha em ambiente de servidor remoto
- Prioriza performance e eficiência
- Quer integrar com pipelines de CI/CD

### Use o __Cliente UI__ quando:

- Você prefere interfaces visuais
- Precisa apresentar dados para equipes
- Quer explorar dados interativamente
- Trabalha com usuários não-técnicos
- Precisa de visualizações e dashboards

## 🛠️ Arquitetura Compartilhada

Ambos os clientes compartilham:

- __Mesmos servidores MCP__ (Datadog, DuckDuckGo)
- __Mesmas ferramentas__ (80+ do Datadog)
- __Mesmos LLMs__ (Gemini, Claude, Ollama)
- __Mesmo protocolo MCP__ para comunicação
- __Mesmas configurações__ de ambiente

Isso garante consistência de funcionalidades independente da interface escolhida.
