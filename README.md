### Desafio Técnico Luizalabs

Este repositório possui o projeto referente ao desafio técnico da Luiz Labs, onde consistia em desenvolver uma api
responsável por gerir clientes e sua lista de produtos favoritos. Algumas considerações:

## Linhas Gerais

- Utilizei o padrão JWT para gerir a autenticação da API;
- MySQL como database

## Estrutura do projeto

### Diretório App

Diretório raiz do projeto onde se encontra todo o código fonte

### Diretório App -> Settings

Neste diretório estão armazenadas as configurações que irão ser adicionadas ao Flask

- Base - São as configurações gerais pra todos os ambientes
- Local - São as configurações para a execução do projeto localmente
- Test - São as configurações para a execução dos testes

Aqui você podemos adicionar as configurações para o ambiente de release e production,
trocando as informações do database pra cada ambiente por exemplo;

### Diretório App -> Presentation

Este diretório é responsável por conter qualquer representação a ser retornada pelos endpoints, eu escolhi retornar
o json gerado diretamente pelo objeto de dominio, mas poderíamos criar as representações dos dominios, mapeá-las e
retorná-las ao invés dos objetos de domínio;

- BaseResponseException - Representa a classe Base de um objeto customizado a ser retornado quando ocorre um erro
  nos endpoints

### Diretório App -> Helpers

Este diretório é responsável por conter algumas funções que são frequentemente usadas no projeto e server de auxílio
para diversas rotinas;

### Diretório App -> Infrastructure

Este diretório eu normalmente utilizo para implementações que dependam de referências externas, para deixar a
camada de domínio o mais pura possível.

Para que isso aconteça, a camada de domínio define contratos a serem cumpridos e as classes que possuem
dependências externas e serão utilizadas pelo domínio, implementam esses contratos e são injetadas para serem usadas;

### Diretório App -> Domain

Este diretório é responsável por conter todas as classes que representam o domínio da aplicação:

- Temos 4 entidades:

  **Customer**: que representa o cliente e tem acesso apenas aos dados pertencentes a ele;

  **User**: que representa o usuário administrativo da Luiza Labs e tem acesso apenas aos dados pertencentes a ele,
  ou dependendo da permissão pode ter acesso a dados de clientes e de outros usuários;

  **Roles**: Representa as permissões do usuário administrativo. Para poder alterar, excluir qualquer entidade que não
  seja a dele própria, o User precisa ter a role SUPER_USER e pra visualizar apenas basta a role ADMIN;

  **WishList**: Que representa a coleção de produtos favoritos do customer originários da api (http://challenge-api.luizalabs.com/api/product/)

### Diretório App -> Controllers

Diretório onde se encontra as implementações dos endpoints

### Diretório App -> Commands

Diretório que contém as implementações de alguns comandos customizados. Nele temos o comando customizado para popular a
base com alguns dados iniciais, além de criar toda a sua estrutura. Esse comando vai ser mapeado depois para o makefile.

## Diretório Config

Diretório responsável por conter as dependências do projeto;

- Existem 2 arquivos que indicam as dependências do projeto:
  - requirements.txt - São aquelas dependências necessárias para rodar o projeto;
  - build_requirements.txt - São aquelas dependências responsáveis por implementar os testes, code style e etc...;

## Diretório Migration

Aqui nesse diretório se encontram as migrations do database, eu configurei como a pasta padrão da library Alembic que é
responsável por manter essas informações. O conteúdo é gerado automaticamente pela lib;

## Diretório Test

Diretório onde se encontra todos os testes das controllers;

###Commandos
Eu fiz o mapeamento dos comandos mais frequentes e fiz a junção de alguns para facilitar o desenvolvimento, execução e
testes e coloquei dentro do makefile, caso você tenha windows, basta ver os comandos mapeados e executar a versão pura deles.

Para executar o projeto sem maiores esforços, basta executar o comando:

`make run`

Aqui ele irá adicionar alguns dados padrões:

User:
<br />
email: luke@luizalabs.com.br
<br />
password: darthVaderIsMyFather

Customer:
<br />
email: anakin@starwars.com.br
<br />
password: iAmDarthVader

Para executar os testes basta executar o comando abaixo:

`make test`

Para inicializar o banco criando a estrutura e adicionando os dados padrões, basta executar:

`make db/initialize`

Para aplicar todas as migrations:

`make db/migrate`

Para criar uma migration:

`make db/migration name=nome_da_migration`

## Endpoints

### Authorization

#### Customer

**URL**: METHOD POST - /api/auth/customer/token
<br />
**Request**:
<br />
```json
{ 
  "email": "anakin@starwars.com.br", 
  "password": "iAmDarthVader" 
}

```
<br />

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDY3NTM4MzgsIm5iZiI6MTYwNjc1MzgzOCwianRpIjoiZTRlMGFjNDAtNjMwYi00ZTZlLTgwMzktYjJjMTRiYmEzZDgxIiwiZXhwIjoxNjA2NzU0NzM4LCJpZGVudGl0eSI6eyJpZCI6MSwidXBkYXRlZF9kYXRlIjpudWxsLCJlbWFpbCI6Imx1a2VAbHVpemFsYWJzLmNvbS5iciIsIm5hbWUiOiJMdWtlIFNreXdhbGtlciIsInJvbGVzIjpbeyJjYXRlZ29yeSI6IkFETUlOIn0seyJjYXRlZ29yeSI6IlNVUEVSX1VTRVIifV0sImNyZWF0ZWRfZGF0ZSI6IjIwMjAtMTEtMzAgMTY6MzA6MzUiLCJkZWxldGVkX2RhdGUiOm51bGx9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJyb2xlcyI6WyJBRE1JTiIsIlNVUEVSX1VTRVIiXX19.XHogF2h605mapxX557974DhWI_uoBQhiATeb2n22Od0"
}

