from operator import and_
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
from model import Session, Dieta, Refeicao, Usuario
from schemas import *



info = Info(title="API de Cadastro de Dieta Nutricional", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuario", description="Adição, Atualização, visualização e remoção de usuários à base")
dieta_tag = Tag(name="Dieta", description="Adição, visualização e remoção de dietas à base")
refeicao_tag = Tag(name="Refeicao", description="Adição, visualização e remoção de refeições à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo Usuario à base de dados

    Retorna uma representação de um usuario.
    """
    usuario = Usuario (        
        nome=form.nome,
        email = form.email,
        sexo = form.sexo,
        nascimento = form.nascimento,
        altura = form.altura,
        peso = form.peso
    ) 

    try:
        # criando conexão com a base
        session = Session()   
       
        # criando conexão com a base
        session = Session()
        # fazendo a busca se já existe com mesmo e-mail
        usuario_cadastrado = session.query(Usuario).filter(Usuario.email == usuario.email).first()
        
        if usuario_cadastrado:
            # se o usuario foi encontrado
            error_msg = "Usuario de mesmo e-mail já salvo na base :/"
            return {"mesage": error_msg}, 409
        

        # adicionando usuario
        session.add(usuario)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_usuario(usuario), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Usuario de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400


@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def get_usuarios():
    """Faz a busca por todos os Usuarios cadastrados

    Retorna uma representação da listagem de usuarios.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca    
    usuarios = session.query(Usuario).all()
               
    if not usuarios:
        # se não há usuarios cadastrados
        return {"usuarios": []}, 200
    else:
        # retorna a representação de usuario        
        return apresenta_usuarios(usuarios), 200


@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def get_usuario(query: UsuarioBuscaSchema):
    """Faz a busca por um Usuario a partir do id do usuario

    Retorna uma representação dos usuarios.
    """
    usuario_id = query.id_usuario
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuario = session.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    if not usuario:
        # se o usuario não foi encontrado
        error_msg = "Usuario não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de usuario
        return apresenta_usuario(usuario), 200


@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})
def del_usuario(query: UsuarioBuscaSchema):
    """Deleta um Usuario a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    usuario_id = query.id_usuario

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Usuario).filter(Usuario.id_usuario == usuario_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Usuário removido", "id": usuario_id}
    else:
        # se o usuario não foi encontrado
        error_msg = "Usuario não encontrado na base :/"
        return {"mesage": error_msg}, 404


@app.post('/update_usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_usuario(form: UsuarioUpdateSchema):
    """Edita um Usuario já salvo na base de dados

    Retorna uma representação dos usuarios.
    """
    usuario_id = form.id    

    try:
        # criando conexão com a base para verificar usuario
        session = Session()
      

         # fazendo a busca do usuario pelo id informado
        query = session.query(Usuario).filter(Usuario.id_usuario == usuario_id)        
        db_usuario = query.first()      

        if not db_usuario:
            # se o usuario não foi encontrado
            error_msg = "Usuário não encontrado na base :/"            
            return {"mesage": error_msg}, 404
        else:
             # altera os campos do usuario
            if form.nome:
                db_usuario.nome = form.nome
            
            if form.email:
                db_usuario.email = form.email
            
            if form.sexo:
                db_usuario.sexo = form.sexo

            if form.nascimento:
                db_usuario.nascimento = form.nascimento
            
            if form.peso:
                db_usuario.peso = form.peso

            if form.altura:
                db_usuario.altura = form.altura          

            #atualiza o usuário
            session.add(db_usuario)
            session.commit()            
            return apresenta_usuario(db_usuario), 200        

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Usuário de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400  
    

"""------------------------Dieta----------------------"""

@app.post('/dieta', tags=[dieta_tag],
        responses={"200": DietaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_dieta(form: DietaSchema):
    """Adiciona uma nova Dieta à base de dados

    Retorna uma representação de uma dieta.
    """
    
    dieta = Dieta (   
        peso = form.peso,
        objetivo = form.objetivo,
        nivel_atividade = form.nivel_atividade,   
        tmb = None,
        tdee = None,
        proteina = None,
        gordura = None,
        carboidrato = None,
        caloria = None,
        usuario = None
    ) 
    
    usuario_id = form.usuario_id

    try:
        # criando conexão com a base
        session = Session()   


         # fazendo a busca do usuario pelo id informado
        usuario = session.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        if not usuario:
            # se não existir o usuario cadastrado
            error_msg = "Usuário não cadastrado na base :/"
            return {"mesage": error_msg}, 404            
        else:
            # adiciona usuario a dieta            
            dieta.usuario = usuario       


        
        #calculando tmb
        dieta.tmb = dieta.calcula_tmb(usuario,form.peso)        
        if dieta.tmb > 0: 
            #calculando tdee
            dieta.tdee = dieta.calcula_tdee(form.nivel_atividade,int(dieta.tmb))
            if dieta.tdee > 0: 
                #calculando as calorias
                dieta.caloria = dieta.calcula_calorias_objetivo(form.objetivo, int(dieta.tdee))
                if dieta.caloria>0:        
                    #calculando as proteinas
                    dieta.proteina = dieta.calcula_proteina(dieta.caloria, form.objetivo)
                    #calculando as gorduras
                    dieta.gordura = dieta.calcula_gordura(dieta.caloria, form.objetivo)
                    #calculando as carboidratros
                    dieta.carboidrato = dieta.calcula_carboidrato(dieta.caloria, form.objetivo)
        

        
        # adicionando dieta
        session.add(dieta)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_dieta(dieta), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Dieta já salva na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400


@app.get('/dietas', tags=[dieta_tag],
        responses={"200": ListagemDietasSchema, "404": ErrorSchema})
def get_dietas():
    """Faz a busca por todas as Dietas cadastradas

    Retorna uma representação da listagem de dietas.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca    
    dietas = session.query(Dieta).all()
            
    if not dietas:
        # se não há dietas cadastradas
        return {"dietas": []}, 200
    else:
        # retorna a representação de dieta        
        return apresenta_dietas(dietas), 200


