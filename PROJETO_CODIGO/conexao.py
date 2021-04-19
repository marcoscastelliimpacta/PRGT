import MySQLdb


class Projeto:
    def __init__(self, codigo_projeto, nome_projeto, local_projeto, orcamento, prazo_dias, data_inicio, data_finalizacao, codigo_cli , codigo_status, observacao):
        self.codigo_projeto = codigo_projeto
        self.nome_projeto = nome_projeto
        self.local_projeto = local_projeto
        self.orcamento = orcamento
        self.prazo_dias = prazo_dias
        self.data_inicio = data_inicio
        self.data_finalizacao = data_finalizacao
        self.codigo_cli = codigo_cli
        self.codigo_status = codigo_status
        self.observacao = observacao
    def __repr__(self):
        return f'Projeto: {self.codigo_projeto}'


class Funcionario:
    def __init__(self, codigo_func, codigo_usuario, email, nome, cpf, funcao):
        self.codigo_func = codigo_func
        self.codigo_usuario = codigo_usuario
        self.email = email
        self.nome = nome
        self.cpf = cpf
        self.funcao = funcao
    def __repr__(self):
        return f'CPF: {self.cpf}'

class Todos_Funcionarios:
    def __init__(self, codigo_func,	codigo_usuario,	nome,	cpf,	email,	codigo_funcao,	codigo_status,	codigo_status_alocacao,	data_hora_post):
        self.codigo_func = codigo_func
        self.codigo_usuario = codigo_usuario
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.codigo_funcao = codigo_func
        self.codigo_status = codigo_status
        self.codigo_status_alocacao = codigo_status_alocacao
        self.data_hora_post = data_hora_post
    def __repr__(self):
        return f'codigo_func: {self.codigo_func}'



class User:
    def __init__(self, codigo, name, email, telefone, username, user_type):
        self.codigo = codigo
        self.name = name
        self.email = email
        self.telefone = telefone
        self.username = username
        self.user_type = user_type
    
    def __repr__(self):
        return f'User: {self.username}'




def open_Conection():
    senha  = 'prgt123456'
    username = 'prgt_db'     
    conn = MySQLdb.Connect(host='prgt_db.mysql.dbaas.com.br',
                            user=username, passwd=senha, db='prgt_db')
    cursor = conn.cursor()
    return cursor, conn


def close_Conection(cursor, conn):
    cursor.close()
    conn.close()




def selecionarTabela():
    cursor = open_Conection()
    cursor[0].callproc('Select_Imgs_Blog_Home')    
    conteudo = []
    for row in cursor[0]:
        conteudo.append(row)    
    close_Conection(cursor[0], cursor[1])
    return conteudo

def selecionarImagens(setor):
    #try:
    cursor = open_Conection()
    cursor[0].callproc("Select_Imgs_Por_Setor",[setor])
    conteudo = []
    for row in cursor[0]:
        conteudo.append(row)    
    close_Conection(cursor[0], cursor[1])
    return conteudo
    #except TypeError as m:
    #    raise SyntaxError
    

def selecionarImagens_Blog(setor):
    #try:
    cursor = open_Conection()
    cursor[0].callproc("Select_Imgs_Blog_page",[setor])
    conteudo = []
    for row in cursor[0]:
        conteudo.append(row)    
    close_Conection(cursor[0], cursor[1])
    return conteudo


funcionarios = []
users = []
projetos = []
def Autentic_Usuario(usuario, senha):
    users.clear()
    cursor = open_Conection()
    cursor[0].callproc("Autentic_Usuario",[usuario, senha])    
    for row in cursor[0]:
        users.append(User(row[0], row[1], row[2], row[3], row[4], row[5]))         
    close_Conection(cursor[0], cursor[1])


def Alter_Password_Usuario(usuario, senha, nova_senha):
    #users.clear()
    cursor = open_Conection()
    cursor[0].callproc("Alter_Password_Usuario",[usuario, senha, nova_senha]) 
    cursor[1].commit()
    #cursor[0].callproc("Autentic_Usuario",[usuario, senha])
    for row in cursor[0]:
        users.append(User(row[0], row[1], row[2], row[3], row[4], row[5]))         
    close_Conection(cursor[0], cursor[1])
    return cursor[0].rowcount