```
<br />

#### User

**URL**: METHOD POST - /api/auth/customer/token
<br />
**Request**:
<br />
```json
{ 
  "email": "luke@luizalabs.com.br", 
  "password": "darthVaderIsMyFather" 
}
```
<br />

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDY3NTM4MzgsIm5iZiI6MTYwNjc1MzgzOCwianRpIjoiZTRlMGFjNDAtNjMwYi00ZTZlLTgwMzktYjJjMTRiYmEzZDgxIiwiZXhwIjoxNjA2NzU0NzM4LCJpZGVudGl0eSI6eyJpZCI6MSwidXBkYXRlZF9kYXRlIjpudWxsLCJlbWFpbCI6Imx1a2VAbHVpemFsYWJzLmNvbS5iciIsIm5hbWUiOiJMdWtlIFNreXdhbGtlciIsInJvbGVzIjpbeyJjYXRlZ29yeSI6IkFETUlOIn0seyJjYXRlZ29yeSI6IlNVUEVSX1VTRVIifV0sImNyZWF0ZWRfZGF0ZSI6IjIwMjAtMTEtMzAgMTY6MzA6MzUiLCJkZWxldGVkX2RhdGUiOm51bGx9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJyb2xlcyI6WyJBRE1JTiIsIlNVUEVSX1VTRVIiXX19.XHogF2h605mapxX557974DhWI_uoBQhiATeb2n22Od0"
}

```
### Customer

#### Add

**URL**: METHOD POST - /api/customer
<br />
**Request**:
<br />
```json
{
  "name": "Leia Organa",
  "email": "leia@starwars.com.br",
  "password": "youAreMyOnlyHope"
}

```
<br />

**Response**:
```json
{
  "created_date": "2020-11-28 22:45:53",
  "deleted_date": null,
  "email": "leia@starwars.com.br",
  "id": 2,
  "name": "Leia Organa",
  "updated_date": null
}

```

#### Update

**HEADER** : Authorization Bearer CUSTOMER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD PUT - /api/customer
<br />
**Request**:
<br />
```json
{
  "name": "Leia B",
  "email": "leia@stawars.com.br"
}

```
<br />

**Response**:
```json
{
  "created_date": "2020-11-28 19:50:56",
  "deleted_date": null,
  "email": "leia@stawars.com.br",
  "id": 1,
  "name": "Leia B",
  "updated_date": "2020-11-28 20:01:12"
}

```
#### Update - SuperUser

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD PUT - /api/customer/[user_id]
<br />
**Request**:
<br />
```json
{
  "name": "Leia B",
  "email": "leia@stawars.com.br"
}

```
<br />