@app.get('/dieta', tags=[dieta_tag],
        responses={"200": DietaViewSchema, "404": ErrorSchema})
def get_dieta(query: DietaBuscaSchema):
    """Faz a busca por uma dieta a partir do id da dieta

    Retorna uma representação das dietas.
    """
    dieta_id = query.id_dieta
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    dieta = session.query(Dieta).filter(Dieta.id_dieta == dieta_id).first()
    
    if not dieta:
        # se a dieta não foi encontrada
        error_msg = "Dieta não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de dieta
        return apresenta_dieta(dieta), 200


@app.delete('/dieta', tags=[dieta_tag],
            responses={"200": DietaDelSchema, "404": ErrorSchema})
def del_dieta(query: DietaBuscaSchema):
    """Deleta uma dieta a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    dieta_id = query.id_dieta

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Dieta).filter(Dieta.id_dieta == dieta_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Dieta removida", "id": dieta_id}
    else:
        # se a dieta não foi encontrada
        error_msg = "Dieta não encontrada na base :/"
        return {"mesage": error_msg}, 404


@app.post('/update_dieta', tags=[dieta_tag],
        responses={"200": DietaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_dieta(form: DietaUpdateSchema):
    """Edita uma Dieta já salva na base de dados

    Retorna uma representação das dietas.
    """
    dieta_id = form.id    

    try:
        # criando conexão com a base para verificar dieta
        session = Session()

         # fazendo a busca do usuario pelo id informado
        usuario = session.query(Usuario).filter(Usuario.id_usuario == form.usuario_id).first()
        if not usuario:
            # se não existir o usuario cadastrado
            error_msg = "Usuário não cadastrado na base :/"
            return {"mesage": error_msg}, 404                    
    
        # fazendo a busca da dieta pelo id informado
        query = session.query(Dieta).filter(Dieta.id_dieta == dieta_id)        
        db_dieta = query.first()      

        if not db_dieta:
            # se a dieta não foi encontrada
            error_msg = "Dieta não encontrada na base :/"            
            return {"mesage": error_msg}, 404
        else:
            # altera os campos da dieta
            if form.peso:
                db_dieta.peso = form.peso
            
            if form.objetivo:
                db_dieta.objetivo = form.objetivo
            
            if form.nivel_atividade:
                db_dieta.nivel_atividade = form.nivel_atividade

            #calculando tmb
            db_dieta.tmb = db_dieta.calcula_tmb(usuario,form.peso)        
            if db_dieta.tmb > 0: 
                #calculando tdee
                db_dieta.tdee = db_dieta.calcula_tdee(form.nivel_atividade,int(db_dieta.tmb))
                if db_dieta.tdee > 0: 
                    #calculando as calorias
                    db_dieta.caloria = db_dieta.calcula_calorias_objetivo(form.objetivo, int(db_dieta.tdee))
                    if db_dieta.caloria>0:        
                        #calculando as proteinas
                        db_dieta.proteina = db_dieta.calcula_proteina(db_dieta.caloria, form.objetivo)
                        #calculando as gorduras
                        db_dieta.gordura = db_dieta.calcula_gordura(db_dieta.caloria, form.objetivo)
                        #calculando as carboidratros
                        db_dieta.carboidrato = db_dieta.calcula_carboidrato(db_dieta.caloria, form.objetivo)
              

            #atualiza a dieta
            session.add(db_dieta)
            session.commit()            
            return apresenta_dieta(db_dieta), 200        

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Dieta já salva na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400
    

"""------------------------Refeição----------------------"""

@app.post('/refeicao', tags=[refeicao_tag],
        responses={"200": RefeicaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_refeicao(form: RefeicaoSchema):
    """Adiciona uma nova Refeicao à base de dados

    Retorna uma representação de uma refeicao.
    """
    refeicao = Refeicao (   
        nome = form.nome,
        dia_semana = form.dia_semana,        
        dieta = None
    ) 

    dieta_id = form.dieta_id

    try:
        # criando conexão com a base
        session = Session()   


         # fazendo a busca da dieta pelo id informado
        dieta = session.query(Dieta).filter(Dieta.id_dieta == dieta_id).first()
        if not dieta:
            # se não existir a dieta cadastrada
            error_msg = "Dieta não cadastrada na base :/"
            return {"mesage": error_msg}, 404            
        else:
            # adiciona refeicao a dieta              
            refeicao.dieta = dieta       


        # adicionando refeicao
        session.add(refeicao)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_refeicao(refeicao), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Refeição já salva na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400


@app.get('/refeicaos', tags=[refeicao_tag],
        responses={"200": ListagemRefeicaosSchema, "404": ErrorSchema})
def get_refeicaos():
    """Faz a busca por todas as Refeições cadastradas

    Retorna uma representação da listagem de Refeições.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca    
    refeicaos = session.query(Refeicao).all()
            
    if not refeicaos:
        # se não há Refeições cadastradas
        return {"refeicaos": []}, 200
    else:
        # retorna a representação de refeição       
        return apresenta_refeicaos(refeicaos), 200



