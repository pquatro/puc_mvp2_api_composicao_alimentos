from datetime import date
from pydantic import BaseModel
from typing import Optional, List
from model.refeicao import Refeicao
from schemas import DietaSchema


class RefeicaoSchema(BaseModel):
    """ Define como um novo refeicao a ser inserido deve ser representado
    """    
    nome: str = "Almoço"   
    dia_semana: str = "todos os dias"
    dieta_id: int = 1


class RefeicaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no código da refeicao.
    """
    id_refeicao: int = 1



class ListagemRefeicaosSchema(BaseModel):
    """ Define como uma listagem de refeicoes será retornada.
    """
    refeicaos:List[RefeicaoSchema]


def apresenta_refeicaos(refeicaos: List[Refeicao]):
    """ Retorna uma representação do refeicao seguindo o schema definido em
        RefeicaoViewSchema.
    """
    result = []
    for refeicao in refeicaos:
        result.append({
            "id": refeicao.id_refeicao,
            "nome": refeicao.nome,
            "dia_semana": refeicao.dia_semana,            
            "dieta": refeicao.dieta.dt_cadastro,
            "id_dieta": refeicao.dieta.id_dieta
        })

    return {"refeicaos": result}


class RefeicaoViewSchema(BaseModel):
    """ Define como um refeicao será retornado: refeicao + dieta.
    """             
    nome: str = "Almoço"
    dia_semana: str = "todos os dias"   
    dieta: DietaSchema = {"id": 1,"dt_cadastro": date(2023, 9, 5)}   


class RefeicaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_refeicao(refeicao: Refeicao):
    """ Retorna uma representação do refeicao seguindo o schema definido em
        RefeicaoViewSchema.
    """
    return {     
        "id": refeicao.id_refeicao,
        "nome": refeicao.nome,
        "dia_semana": refeicao.dia_semana,            
        "dieta":  {"id": refeicao.dieta.id_dieta,"dt_cadastro": refeicao.dieta.dt_cadastro}    
    }


class RefeicaoUpdateSchema(BaseModel):
    """ Define como um novo refeicao pode ser atualizado.
    """
    id: int = 1
    nome: str = "Almoço"   
    dia_semana: str = "todos os dias"    
    dieta_id: int = 1