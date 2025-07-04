# Módulos MCP User DB

Este documento descreve os módulos disponíveis no servidor MCP User DB para gerenciamento de usuários.

## Ferramentas

- **create_user**: Cria um novo usuário no banco de dados.
  - `name` (str): Nome do usuário.
  - `email` (str): E-mail do usuário (deve ser único).

- **list_users**: Lista todos os usuários cadastrados.
  - Nenhum argumento.

- **get_user_by_email**: Busca um usuário específico pelo seu e-mail.
  - `user_email` (str): O e-mail do usuário a ser buscado.