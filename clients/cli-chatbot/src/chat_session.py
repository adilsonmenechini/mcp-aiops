import logging
import json
from typing import List, Dict, Any

from src.service.server import Server
from src.model.llm_client import LLMClient

class ChatSession:
    """
    Gere a interação geral do chat, orquestrando a comunicação
    entre o utilizador, o LLM e os servidores/ferramentas MCP.
    """
    def __init__(self, servers: List[Server], llm_client: LLMClient, sre_system_prompt: str = "", llm_config_params: Dict[str, Any] = None) -> None:
        self.servers: List[Server] = servers
        self.llm_client: LLMClient = llm_client
        self.messages: List[Dict[str, str]] = [] # Armazena o histórico do chat
        self.sre_system_prompt = sre_system_prompt # Armazena o prompt SRE
        self.tool_map: Dict[str, Server] = {} # Mapa para acesso rápido às ferramentas
        self.llm_config_params = llm_config_params or {}

    async def cleanup_servers(self) -> None:
        """
        Garante que todos os servidores MCP inicializados sejam devidamente limpos.
        """
        logging.info("A iniciar a limpeza dos servidores...")
        for server in reversed(self.servers):
            try:
                await server.cleanup()
            except Exception as e:
                logging.warning(f"Aviso durante a limpeza final do servidor {server.name}: {e}")
        logging.info("Todos os servidores limpos.")

    async def process_llm_response(self, llm_response: str) -> str:
        """
        Processa a resposta do LLM. Se for uma chamada de ferramenta, executa a ferramenta.
        Caso contrário, retorna a resposta de texto do LLM.
        """
        if not llm_response:
            logging.error("O LLM não forneceu uma resposta.")
            return "O LLM não respondeu ou ocorreu um erro."
        
        logging.debug(f"ChatSession - Processing LLM response: {llm_response[:200]}...")
        
        # Tenta remover o bloco de código markdown, se presente
        stripped_response = llm_response.strip()
        if stripped_response.startswith("```json") and stripped_response.endswith("```"):
            stripped_response = stripped_response[len("```json"):-len("```")].strip()
            logging.debug(f"ChatSession - Markdown removido da resposta do LLM. Nova resposta: {stripped_response}")

        # Verifica se parece com JSON antes de tentar fazer parse
        if stripped_response.startswith("{") and stripped_response.endswith("}"):
            logging.debug("ChatSession - Response appears to be JSON, attempting to parse...")
        else:
            logging.debug("ChatSession - Response does not appear to be JSON, treating as natural language")
            return llm_response

        try:
            tool_call = json.loads(stripped_response) # Usa a resposta sem markdown aqui
            logging.debug(f"ChatSession - Successfully parsed JSON: {tool_call}")
            
            if "tool" in tool_call and "arguments" in tool_call:
                logging.info(f"ChatSession - LLM solicitou a execução da ferramenta: {tool_call['tool']}")
                logging.info(f"ChatSession - Argumentos: {tool_call['arguments']}")

                tool_name = tool_call["tool"]
                server = self.tool_map.get(tool_name)
                
                logging.debug(f"ChatSession - Available tools in tool_map: {list(self.tool_map.keys())}")

                if server:
                    try:
                        logging.debug(f"ChatSession - Executing tool '{tool_name}' on server '{server.name}'")
                        result = await server.execute_tool(tool_name, tool_call["arguments"])
                        logging.info(f"ChatSession - Execução da ferramenta '{tool_name}' bem-sucedida. Resultado: {result}")
                        return f"Resultado da execução da ferramenta: {result}"
                    except Exception as e:
                        error_msg = f"Erro ao executar a ferramenta '{tool_name}': {str(e)}"
                        logging.error(f"ChatSession - {error_msg}")
                        return error_msg
                
                logging.error(f"ChatSession - Nenhum servidor encontrado com a ferramenta: {tool_name}")
                return f"Nenhum servidor encontrado com a ferramenta: {tool_name}"
            else:
                logging.debug("ChatSession - JSON parsed but missing 'tool' or 'arguments' keys")
                return llm_response # Não é uma chamada de ferramenta, retorna como está (resposta original, sem remover markdown)
        except json.JSONDecodeError as e:
            # Se não for um JSON válido mesmo após remover markdown, trata como resposta em linguagem natural
            logging.debug(f"ChatSession - JSON decode error: {e}. Treating as natural language.")
            return llm_response
        except Exception as e:
            logging.error(f"ChatSession - Ocorreu um erro inesperado ao processar a resposta do LLM: {e}")
            return f"Ocorreu um erro interno: {e}"


    async def start(self) -> None:
        """
        Inicia o loop principal do chat, inicializando servidores e gerindo interações.
        """
        try:
            # Inicializa todos os servidores
            for server in self.servers:
                try:
                    await server.initialize()
                except Exception as e:
                    logging.error(f"Falha ao inicializar o servidor {server.name}: {e}. A abortar a sessão de chat.")
                    await self.cleanup_servers()
                    return

            # Agrega todas as ferramentas, cria o mapa de ferramentas e a descrição para o LLM
            all_tools_desc: List[str] = []
            for server in self.servers:
                tools = await server.list_tools()
                for tool in tools:
                    self.tool_map[tool.name] = server
                    all_tools_desc.append(tool.format_for_llm())
            tools_description = "\n".join(all_tools_desc)

            # Mensagem base do sistema para o papel do assistente e uso de ferramentas
            base_system_message = (
                "Você é um assistente SRE especialista integrado com o Protocolo de Contexto do Modelo (MCP), "
                "com acesso a várias ferramentas e recursos para ajudar em tarefas específicas.\n\n"
                "📚 FERRAMENTAS DISPONÍVEIS:\n"
                f"{tools_description}\n\n"
                "🔧 INSTRUÇÕES CRÍTICAS PARA USO DE FERRAMENTAS:\n\n"
                "QUANDO PRECISAR USAR UMA FERRAMENTA:\n"
                "1. Responda EXCLUSIVAMENTE com um JSON válido no formato exato:\n"
                "{\n"
                '  "tool": "nome_exato_da_ferramenta",\n'
                '  "arguments": {\n'
                '    "parametro1": "valor1",\n'
                '    "parametro2": "valor2"\n'
                "  }\n"
                "}\n\n"
                "2. REGRAS OBRIGATÓRIAS:\n"
                "   - Use APENAS o nome exato da ferramenta listada acima\n"
                "   - Inclua TODOS os parâmetros obrigatórios\n"
                "   - NÃO adicione texto antes ou depois do JSON\n"
                "   - NÃO use markdown ou formatação\n"
                "   - O JSON deve ser válido e bem formado\n\n"
                "3. QUANDO NÃO USAR FERRAMENTAS:\n"
                "   - Para conversas normais, responda em texto natural\n"
                "   - Para explicações, use linguagem natural\n"
                "   - Para resumos de resultados, use texto natural\n\n"
                "⚠️ CRÍTICO: Se você decidir usar uma ferramenta, sua resposta deve conter APENAS o JSON, nada mais."
            )

            # Combina o prompt do sistema SRE com a mensagem base do sistema
            # O prompt SRE é precedido para lhe dar maior prioridade
            if self.sre_system_prompt:
                final_system_message = f"{self.sre_system_prompt}\n\n{base_system_message}"
            else:
                final_system_message = base_system_message

            # Adiciona a mensagem final do sistema como a primeira mensagem do 'model'
            # Este papel 'model' será interpretado como uma SystemMessage pelos clientes LangChain
            # (Gemini, Ollama, Anthropic) em src/model/llm_clients.
            self.messages.append({"role": "model", "content": final_system_message})
            logging.info("Mensagem do sistema adicionada ao histórico do chat.")

            while True:
                try:
                    user_input = input("Você: ").strip()
                    if user_input.lower() in ["sair", "exit"]:
                        logging.info("\nA sair da sessão de chat...")
                        break

                    # Adiciona a entrada do utilizador ao histórico do chat
                    self.messages.append({"role": "user", "content": user_input})
                    print("\n🧠 A pensar...")

                    # Obtém a resposta do LLM, passando os parâmetros configurados
                    llm_response = self.llm_client.get_response(self.messages, **self.llm_config_params)
                    if not llm_response:
                        logging.error("A resposta do LLM é Nula. A ignorar a iteração.")
                        # Remove a última mensagem do utilizador se o LLM não respondeu
                        if self.messages and self.messages[-1]["role"] == "user":
                            self.messages.pop()
                        continue
                    # Exibe a resposta bruta do LLM (para depuração/visibilidade, se necessário)
                    logging.info("\n🤖 Resposta Bruta do Assistente: %s", llm_response)


                    # Processa a resposta do LLM (chamada de ferramenta ou linguagem natural)
                    processed_result = await self.process_llm_response(llm_response)

                    if processed_result != llm_response:
                        # Se uma ferramenta foi executada, a resposta do LLM foi uma chamada de ferramenta.
                        # Anexamos a própria chamada de ferramenta e, em seguida, o resultado da ferramenta.
                        self.messages.append({"role": "model", "content": llm_response}) # A chamada de ferramenta do LLM
                        self.messages.append({"role": "user", "content": processed_result}) # O resultado da execução da ferramenta

                        # Obtém uma resposta final em linguagem natural do LLM, incorporando o resultado da ferramenta
                        print("\n✨ A obter a resposta final do LLM...")
                        final_llm_response = self.llm_client.get_response(self.messages, **self.llm_config_params)
                        if final_llm_response:
                            logging.info("\n✨ Resposta Final do Assistente: %s", final_llm_response)
                            print(f"\n✨ Resposta Final do Assistente: {final_llm_response}")
                        else:
                            logging.warning("A resposta final do LLM foi Nula após a execução da ferramenta.")
                            print(f"\nResultado da Ferramenta: {processed_result}")
                            self.messages.append({"role": "model", "content": f"Resultado da Ferramenta: {processed_result}"})

                    else:
                        # Se nenhuma ferramenta foi executada, a resposta do LLM foi em linguagem natural.
                        logging.info("\n🤖 Assistente: %s", llm_response)
                        print(f"\n🤖 Assistente: {llm_response}")
                        self.messages.append({"role": "model", "content": llm_response})

                except KeyboardInterrupt:
                    logging.info("\nKeyboardInterrupt detetado. A sair...")
                    break
                except Exception as e:
                    logging.error(f"Ocorreu um erro não tratado no loop do chat: {e}")
                    # Opcionalmente, remove a última mensagem do utilizador para evitar ficar preso
                    if self.messages and self.messages[-1]["role"] == "user":
                        self.messages.pop()
                    print(f"\nOcorreu um erro: {e}. Por favor, tente novamente.")

        finally:
            await self.cleanup_servers()
