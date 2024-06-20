# Haversine BR

Este projeto é uma API construída com FastAPI que calcula as distâncias entre todas as cidades do Brasil usando a biblioteca `haversine` e armazena os resultados em um banco de dados Redis. A API permite consultar as cidades mais próximas de uma cidade específica.

## Requisitos

- Docker
- Docker Compose
- Make

## Instalação

Clone o repositório:

```
git clone https://github.com/pedromenezes/haversine-br.git
cd haversine-br
```

Construa e inicie os contêineres:

```
make up
```

## Uso

A API estará disponível em http://localhost:8000.

### Endpoints Disponíveis

- **GET /**: Endpoint raiz que retorna uma mensagem de boas-vindas.
- **GET /nearest_cities/{city_name}**: Retorna as cidades mais próximas da cidade especificada.

## Exemplo de Requisição

Para obter as cidades mais próximas de uma cidade específica:

```
curl -X 'GET' \
  'http://localhost:8000/nearest_cities/Sao_Paulo?max_results=5' \
  -H 'accept: application/json'
```

## Executando os Testes

```
make test
```

## Parando os Contêineres

Para parar e remover os contêineres:

```
make down
```

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.
