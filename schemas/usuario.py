from datetime import date
import datetime
from pydantic import BaseModel
from typing import Optional, List
from model.usuario import Usuario


class UsuarioSchema(BaseModel):
    """ Define como um novo usuario a ser inserido deve ser representado
    """    
    nome: str = "Fulano de Tal"
    email: str = "pquatro@gmail.com"
    sexo: str = "masculino"
    altura: float = 184
    peso: float = 95
    nascimento: date = date(1978, 5, 13)    


class UsuarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no código do usuario.
    """
    id_usuario: int = 1


class ListagemUsuariosSchema(BaseModel):
    """ Define como uma listagem de usuarios será retornada.
    """
    usuarios:List[UsuarioSchema]


def apresenta_usuarios(usuarios: List[Usuario]):
    """ Retorna uma representação do usuario seguindo o schema definido em
        UsuarioViewSchema.
    """
    result = []
    for usuario in usuarios:
        result.append({
            "id": usuario.id_usuario,
            "nome": usuario.nome,
            "email": usuario.email,
            "sexo": usuario.sexo,
            "altura": usuario.altura,
            "peso": usuario.peso,
            "nascimento": usuario.nascimento,
            "dt_cadastro": usuario.dt_cadastro
        })

    return {"usuarios": result}



class UsuarioViewSchema(BaseModel):
    """ Define como um usuario será retornado: usuario + grupo.
    """         
    nome: str = "Fulano de Tal"
    email: str = "pquatro@gmail.com"
    sexo: str = "masculino"
    altura: float = 184
    peso: float = 95
    nascimento: date = date(1978, 5, 13)    


class UsuarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação do usuario seguindo o schema definido em
        UsuarioViewSchema.
    """
    return {     
        "id": usuario.id_usuario,   
        "nome": usuario.nome,
        "email": usuario.email,
        "sexo": usuario.sexo,
        "altura": usuario.altura,
        "peso": usuario.peso,
        "nascimento": usuario.nascimento,        
        "dt_cadastro": usuario.dt_cadastro
    }


class UsuarioUpdateSchema(BaseModel):
    """ Define como um novo usuario pode ser atualizado.
    """
    id: int = 1
    nome: str = "Fulano de Tal"    
    email: str = "pquatro@gmail.com"
    sexo: str = "masculino"
    altura: float = 184
    peso: float = 95
    nascimento: date = date(1978, 5, 13)
    