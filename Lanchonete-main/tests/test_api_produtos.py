def test_produto_alteracao_valor(client):
    
    r1 = client.post("/produtos", json={"codigo": 1, "valor": 5, "tipo": 1})
    assert r1.status_code == 200
    assert r1.json()["codigo"] == 1
    cod_produto = r1.json()["codigo"]

    r2 = client.post(f"/produtos/{cod_produto}/valor", json={"novo_valor": 6.5})
    assert r2.status_code == 200
    assert r2.json()["alterou"] == True