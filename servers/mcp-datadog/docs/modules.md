# Módulos MCP Datadog

Este documento descreve os módulos disponíveis no servidor MCP Datadog e suas respectivas funcionalidades.

## Sumário

- [Alertas](#alertas)
- [APM (Application Performance Monitoring)](#apm)
- [Dashboards](#dashboards)
- [Downtime](#downtime)
- [Eventos](#eventos)
- [Hosts](#hosts)
- [Incidentes](#incidentes)
- [Logs](#logs)
- [Métricas](#métricas)
- [Monitores](#monitores)
- [Funções](#funções)
- [Análise de Causa Raiz](#análise-de-causa-raiz)
- [Verificações de Serviço](#verificações-de-serviço)
- [Dependências de Serviço](#dependências-de-serviço)
- [SLO (Service Level Objectives)](#slo)
- [Tags](#tags)
- [Traces](#traces)
- [Uso](#uso)
- [Usuários](#usuários)

## Alertas

O módulo `alerts.py` fornece funcionalidades para gerenciamento de alertas:

- **mute_alert**: Silencia um alerta específico para um monitor
- **unmute_alert**: Remove o silenciamento de um alerta

## APM

O módulo `apm.py` oferece ferramentas para monitoramento de desempenho de aplicações:

- **list_apm_traces**: Lista traces APM com base em uma query
- **get_apm_trace_details**: Obtém detalhes de um trace específico
- **summarize_apm_traces**: Gera resumo estatístico dos traces
- **query_apm_errors**: Consulta métricas de erro para um serviço
- **query_apm_latency**: Consulta métricas de latência para um serviço
- **query_apm_spans**: Consulta spans para um serviço específico

## Dashboards

O módulo `dashboard.py` permite gerenciar dashboards:

- **list_dashboards**: Lista dashboards com filtros por nome e tags
- **list_prompts**: Lista prompts disponíveis (placeholder)

## Downtime

O módulo `downtime.py` gerencia períodos de inatividade programada:

- **create_downtime**: Cria um novo período de downtime
- **update_downtime**: Atualiza um downtime existente
- **cancel_downtime**: Cancela um downtime específico

## Eventos

O módulo `events.py` gerencia eventos:

- **search_events**: Pesquisa eventos com base em critérios
- **get_event**: Obtém detalhes de um evento específico
- **delete_event**: Remove um evento

## Hosts

O módulo `host.py` fornece funcionalidades para gerenciamento de hosts:

- **list_hosts**: Lista hosts com filtros e ordenação
- **get_host_totals**: Obtém totais relacionados aos hosts
- **mute_host**: Silencia um host específico
- **unmute_host**: Remove o silenciamento de um host

## Incidentes

O módulo `incident.py` gerencia incidentes:

- **search_incidents**: Pesquisa incidentes
- **list_incidents**: Lista todos os incidentes
- **get_incident**: Obtém detalhes de um incidente
- **update_incident**: Atualiza um incidente
- **delete_incident**: Remove um incidente

## Logs

O módulo `logs.py` gerencia logs:

- **archive_logs**: Arquiva logs com base em critérios específicos

## Métricas

O módulo `metrics.py` fornece funcionalidades para métricas:

- **query_metrics**: Consulta métricas com base em uma query
- **list_metrics**: Lista métricas disponíveis
- **update_metric_metadata**: Atualiza metadados de uma métrica
- **delete_metric_metadata**: Remove metadados de uma métrica
- **query_p99_latency**: Consulta latência P99
- **query_error_rate**: Consulta taxa de erro
- **query_downstream_latency**: Consulta latência downstream

## Monitores

O módulo `monitor.py` gerencia monitores:

- **create_monitor**: Cria um novo monitor
- **delete_monitor**: Remove um monitor
- **get_monitor_status**: Obtém status de monitores
- **update_monitor**: Atualiza um monitor
- **create_monitor_config_policy**: Cria política de configuração
- **update_monitor_config_policy**: Atualiza política de configuração
- **delete_monitor_config_policy**: Remove política de configuração
- **list_monitor_config_policies**: Lista políticas de configuração
- **search_monitors**: Pesquisa monitores
- **get_monitor**: Obtém detalhes de um monitor

## Funções

O módulo `roles.py` gerencia funções:

- **list_roles**: Lista todas as funções
- **get_role**: Obtém detalhes de uma função
- **create_role**: Cria uma nova função
- **delete_role**: Remove uma função
- **update_role**: Atualiza uma função existente

## Análise de Causa Raiz

O módulo `root_cause.py` fornece análise de causa raiz:

- **analyze_service_with_apm**: Analisa um serviço usando dados APM

## Verificações de Serviço

O módulo `service_checks.py` gerencia verificações de serviço:

- **submit_service_check**: Envia uma verificação de serviço
- **list_service_checks**: Lista verificações de serviço

## Dependências de Serviço

O módulo `service_dependencies.py` gerencia dependências entre serviços:

- **list_service_dependencies**: Lista dependências de um serviço
- **create_service_dependency**: Cria uma nova dependência
- **delete_service_dependency**: Remove uma dependência

## SLO

O módulo `slo.py` gerencia objetivos de nível de serviço:

- **list_slos**: Lista SLOs com filtros
- **get_slo**: Obtém detalhes de um SLO
- **delete_slo**: Remove um SLO

## Tags

O módulo `tags.py` gerencia tags:

- **list_host_tags**: Lista tags de hosts
- **add_host_tags**: Adiciona tags a um host
- **delete_host_tags**: Remove tags de um host

## Traces

O módulo `trace.py` gerencia traces:

- **list_traces**: Lista traces com filtros
- **get_trace_details**: Obtém detalhes de um trace
- **summarize_traces**: Gera resumo de traces

## Uso

O módulo `usage.py` fornece métricas de uso:

- **get_hourly_usage**: Obtém uso por hora

## Usuários

O módulo `users.py` gerencia usuários:

- **list_users**: Lista todos os usuários
- **get_user**: Obtém detalhes de um usuário