def Alter_Dados_Cliente(id_cli, nome, email, telefone):
    cursor = open_Conection()
    cursor[0].callproc("Alter_Dados_Cliente", [id_cli, nome, email, telefone])
    cursor[1].commit()



def Select_Func_Data(codigo_usuario):
    cursor = open_Conection()
    cursor[0].callproc("Select_Func_Data",[codigo_usuario])
    conteudo = []
    for row in cursor[0]:
        funcionarios.append(Funcionario(row[0], row[1], row[2], row[3], row[4], row[5]))    
    close_Conection(cursor[0], cursor[1])




def Select_Img_Admin_Por_Permissao(codigo_usuario):
    cursor = open_Conection()
    cursor[0].callproc("Select_Img_Admin_Por_Permissao",[codigo_usuario])
    conteudo = []
    for row in cursor[0]:
        conteudo.append(row)    
    close_Conection(cursor[0], cursor[1])
    return conteudo


def Listar_Todos_Projetos():
    cursor = open_Conection()
    cursor[0].callproc("Listar_Todos_Projetos")
    conteudo = []
    for row in cursor[0]:
        conteudo.append(row)    
    close_Conection(cursor[0], cursor[1])
    return conteudo

def Listar_Todos_Clientes():
    cursor = open_Conection()
    cursor[0].callproc("Listar_Todos_Clientes")
    conteudo = []
    for row in cursor[0]:
        conteudo.append(row)    
    close_Conection(cursor[0], cursor[1])
    return conteudo


def Listar_Status_Projeto():
    cursor = open_Conection()
    cursor[0].callproc("Listar_Status_Projeto")
    conteudo = []
    for row in cursor[0]:
        conteudo.append(row)    
    close_Conection(cursor[0], cursor[1])
    return conteudo

def Listar_Todos_Funcionarios(codigo_projeto):
    if codigo_projeto == None:
        codigo_projeto = 0
    cursor = open_Conection()
    cursor[0].callproc("Listar_Todos_Funcionarios",[codigo_projeto])
    conteudo = []
    for row in cursor[0]:
        conteudo.append(row)    
    close_Conection(cursor[0], cursor[1])
    return conteudo



def Insert_New_Project(nome_projeto, local_projeto, orcamento, prazo_dias,
                        data_inicio, data_fim, codigo_cliente, codigo_status, observacao, codigo_func):
    cursor = open_Conection()
    cursor[0].callproc("Insert_New_Project",[nome_projeto, local_projeto, orcamento, prazo_dias,
                        data_inicio, data_fim, codigo_cliente, codigo_status, observacao, codigo_func]) 
    cursor[1].commit()
    close_Conection(cursor[0], cursor[1])
    

def Select_Top_Projeto():
    projetos.clear()
    cursor = open_Conection()
    cursor[0].callproc("Select_Top_Projeto")
    for row in cursor[0]:
        projetos.append(Projeto(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))    
    close_Conection(cursor[0], cursor[1])
    return projetos[len(projetos)-1].codigo_projeto


def Insert_Func_Proj(codigo_projeto, codigo_func):
    cursor = open_Conection()
    cursor[0].callproc("Insert_Func_Proj",[codigo_projeto, codigo_func]) 
    cursor[1].commit()
    close_Conection(cursor[0], cursor[1])


def Select_Projeto_Selecionado(codigo_projeto):
    projetos.clear()
    cursor = open_Conection()
    cursor[0].callproc("Select_Projeto_Selecionado",[codigo_projeto])
    for row in cursor[0]:
        projetos.append(Projeto(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))    
    close_Conection(cursor[0], cursor[1])
    return projetos[len(projetos)-1].codigo_projeto


def Listar_Servicos_Projetos(codigo_projeto):
    cursor = open_Conection()
    cursor[0].callproc("Listar_Servicos_Projetos",[codigo_projeto])
    servicos = []
    for row in cursor[0]:
        servicos.append(row)
    close_Conection(cursor[0], cursor[1])
    return servicos


def Insert_and_Update_Servicos(codigo_projeto, codigo_servico, porcentagem):
    cursor = open_Conection()
    cursor[0].callproc("Insert_and_Update_Servicos",[codigo_projeto, codigo_servico, porcentagem]) 
    cursor[1].commit()
    close_Conection(cursor[0], cursor[1])
    