@app.get('/refeicao', tags=[refeicao_tag],
        responses={"200": RefeicaoViewSchema, "404": ErrorSchema})
def get_refeicao(query: RefeicaoBuscaSchema):
    """Faz a busca por uma refeição a partir do id da refeição

    Retorna uma representação das refeições.
    """
    refeicao_id = query.id_refeicao
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    refeicao = session.query(Refeicao).filter(Refeicao.id_refeicao == refeicao_id).first()
    
    if not refeicao:
        # se a refeição não foi encontrada
        error_msg = "Refeicao não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de refeição
        return apresenta_refeicao(refeicao), 200


@app.delete('/refeicao', tags=[refeicao_tag],
            responses={"200": RefeicaoDelSchema, "404": ErrorSchema})
def del_refeicao(query: RefeicaoBuscaSchema):
    """Deleta uma refeição a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    refeicao_id = query.id_refeicao

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Refeicao).filter(Refeicao.id_refeicao == refeicao_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Refeição removida", "id": refeicao_id}
    else:
        # se a refeição não foi encontrada
        error_msg = "Refeição não encontrada na base :/"
        return {"mesage": error_msg}, 404


@app.put('/update_refeicao', tags=[refeicao_tag],
        responses={"200": RefeicaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_refeicao(form: RefeicaoUpdateSchema):
    """Edita uma Refeição já salva na base de dados

    Retorna uma representação das refeições.
    """
    refeicao_id = form.id    

    try:
        # criando conexão com a base para verificar refeição
        session = Session()
    

        # fazendo a busca da refeição pelo id informado
        query = session.query(Refeicao).filter(Refeicao.id_refeicao == refeicao_id)        
        db_refeicao = query.first()      

        if not db_refeicao:
            # se a refeição não foi encontrada
            error_msg = "Refeição não encontrada na base :/"            
            return {"mesage": error_msg}, 404
        else:
            # altera os campos da refeição
            if form.nome:
                db_refeicao.nome = form.nome
            
            if form.dia_semana:
                db_refeicao.dia_semana = form.dia_semana

            #atualiza a refeicao
            session.add(db_refeicao)
            session.commit()            
            return apresenta_refeicao(db_refeicao), 200        

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Refeição já salva na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400