**Response**:
```json
{
  "created_date": "2020-11-28 19:50:56",
  "deleted_date": null,
  "email": "leia@stawars.com.br",
  "id": 1,
  "name": "Leia B",
  "updated_date": "2020-11-28 20:01:12"
}

```

#### Change Password

**HEADER** : Authorization Bearer CUSTOMER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD PUT - /api/customer/password
<br />
**Request**:
<br />
```json
{
  "password": "iamDarthVader",
  "new_password": "iamVader"
}

```
<br />

**Response**:
```json
{}

```

#### Delete

**HEADER** : Authorization Bearer CUSTOMER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD DELETE - /api/customer
<br />
**Response**:
```json
{}
```

#### Delete - SuperUser

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD DELETE - /api/customer/[user_id]
<br />
**Response**:
```json
{}
```

#### Get

**HEADER** : Authorization Bearer CUSTOMER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/customer
<br />
**Response**:
```json
{
  "created_date": "2020-11-28 19:50:56",
  "deleted_date": null,
  "email": "anakin@starwars.com.br",
  "id": 1,
  "name": "Anakin Skywalker",
  "updated_date": null
}
```
#### Get Customer by Email - SuperUser

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/customer/email/[email]
<br />
**Response**:
```json
{
  "created_date": "2020-11-28 20:00:02",
  "deleted_date": null,
  "email": "leia@starwars.com.br",
  "id": 2,
  "name": "Leia Organa",
  "updated_date": null
}
```

#### Get Customer by ID - SuperUser

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/customer/[id]
<br />
**Response**:
```json
{
  "created_date": "2020-11-28 20:00:02",
  "deleted_date": null,
  "email": "leia@starwars.com.br",
  "id": 2,
  "name": "Leia Organa",
  "updated_date": null
}
```

#### Get Customers - SuperUser

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/customer/[offset]/[limit]
<br />
**Response**:
```json
[{
  "created_date": "2020-11-28 20:00:02",
  "deleted_date": null,
  "email": "leia@starwars.com.br",
  "id": 2,
  "name": "Leia Organa",
  "updated_date": null
}]
```

### User
#### Add
**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD POST - /api/user
<br />
**Request**:
<br />
```json
{
	"name": "Anakin Skywalker",
	"email": "ana@luizalabs.com.br",
	"password": "iamDarthVader",
	"roles" : ["ADMIN"]
}

```
<br />

**Response**:
```json
{
  "created_date": "2020-11-28 22:46:06",
  "deleted_date": null,
  "email": "ana@luizalabs.com.br",
  "id": 2,
  "name": "Anakin Skywalker",
  "roles": [
    {
      "category": "ADMIN"
    }
  ],
  "updated_date": null
}

```

#### Update

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD PUT - /api/user
<br />
**Request**:
<br />
```json
{
	"name": "Darth Vader",
	"email": "darth@luizalabs.com.br",
	"roles" : ["CUSTOMER_EXPERIENCE"]
}

```
<br />

**Response**:
```json
{
  "created_date": "2020-11-28 18:13:14",
  "deleted_date": null,
  "email": "darth@luizalabs.com.br",
  "id": 1,
  "name": "Darth Vader",
  "roles": [
    {
      "category": "ADMIN"
    },
    {
      "category": "CUSTOMER_EXPERIENCE"
    },
    {
      "category": "SUPER_USER"
    }
  ],
  "updated_date": "2020-11-28 18:25:11"
}

```

#### Change Password

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD PUT - /api/user/password
<br />
**Request**:
<br />
```json
{
  "password": "iamDarthVader",
  "new_password": "iamVader"
}

```
<br />

**Response**:
```json
{}

```

#### Delete

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD DELETE - /api/user
<br />
**Response**:
```json
{}
```


#### Get

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/user
<br />
**Response**:
```json
{
  "created_date": "2020-11-28 18:13:14",
  "deleted_date": null,
  "email": "darth@luizalabs.com.br",
  "id": 1,
  "name": "Darth Vader",
  "roles": [
    {
      "category": "ADMIN"
    },
    {
      "category": "CUSTOMER_EXPERIENCE"
    },
    {
      "category": "SUPER_USER"
    }
  ],
  "updated_date": "2020-11-28 18:25:11"
}
```

