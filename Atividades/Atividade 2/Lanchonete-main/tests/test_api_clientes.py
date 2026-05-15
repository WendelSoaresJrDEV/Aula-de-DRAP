# =============================================================================
# test_api_clientes.py — Testes de integração dos endpoints de clientes
# =============================================================================
#
# Testes de integração verificam se os componentes da aplicação funcionam
# corretamente juntos: a requisição HTTP chega ao endpoint, passa pelo
# service, persiste no repositório e retorna a resposta correta.
#
# O fixture `client` (definido em conftest.py) é injetado automaticamente
# pelo pytest em cada função que o declara como parâmetro.
# =============================================================================


def test_post_e_get_cliente(client):
    """Deve ser possível criar um cliente e buscá-lo em seguida pelo CPF.

    Este teste cobre o fluxo completo de criação e leitura:
        1. POST /clientes  → cria o cliente e retorna seus dados
        2. GET /clientes/{cpf} → busca o cliente cadastrado

    Verificações:
        - O status HTTP da criação é 200 (OK)
        - O CPF retornado bate com o enviado
        - O status HTTP da busca é 200 (OK)
        - O nome retornado bate com o cadastrado
    """
    response = client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    assert response.status_code == 200
    assert response.json()["cpf"] == "11122233344"

    response2 = client.get("/clientes/11122233344")
    assert response2.status_code == 200
    assert response2.json()["nome"] == "Cliente X"


def test_get_cliente_inexistente(client):
    """Buscar um CPF que não existe deve retornar erro 404 (Not Found).

    Este é um teste de caminho negativo (sad path): verificamos que a API
    se comporta corretamente quando recebe uma entrada inválida ou
    inexistente, retornando o código HTTP adequado.
    """
    response = client.get("/clientes/000")
    assert response.status_code == 404