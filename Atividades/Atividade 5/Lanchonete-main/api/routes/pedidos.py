from fastapi import APIRouter, HTTPException
from schemas.pedido import PedidoCreate, PedidoAddItem, PedidoOut, ObservacaoInput, ObservacaoOut
from services.lanchonete_service import service

router = APIRouter(prefix="/lanchonete/pedidos", tags=["pedidos"])


@router.post("", response_model=PedidoOut)
def criar(payload: PedidoCreate):
    """Cria um pedido com o primeiro produto já adicionado."""
    pedido = service.criar_pedido(payload.cpf, payload.cod_produto, payload.qtd_max_produtos)
    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Cliente ou produto não encontrado"
        )

    return PedidoOut(
        codigo=pedido.codigo,
        cpf=pedido.cliente.cpf,
        esta_entregue=pedido.esta_entregue,
        produtos=[p.codigo for p in pedido.listaProdutos],
    )


@router.put("/{cod_pedido}/itens")
def adicionar_item(cod_pedido: int, payload: PedidoAddItem):
    """Adiciona um produto a um pedido existente."""
    ok = service.alterar_pedido(cod_pedido, payload.cod_produto)
    if not ok:
        raise HTTPException(
            status_code=400,
            detail="Pedido/produto inválido ou limite excedido"
        )
    return {"ok": True}


@router.post("/{cod_pedido}/finalizar")
def finalizar(cod_pedido: int):
    """Finaliza um pedido e retorna o total calculado."""
    total = service.finalizar_pedido(cod_pedido)
    if total is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"total": total}


@router.get("/{cod_pedido}", response_model=PedidoOut)
def obter(cod_pedido: int):
    """Busca um pedido pelo código."""
    pedido = service.obter_pedido(cod_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return PedidoOut(
        codigo=pedido.codigo,
        cpf=pedido.cliente.cpf,
        esta_entregue=pedido.esta_entregue,
        produtos=[p.codigo for p in pedido.listaProdutos],
    )

@router.post("/{cod_pedido}/observacao")
def adicionar_observacao(
    cod_pedido: int,
    body: ObservacaoInput
):
    resultado = service.adicionar_observacao(
        cod_pedido,
        body.observacao
    )

    if not resultado:
        raise HTTPException(
            status_code=400,
            detail="Pedido não encontrado ou inválido"
        )

    return {
        "ok": True,
        "mensagem": "Observação adicionada com sucesso"
    }

@router.get(
    "/{cod_pedido}/observacao",
    response_model=ObservacaoOut
)
def buscar_observacao(cod_pedido: int):
    pedido = service.buscar_observacao_pedido(
        cod_pedido
    )

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return ObservacaoOut(
        codigo=pedido.codigo,
        observacao=pedido.observacao
    )