#### Get User by Email - SuperUser

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/user/email/[email]
<br />
**Response**:
```json
{
  "created_date": "2020-11-28 18:24:41",
  "deleted_date": null,
  "email": "ana@luizalabs.com.br",
  "id": 2,
  "name": "Anakin Skywalker",
  "roles": [
    {
      "category": "ADMIN"
    }
  ],
  "updated_date": null
}
```

#### Get User by ID - SuperUser

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/user/[id]
<br />
**Response**:
```json
{
  "created_date": "2020-11-28 18:24:41",
  "deleted_date": null,
  "email": "ana@luizalabs.com.br",
  "id": 2,
  "name": "Anakin Skywalker",
  "roles": [
    {
      "category": "ADMIN"
    }
  ],
  "updated_date": null
}
```

#### Get Users - SuperUser

**HEADER** : Authorization Bearer USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/user/[offset]/[limit]
<br />
**Response**:
```json
[[
  {
    "created_date": "2020-11-28 18:13:14",
    "deleted_date": null,
    "email": "luke@luizalabs.com.br",
    "id": 1,
    "name": "Luke Skywalker",
    "roles": [
      {
        "category": "ADMIN"
      },
      {
        "category": "SUPER_USER"
      }
    ],
    "updated_date": null
  },
  {
    "created_date": "2020-11-28 18:24:41",
    "deleted_date": null,
    "email": "ana@luizalabs.com.br",
    "id": 2,
    "name": "Anakin Skywalker",
    "roles": [
      {
        "category": "ADMIN"
      }
    ],
    "updated_date": null
  }
]]
```
### Product
#### Get by id
**HEADER** : Authorization Bearer CUSTOMER_AUTHORIZATION_TOKEN OR USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/product/[id]
<br />
**Response**:
```json
{
  "brand": "burigotto",
  "id": "ddeb989e-53c4-e68b-aa93-6e43afddb797",
  "image": "http://challenge-api.luizalabs.com/images/ddeb989e-53c4-e68b-aa93-6e43afddb797.jpg",
  "price": 704.8,
  "title": "Cadeira para Auto Burigotto Matrix p/ Crianças"
}
```

#### Get products
**HEADER** : Authorization Bearer CUSTOMER_AUTHORIZATION_TOKEN OR USER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/product/[page]
<br />
**Response**:
```json
{
  "meta": {
    "page_number": 2,
    "page_size": 100
  },
  "products": [
    {
      "brand": "burigotto",
      "id": "ddeb989e-53c4-e68b-aa93-6e43afddb797",
      "image": "http://challenge-api.luizalabs.com/images/ddeb989e-53c4-e68b-aa93-6e43afddb797.jpg",
      "price": 704.8,
      "title": "Cadeira para Auto Burigotto Matrix p/ Crianças"
    },
    {
      "brand": "elg",
      "id": "de2911eb-ce5c-e783-1ca5-82d0ccd4e3d8",
      "image": "http://challenge-api.luizalabs.com/images/de2911eb-ce5c-e783-1ca5-82d0ccd4e3d8.jpg",
      "price": 39.9,
      "title": "Película Protetora para Samsung Galaxy S6"
    }
]
}
```

### WishList
#### Add
**HEADER** : Authorization Bearer CUSTOMER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD POST - /api/wishlist/product/[product_id]
<br />
**Response**:
```json
{
  "id": 2,
  "product_id": "958ec015-cfcf-258d-c6df-1721de0ab6ea"
}
```

#### Delete
**HEADER** : Authorization Bearer CUSTOMER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD DELETE - /api/wishlist/product/[product_id]
<br />
**Response**:
```json
{
  "id": 2,
  "product_id": "958ec015-cfcf-258d-c6df-1721de0ab6ea"
}
```
#### Get Wishlist
**HEADER** : Authorization Bearer CUSTOMER_AUTHORIZATION_TOKEN
<br />
**URL**: METHOD GET - /api/wishlist/[offset]/[limit]
<br />
**Response**:
```json
[{
  "id": 2,
  "product_id": "958ec015-cfcf-258d-c6df-1721de0ab6ea"
}]
```

