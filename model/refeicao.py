from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from model.dieta import Dieta
from datetime import datetime
from typing import Union
from  model import Base


class Refeicao(Base):
    __tablename__ = 'refeicao'
    
    id_refeicao = Column("id_refeicao", Integer, primary_key=True)
    nome = Column(String(100))    
    dia_semana = Column(String(20))
    
    
    # Definição do relacionamento entre o dieta e refeicao.
    # Aqui está sendo definido a coluna 'dieta_id' que vai guardar
    # a referencia a dieta, a chave estrangeira que relaciona
    # uma dieta e refeicao.
    dieta_id = Column(Integer, ForeignKey("dieta.id_dieta", ondelete="CASCADE"), nullable=False)
    
    # many-to-one 
    dieta = relationship("Dieta", backref=backref("Refeicao", cascade="all,delete"))

    def __init__(self, nome:str, dia_semana:str, dieta:Dieta):                
        """
        Cria uma refeição

        Arguments:
            nome: almoço, jantar, lanche,....
            dia_semana: seg, tec, qua, todos os dias, ....  
            dieta: refeição pertence a que dieta         
        """
        self.nome = nome
        self.dia_semana = dia_semana
        self.dieta = dieta