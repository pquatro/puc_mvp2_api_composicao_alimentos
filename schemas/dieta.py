from datetime import date
from pydantic import BaseModel
from typing import Optional, List
from model.dieta import Dieta
from schemas import UsuarioSchema


class DietaSchema(BaseModel):
    """ Define como um novo dieta a ser inserido deve ser representado
    """    
    objetivo: str = "agressivos"
    nivel_atividade: str = "moderado"    
    peso: int = 95       
    usuario_id: int = 1


class DietaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no código da dieta.
    """
    id_dieta: int = 1


class ListagemDietasSchema(BaseModel):
    """ Define como uma listagem de dietas será retornada.
    """
    dietas:List[DietaSchema]


def apresenta_dietas(dietas: List[Dieta]):
    """ Retorna uma representação do dieta seguindo o schema definido em
        DietaViewSchema.
    """
    result = []
    for dieta in dietas:
        result.append({
            "id": dieta.id_dieta,
            "objetivo": dieta.objetivo,
            "nivel_atividade": dieta.nivel_atividade,
            "tmb": dieta.tmb,
            "tdee": dieta.tdee,
            "proteina": dieta.proteina,
            "gordura": dieta.gordura,
            "carboidrato": dieta.carboidrato,
            "caloria": dieta.caloria,
            "peso": dieta.peso,
            "dt_cadastro": dieta.dt_cadastro,
            "usuario": dieta.usuario.nome
        })

    return {"dietas": result}


class DietaViewSchema(BaseModel):
    """ Define como um dieta será retornado: dieta + grupo.
    """             
    objetivo: str = "agressivos"
    nivel_atividade: str = "moderado"   
    peso: int = 95       
    usuario: UsuarioSchema = {"id": 1,"nome": "Fulano de Tal"}   


class DietaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_dieta(dieta: Dieta):
    """ Retorna uma representação do dieta seguindo o schema definido em
        DietaViewSchema.
    """
    return {     
        "id": dieta.id_dieta,
        "objetivo": dieta.objetivo,
        "nivel_atividade": dieta.nivel_atividade,
        "tmb": dieta.tmb,
        "tdee": dieta.tdee,
        "proteina": dieta.proteina,
        "gordura": dieta.gordura,
        "carboidrato": dieta.carboidrato,
        "caloria": dieta.caloria,
        "peso": dieta.peso,
        "dt_cadastro": dieta.dt_cadastro,
        "usuario":  {"id": dieta.usuario.id_usuario,"nome": dieta.usuario.nome}    
    }


class DietaUpdateSchema(BaseModel):
    """ Define como um novo dieta pode ser atualizado.
    """
    id: int = 1
    objetivo: str = "agressivos"
    nivel_atividade: str = "moderado"   
    peso: int = 95       
    usuario_id: int = 1