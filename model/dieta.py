from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
import datetime
from sqlalchemy.orm import relationship, backref
from model.usuario import Usuario
from typing import Union
from  model import Base


class Dieta(Base):
    __tablename__ = 'dieta'

    id_dieta = Column("id_dieta", Integer, primary_key=True)
    peso = Column(Float)    
    objetivo = Column(String(30))
    nivel_atividade = Column(String(50))
    tmb = Column(Integer)
    tdee = Column(Integer)
    proteina = Column(Integer)
    gordura = Column(Integer)
    carboidrato = Column(Integer)
    caloria = Column(Integer)
    dt_cadastro = Column(DateTime,default=datetime.datetime.now())

    # Definição do relacionamento entre dieta e refeiçao.    
    refeicoes = relationship("Refeicao", cascade="all,delete", backref="Dieta")   
    
    # Definição do relacionamento entre o dieta e usuario.
    # Aqui está sendo definido a coluna 'usuario_id' que vai guardar
    # a referencia ao usuario, a chave estrangeira que relaciona
    # um usuario a dieta.
    usuario_id = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    
    # many-to-one 
    usuario = relationship("Usuario", backref=backref("Dieta", cascade="all,delete"))

    def __init__(self, peso:float, objetivo:str,nivel_atividade:str, tmb:int, tdee:int, proteina:int, gordura:int, carboidrato:int, caloria:int, usuario:Usuario, dt_cadastro:Union[DateTime, None] = None):                 
        """
        Cria uma dieta

        Arguments:
            peso: peso do usuário em Kg.
            dt_cadastro: data que esta cadastrando a dieta 
            objetivo: emagrecer, manter o peso, ganhar peso,...
            nivel_atividade: sedentário, levemente ativo, ...
            tmb: Taxa Metabólica Basal
            tdee: gasto total diário ou do inglês (Total Daily Energy Expenditure)
            proteina: quantidade em gramas
            gordura: quantidade em gramas
            carboidrato: quantidade em gramas
            caloria: quantidade de calorias (kcal)
            usuario: usuário que a dieta pertence
        """       
        self.peso = peso        
        self.objetivo = objetivo
        self.nivel_atividade = nivel_atividade
        self.tmb = tmb        
        self.tdee = tdee        
        self.proteina = proteina        
        self.gordura = gordura        
        self.carboidrato = carboidrato        
        self.caloria = caloria
        self.usuario = usuario
    
        # se não for informada, será o data exata da inserção no banco
        if dt_cadastro:
            self.dt_cadastro = dt_cadastro
        

    def adiciona_usuario(self, usuario:Usuario):
        """ Adiciona um novo usuario a dieta
        """
        self.usuario = usuario
    

    def calcula_tmb(self, usuario:Usuario, peso:float):
        """ Gasto de caloria basal
            Resultado em Kcal
        """
        tmb=0

        idade = usuario.calcula_idade(usuario.nascimento)

        if usuario.sexo == "masculino":            
            #tmb = 66.5 + (13.75 * peso) + (5.003 * usuario.altura) - (6.755 * usuario.idade)
            tmb = (10 * peso) + (6.25 * usuario.altura) - (5 * idade) + 5 

        if usuario.sexo == "feminino":            
            #tmb = 655.1 + (9.563 * peso) + (1.850 * usuario.altura) - (4.676 * usuario.idade)
            tmb = (10 * peso) + (6.25 * usuario.altura) - (5 * idade) - 161 

        return tmb
    

    def calcula_tdee(self, nivel_atividade:str, tmb:int):
        """ Gasto energético total
                Sedentário (exercício mínimo)
                Exercício Leve (1-3 dias por semana)
                Exercício Moderado (3-5 dias por semana)
                Exercício Intenso (6-7 dias por semana)
                Exercício muito intenso (atleta - 2x por dia)
        """
        tdee = 0
        if nivel_atividade == 'sedentario':
            tdee = tmb * 1.2
        if nivel_atividade == 'leve':
            tdee = tmb * 1.375
        if nivel_atividade == 'moderado':
            tdee = tmb * 1.55
        if nivel_atividade == 'intenso':
            tdee = tmb * 1.725
        if nivel_atividade == 'muito':
            tdee = tmb * 1.9
        
        return tdee
    

    def calcula_calorias_objetivo(self, objetivo:str, tdee:int):
        """ Ajusta calorias com base no objetivo
                Emagrecer Rápido -20%
                Emagrecer -15%
                Manter Peso 
                Ganhos Moderados 10%
                Ganhos Agressivos 17%
        """
        caloria = 0
        if objetivo == 'rapido':
            caloria = tdee * 0.8
        if objetivo == 'emagrecer':
            caloria = tdee * 0.85
        if objetivo == 'manter':
            caloria = tdee * 1
        if objetivo == 'moderados':
            caloria = tdee * 1.1
        if objetivo == 'agressivos':
            caloria = tdee * 1.17
        
        return int(caloria)

    
    def calcula_proteina(self, caloria:int, objetivo:str):
        """ Calcula as proteinas (g) com base no objetivo
                Emagrecer Rápido LOW CARB (40/40/20) (p/g/c)
                Emagrecer LOW CARB (40/40/20) (p/g/c)
                Manter Peso CARBO MODERADO (30/35/35) (p/g/c)
                Ganhos Moderados CARBO MODERADO (30/35/35) (p/g/c)
                Ganhos Agressivos CARBO ALTO (30/20/50) (p/g/c)

                cada g de proteina 4Kcal
        """
        proteina = 0
        if objetivo == 'rapido':
            proteina = (caloria * 0.4) /4
        if objetivo == 'emagrecer':
            proteina = (caloria * 0.4) /4
        if objetivo == 'manter':
            proteina = (caloria * 0.3) /4
        if objetivo == 'moderados':
            proteina = (caloria * 0.3) /4
        if objetivo == 'agressivos':
            proteina = (caloria * 0.3) /4
        
        return int(proteina)


    def calcula_gordura(self, caloria:int, objetivo:str):
        """ Calcula as gorduras (g) com base no objetivo
                Emagrecer Rápido LOW CARB (40/40/20) (p/g/c)
                Emagrecer LOW CARB (40/40/20) (p/g/c)
                Manter Peso CARBO MODERADO (30/35/35) (p/g/c)
                Ganhos Moderados CARBO MODERADO (30/35/35) (p/g/c)
                Ganhos Agressivos CARBO ALTO (30/20/50) (p/g/c)

                cada g de gordura 9Kcal
        """
        proteina = 0
        if objetivo == 'rapido':
            proteina = (caloria * 0.4) /9
        if objetivo == 'emagrecer':
            proteina = (caloria * 0.4) /9
        if objetivo == 'manter':
            proteina = (caloria * 0.35) /9
        if objetivo == 'moderados':
            proteina = (caloria * 0.35) /9
        if objetivo == 'agressivos':
            proteina = (caloria * 0.2) /9
        
        return int(proteina)
    

    def calcula_carboidrato(self, caloria:int, objetivo:str):
        """ Calcula os carboidratos (g) com base no objetivo
                Emagrecer Rápido LOW CARB (40/40/20) (p/g/c)
                Emagrecer LOW CARB (40/40/20) (p/g/c)
                Manter Peso CARBO MODERADO (30/35/35) (p/g/c)
                Ganhos Moderados CARBO MODERADO (30/35/35) (p/g/c)
                Ganhos Agressivos CARBO ALTO (30/20/50) (p/g/c)

                cada g de gordura 4Kcal
        """
        proteina = 0
        if objetivo == 'rapido':
            proteina = (caloria * 0.2) /4
        if objetivo == 'emagrecer':
            proteina = (caloria * 0.2) /4
        if objetivo == 'manter':
            proteina = (caloria * 0.35) /4
        if objetivo == 'moderados':
            proteina = (caloria * 0.35) /4
        if objetivo == 'agressivos':
            proteina = (caloria * 0.5) /4
        
        return int(proteina)