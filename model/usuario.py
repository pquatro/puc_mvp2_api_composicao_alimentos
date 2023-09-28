from sqlalchemy import Column, Date, String, DateTime, Float, Integer
from sqlalchemy.orm import relationship
from datetime import date, datetime
from typing import Union
from  model import Base


class Usuario(Base):
    __tablename__ = 'usuario'
    
    id_usuario = Column("id_usuario", Integer, primary_key=True)
    nome = Column(String(4000))
    email = Column(String(4000),unique=True)
    sexo = Column(String(9))
    nascimento = Column(Date)
    altura = Column(Float)
    peso = Column(Float)
    dt_cadastro = Column(DateTime,default=datetime.now())
    
    # Definição do relacionamento entre o usuario e a dieta.    
    dietas = relationship("Dieta", cascade="all,delete", backref="Usuario")    

    def __init__(self, nome:str, email:str, sexo:str, altura:float, peso:float, nascimento:Union[date, None] = None, dt_cadastro:Union[DateTime, None] = None):                
        """
        Cria um usuário

        Arguments:
            nome: o nome do usuário.
            email: e-mail do usuário.
            sexo: masculino (m) ou feminino (f)
            nascimento: data de nascimento
            altura: altura em cm
            peso: peso em kg            
        """
        self.nome = nome
        self.email = email
        self.sexo = sexo
        self.nascimento = nascimento
        self.altura = altura
        self.peso = peso
        
        # se não for informada, será o data exata da inserção no banco
        if dt_cadastro:
            self.dt_cadastro = dt_cadastro
        
    def calcula_idade(self, nascimento:Union[date, None] = None):
        """
        Calcula a idade com base no dia atual

        Arguments:            
            nascimento: data de nascimento               
        """
        hoje = date.today()
        return hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))    