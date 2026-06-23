# BD2 Lab02 - Grupo 2

Projeto da disciplina de Bases de Dados II com foco em:

- ambiente distribuido com MySQL (no principal + replicas)
- carga inicial de dados SQL
- validacao de conectividade entre nos
- experimentos de transacoes distribuidas
- suporte a componente NoSQL (MongoDB) para a parte 2

## Estrutura do projeto

```text
conclusoes/
  docker-compose.yml
  dados/
    mercadokwanza_p1.sql
    mercadokwanza_p2.sql
  relatorio/
  scripts/
    migracao.py
    replicacao.sql
    test_conexao.py
    transacao.py
```

## Arquitetura (Docker)

Servicos definidos em `conclusoes/docker-compose.yml`:

- `mysql-luanda` (container `no-luanda`) - MySQL principal
  - host port: `3307`
- `mysql-benguela` (container `no-benguela`) - replica
  - host port: `3308`
- `mysql-huambo` (container `no-huambo`) - replica
  - host port: `3309`
- `mongodb` (container `mongo-kwanza`) - apoio NoSQL
  - host port: `27017`

Credenciais MySQL usadas no compose e scripts:

- user: `root`
- password: `kwanza2024`
- database: `mercadokwanza`

## Pre-requisitos

- Docker Desktop (ou Docker Engine + Compose)
- Python 3.10+ (recomendado)
- pip

Dependencia Python:

```bash
pip install mysql-connector-python
```

## Como executar

### 1. Subir os containers

Na pasta `conclusoes`:

```bash
docker compose up -d
```

### 2. Confirmar se os servicos estao ativos

```bash
docker compose ps
```

### 3. Verificar conectividade MySQL

Na pasta `conclusoes/scripts`:

```bash
python test_conexao.py
```

Espera-se conexao com as portas `3307` e `3308` (de acordo com o script atual).

### 4. Executar experimento de transacao

```bash
python transacao.py
```

O script tenta:

- bloquear e verificar stock em Benguela
- decrementar stock
- registar venda em Luanda
- efetuar `COMMIT` em ambos os nos
- ou `ROLLBACK` em caso de erro

## Carga de dados

Os ficheiros SQL em `conclusoes/dados` sao carregados automaticamente na inicializacao dos containers MySQL via:

- volume `./dados:/docker-entrypoint-initdb.d`

Se precisar recarregar os dados do zero:

```bash
docker compose down -v
docker compose up -d
```

## Parar ambiente

Na pasta `conclusoes`:

```bash
docker compose down
```

Para remover tambem os volumes:

```bash
docker compose down -v
```

## Troubleshooting rapido

- Porta ocupada (`3307`, `3308`, `3309` ou `27017`):
  - altera o mapeamento de portas no `docker-compose.yml`
- Erro de ligacao no Python:
  - confirma se os containers estao em estado `Up`
  - confirma se instalaste `mysql-connector-python`
- Dados nao atualizam como esperado:
  - recria o ambiente com `docker compose down -v` e sobe novamente

## Notas

- Os scripts `migracao.py` e `replicacao.sql` existem no repositorio, mas estao vazios no estado atual.
- O diretorio `conclusoes/relatorio` esta reservado para a documentacao final do trabalho.
