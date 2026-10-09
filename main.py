# Pokédex em Python
# API: PokéAPI - https://pokeapi.co/

import json
import requests

URL = "https://pokeapi.co/api/v2/"
ARQUIVO = "pokemons.json"


# faz a requisição na API e devolve os dados em dicionário
def pegar_dados(endereco):
    try:
        resposta = requests.get(URL + endereco, timeout=10)
        if resposta.status_code == 200:
            return resposta.json()
        elif resposta.status_code == 404:
            print("Não encontrado, confira o que você digitou.\n")
        else:
            print("Erro na API:", resposta.status_code, "\n")
    except requests.exceptions.ConnectionError:
        print("Sem conexão com a internet.\n")
    except requests.exceptions.Timeout:
        print("A API demorou muito para responder.\n")
    return None


# mostra os pokémon de 20 em 20 com número e nome
def mostrar_lista():
    inicio = 0
    while True:
        dados = pegar_dados("pokemon?limit=20&offset=" + str(inicio))
        if dados is None:
            break

        numero = inicio + 1
        for item in dados["results"]:
            print(numero, "-", item["name"])
            numero = numero + 1

        resposta = input("\nENTER para ver mais ou S para voltar: ")
        print()
        if resposta.lower() == "s":
            break
        inicio = inicio + 20


# pega do json da api só o que vamos usar
def organizar(dados):
    tipos = []
    for t in dados["types"]:
        tipos.append(t["type"]["name"])

    habilidades = []
    for h in dados["abilities"]:
        habilidades.append(h["ability"]["name"])

    pokemon = {
        "numero": dados["id"],
        "nome": dados["name"],
        "tipos": tipos,
        "habilidades": habilidades,
        "altura": dados["height"] / 10,
        "peso": dados["weight"] / 10,
        "hp": dados["stats"][0]["base_stat"],
        "ataque": dados["stats"][1]["base_stat"],
        "defesa": dados["stats"][2]["base_stat"],
        "velocidade": dados["stats"][5]["base_stat"],
    }
    # poder total = soma dos status
    pokemon["poder_total"] = pokemon["hp"] + pokemon["ataque"] + pokemon["defesa"] + pokemon["velocidade"]
    return pokemon


def mostrar(pokemon):
    print("----------------------")
    print("Número:", pokemon["numero"])
    print("Nome:", pokemon["nome"])
    print("Tipo:", ", ".join(pokemon["tipos"]))
    print("Habilidades:", ", ".join(pokemon["habilidades"]))
    print("Altura:", pokemon["altura"], "m")
    print("Peso:", pokemon["peso"], "kg")
    print("HP:", pokemon["hp"])
    print("Ataque:", pokemon["ataque"])
    print("Defesa:", pokemon["defesa"])
    print("Velocidade:", pokemon["velocidade"])
    print("Poder total:", pokemon["poder_total"])
    print("----------------------\n")


# compara o poder total dos dois pokémon
def comparar(p1, p2):
    total1 = p1["poder_total"]
    total2 = p2["poder_total"]

    print(p1["nome"], "tem", total1, "pontos")
    print(p2["nome"], "tem", total2, "pontos")

    if total1 > total2:
        print("O mais forte é o", p1["nome"], "\n")
    elif total2 > total1:
        print("O mais forte é o", p2["nome"], "\n")
    else:
        print("Deu empate!\n")


def salvar(lista):
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump(lista, arquivo, indent=4, ensure_ascii=False)
    except OSError:
        print("Erro ao salvar o arquivo.\n")


def carregar():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# programa principal
salvos = carregar()

while True:
    print("===== POKÉDEX =====")
    print("1 - Ver lista de pokémon")
    print("2 - Buscar pokémon")
    print("3 - Comparar dois pokémon")
    print("4 - Ver pokémon salvos")
    print("0 - Sair")
    opcao = input("Opção: ")
    print()

    if opcao == "1":
        mostrar_lista()

    elif opcao == "2":
        nome = input("Nome ou número: ").lower().strip()
        if nome == "":
            print("Digite um nome ou número.\n")
            continue
        dados = pegar_dados("pokemon/" + nome)
        if dados is not None:
            pokemon = organizar(dados)
            mostrar(pokemon)
            salvos.append(pokemon)
            salvar(salvos)

    elif opcao == "3":
        nome1 = input("Primeiro pokémon: ").lower().strip()
        nome2 = input("Segundo pokémon: ").lower().strip()
        if nome1 == "" or nome2 == "":
            print("Digite os dois nomes.\n")
            continue
        dados1 = pegar_dados("pokemon/" + nome1)
        dados2 = pegar_dados("pokemon/" + nome2)
        if dados1 is not None and dados2 is not None:
            comparar(organizar(dados1), organizar(dados2))

    elif opcao == "4":
        if len(salvos) == 0:
            print("Nenhum pokémon salvo.\n")
        for pokemon in salvos:
            mostrar(pokemon)

    elif opcao == "0":
        print("Tchau!")
        break

    else:
        print("Opção inválida.\n")