def Delete_All_Servicos(codigo_projeto):
    cursor = open_Conection()
    cursor[0].callproc("Delete_All_Servicos",[codigo_projeto]) 
    cursor[1].commit()
    close_Conection(cursor[0], cursor[1])


def Insert_Imagem(caminho, nome_img, setor, texto_img, link):
    cursor = open_Conection()
    cursor[0].callproc("Insert_Imagem",[caminho, nome_img, setor, texto_img, link]) 
    cursor[1].commit()
    close_Conection(cursor[0], cursor[1])


def Listar_Imagem_Projetos(caminho):
    cursor = open_Conection()
    cursor[0].callproc("Listar_Imagem_Projetos",[caminho])
    imagens = []
    for row in cursor[0]:
        imagens.append(row)
    close_Conection(cursor[0], cursor[1])
    return imagens

def Delete_Img_Projeto(caminho, nome_img):
    cursor = open_Conection()
    cursor[0].callproc("Delete_Img_Projeto",[caminho, nome_img]) 
    cursor[1].commit()
    close_Conection(cursor[0], cursor[1])



def Delete_Todo_Projeto(codigo_projeto):
    cursor = open_Conection()
    cursor[0].callproc("Delete_Todo_Projeto",[codigo_projeto]) 
    cursor[1].commit()
    close_Conection(cursor[0], cursor[1])


def Alterar_Func_Projeto(codigo_projeto, codigo_func):
    cursor = open_Conection()
    cursor[0].callproc("Alterar_Func_Projeto",[codigo_projeto, codigo_func]) 
    cursor[1].commit()
    close_Conection(cursor[0], cursor[1])


def Alterar_Project(idProjeto, projeto, local, orcamento, prazo, dataInicio, dataFim, idCliente, idStatus, obs, codigo_func):
    cursor = open_Conection()
    cursor[0].callproc("Alterar_Project",[idProjeto, projeto, local, orcamento, prazo, dataInicio, dataFim, idCliente, idStatus, obs, codigo_func])
    cursor[1].commit()
    close_Conection(cursor[0], cursor[1])



def Listar_Projetos_Cliente(codigo_usuario):
    cursor = open_Conection()
    cursor[0].callproc("Listar_Projetos_Cliente",[codigo_usuario])
    imagensCapa = []
    for row in cursor[0]:
        imagensCapa.append(row)
    close_Conection(cursor[0], cursor[1])
    return imagensCapa

todos_Func = []
def Listar_Todos_Funcionarios_Cadastrados():
    todos_Func.clear()
    cursor = open_Conection()
    cursor[0].callproc("Listar_Todos_Funcionarios_Cadastrados")    
    for row in cursor[0]:
        todos_Func.append(Todos_Funcionarios(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    close_Conection(cursor[0], cursor[1])


def Listar_Cargos():
    cursor = open_Conection()
    cursor[0].callproc("Listar_Cargos")
    cargos = []
    for row in cursor[0]:
        cargos.append(row)
    close_Conection(cursor[0], cursor[1])
    return cargos


def Limpar_Func_Projeto(idProjeto):
    cursor = open_Conection()
    cursor[0].callproc("Limpar_Func_Projeto",[idProjeto])
    cursor[1].commit()
    close_Conection(cursor[0], cursor[1])


def Listar_Usuario_Func(codigo_usuario):
    cursor = open_Conection()
    cursor[0].callproc("Listar_Usuario_Func",[codigo_usuario])
    usuario = []
    for row in cursor[0]:
        usuario.append(row)
    close_Conection(cursor[0], cursor[1])
    return usuario



def Listar_Tipo_Usuario():
    cursor = open_Conection()
    cursor[0].callproc("Listar_Tipo_Usuario")
    tpUsuario = []
    for row in cursor[0]:
        tpUsuario.append(row)
    close_Conection(cursor[0], cursor[1])
    return tpUsuario


def Listar_Permissoes_Usuarios(codigo_usuario):
    cursor = open_Conection()
    cursor[0].callproc("Listar_Permissoes_Usuarios",[codigo_usuario])
    perUsuario = []
    for row in cursor[0]:
        perUsuario.append(row)
    close_Conection(cursor[0], cursor[1])
    return perUsuario



'Delete_Todo_Projeto'