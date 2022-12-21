from Crypto.Hash import SHA512
import json

hash = SHA512.new()

bloco = """{id: 10,
    "transacoes": [
    {
        "de": "carteira_carlos",
        "para": "carteira_andre",
        "valor": 1000,
        "data": "10/20/2021"
    },
    {
        "de": "carteira_johnnie",
        "para": "carteira_andre",
        "valor": 1000,
        "data": "10/20/2021"
    },
    {
        "de": "carteira_andre",
        "para": "carteira_lian",
        "valor": 100,
        "data": "10/20/2010"
    }
]}
"""
bloco_anterior_id = "128319283991"

bloco_para_aprovacao = bloco_anterior_id + bloco
for i in range(1000000000000000):
    solucao_challenge = bloco_para_aprovacao + f"{i}"
    hash.update(bytes(solucao_challenge, "utf-8"))
    if hash.digest().hex().startswith("000000"):
        print(i)
        print(hash.digest().hex())
        break

    



