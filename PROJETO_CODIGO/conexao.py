import MySQLdb


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