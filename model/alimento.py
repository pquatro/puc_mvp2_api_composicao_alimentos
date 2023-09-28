class Alimento: 

    def __init__(self, nome:str, energia:int, proteina:float, lipideo:float, carboidrato:float):                 
        """
        Cria um Alimento

        Arguments:
            nome: nome ou descrição do alimento por 100 gramas por parte comestível.
            energia: quantidade de calorias (kcal) 
            proteína: quantidade em gramas
            lipídeo: quantidade em gramas
            carboidrato: quantidade em gramas            
        """       
        self.nome = nome
        self.energia = energia
        self.proteina = proteina
        self.lipideo = lipideo
        self.carboidrato = carboidrato        