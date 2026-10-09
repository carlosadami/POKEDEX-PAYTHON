# Pokédex em Python

Checkpoint 5 - Computational Thinking With Python

## Problema

Quem joga Pokémon e quer montar um time precisa saber o tipo, as habilidades e o poder de cada Pokémon, e às vezes não sabe qual de dois Pokémon é mais forte. Procurar isso em vários sites demora.

Nosso programa resolve isso pelo terminal: dá para ver a lista de Pokémon com o número de cada um, buscar um Pokémon pelo nome ou número, comparar dois Pokémon para ver qual é mais forte e guardar os Pokémon pesquisados em um arquivo JSON.

## API escolhida

Usamos a **PokéAPI**, uma API pública e gratuita com dados de todos os Pokémon. Ela não precisa de cadastro nem de chave, e as respostas vêm em JSON.

- Site: https://pokeapi.co/
- Documentação: https://pokeapi.co/docs/v2

Endpoints usados:

- `https://pokeapi.co/api/v2/pokemon?limit=20&offset=0` → lista de Pokémon, 20 por vez
- `https://pokeapi.co/api/v2/pokemon/{nome ou número}` → dados de um Pokémon (ex.: `/pokemon/pikachu`)

Do JSON que a API devolve, usamos os campos `id`, `name`, `types`, `abilities`, `height`, `weight` e `stats`. Com os status (HP, ataque, defesa e velocidade) o programa calcula o **poder total**, que é a soma deles. A altura vem em decímetros e o peso em hectogramas, por isso o programa divide os dois por 10 para mostrar em metros e quilos.

## Como o programa funciona

O programa usa a biblioteca `requests` para fazer as requisições. A função `pegar_dados()` faz o `requests.get()`, confere o código de status e transforma a resposta em dicionário com `.json()`.

Funções principais:

- `pegar_dados()`: faz a requisição na API e trata os erros
- `mostrar_lista()`: mostra os Pokémon com número e nome, de 20 em 20
- `organizar()`: pega do JSON só os dados que vamos usar
- `mostrar()`: mostra na tela o tipo, as habilidades, a altura, o peso, os status e o poder total
- `comparar()`: compara o poder total de dois Pokémon e mostra qual é o mais forte
- `salvar()` e `carregar()`: salvam e leem o arquivo `pokemons.json`

## Tratamento de erros

- Pokémon que não existe (erro 404) → mostra uma mensagem
- Outros erros da API → mostra o código do erro
- Sem internet → `ConnectionError`
- API demorando → `Timeout`
- Arquivo JSON não existe ou está com problema → começa com a lista vazia
- Erro ao salvar o arquivo → mostra uma mensagem

## Arquivo JSON

O `pokemons.json` tem os dados dos Pokémon que buscamos na API. Cada Pokémon pesquisado é salvo nele.

## Como executar

```
pip install -r requirements.txt
python main.py
```
