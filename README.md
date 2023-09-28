# API de Cadastro de Dieta Nutricional

Este pequeno projeto faz parte da Disciplina **Arquitetura de Software** da Pós-Graduação Engenharia de Software PUC-Rio

A idéia desse projeto é apresentar o cadastro de uma dieta nutricional, calculando o metabolismo do usuário e a quantidade de macros necessários para atingir sua meta. Nesse cadastro teremos os usuários, a dieta e as refeições que o usuário irá montar para atingir seu objetivo nutricional. Temos também os alimentos classificados por grupos alimentícios, com seus respectivos conjunto de macros principais (calorias, proteínas, carboidratos e gorduras). Esses dados são usados por nutricionistas para calcular uma dieta.

O front-end foi desenvolvido utilizando [Bootstrap](https://getbootstrap.com/) para tornar responsivo e a biblioteca [jQuery](https://jquery.com/) para interação JavaScript. Foi utilizado também o plug-in de jQuery [DataTables](https://datatables.net/), para exibição dos dados em uma grid.  

---
# Como executar 
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Para criar o ambiente:
```
py -m venv env
```
Para ativar o ambiente:
```
.\env\Scripts\activate
```
Será necessário ter todas as libs python listadas no arquivo `requirements.txt` instaladas.
Para instalar as libs:
```
(env)pip install -r requirements.txt
```
Pode acontecer no momento de executar a API, a falta de alguma lib no projeto. Basta executar o comando abaixo para instalar alguma lib que esteja faltando:
```
(env)pip install <nome_da_lib>
```
Para executar a API  basta executar:

```
(env)flask run --host 0.0.0.0 --port 5000
```
Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

> Todos os comandos acima foram executados no sistema operacional Windows. Em Linux, alguns desses comandos tem sintaxe diferente.

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t rest-api .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 5000:5000 rest-api
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.



### Alguns comandos úteis do Docker

**Para verificar se a imagem foi criada** você pode executar o seguinte comando:

```
$ docker images
```

 Caso queira **remover uma imagem**, basta executar o comando:
```
$ docker rmi <IMAGE ID>
```
Subistituindo o `IMAGE ID` pelo código da imagem

**Para verificar se o container está em exceução** você pode executar o seguinte comando:

```
$ docker container ls --all
```

 Caso queira **parar um conatiner**, basta executar o comando:
```
$ docker stop <CONTAINER ID>
```
Subistituindo o `CONTAINER ID` pelo ID do conatiner


 Caso queira **destruir um conatiner**, basta executar o comando:
```
$ docker rm <CONTAINER ID>
```
Para mais comandos, veja a [documentação do docker](https://docs.docker.com/engine/reference/run/).