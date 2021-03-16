from flask import Blueprint, render_template, redirect, request, g, session, url_for
import os.path
from datetime import date
from conexao import *

admin_dp = Blueprint(
    'profile',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/admin/'
)


@admin_dp.route('/', methods=['GET', 'POST'])
def home():    
    if 'user_type' in session:
        user = [x for x in users if x.user_type == session['user_type']][0]
        g.user = user
        if request.method == 'GET':
            if g.user.user_type == 'dev' or g.user.user_type == 'admin' or g.user.user_type == 'func' or g.user.user_type == 'assistente' or g.user.user_type == 'blog':
                Select_Func_Data(g.user.codigo)
                acessos = Select_Img_Admin_Por_Permissao(g.user.codigo)
                func = [x for x in funcionarios if x.codigo_usuario == g.user.codigo][0]
                if func:
                    g.func = func
                return render_template(
                    'admin.html',
                    msgModal = '',
                    titulo = '',
                    retorno = 0,
                    acessos = acessos
                    )
            elif g.user.user_type == 'cliente':
                g.func = 'funcao:'
                return render_template(
                    'area_clientes.html',
                    msgModal = '',
                    titulo = '',
                    retorno = 0
                )                
        elif request.method == 'POST':
            form = request.form
            if request.form['btn_alter'] == 'btn_alter_password':
                    oldPassword = form.get("senha_atual")
                    newPassword = form.get("nova_senha")
                    msgModal = ""
                    titulo = "Alteração de Senha"
                    rowCont = Alter_Password_Usuario(g.user.username, oldPassword, newPassword)                
                    if rowCont >= 1:
                        msgModal = "Senha Alterada com Sucesso!   \t\t  Por vafor, deslogue e logue com a nova senha."
                    else:
                        msgModal = "Senha atual incorreta!"                        
            if g.user.user_type == 'dev' or g.user.user_type == 'admin' or g.user.user_type == 'func':
                acessos = Select_Img_Admin_Por_Permissao(g.user.codigo)
                return render_template(
                    'admin.html',
                    msgModal = msgModal,
                    titulo = titulo,
                    retorno = 1,
                    acessos = acessos
                    )
            elif g.user.user_type == 'cliente':                
                if request.form['btn_alter'] == 'btn_alter_info':
                    vNome = form.get("nome")
                    vEmail = form.get("email")
                    vTelefone = form.get("telefone")
                    g.user.name = vNome
                    g.user.email = vEmail
                    g.user.telefone = vTelefone
                    Alter_Dados_Cliente(g.user.codigo, vNome, vEmail, vTelefone)
                    msgModal = "Alteração feita com sucesso!"
                    titulo = "Alteração dos Dados"
                    print(g.user.codigo)
                    '''return redirect(url_for('profile'))'''
                return render_template(
                    'area_clientes.html',
                    msgModal = msgModal,
                    titulo = titulo,
                    retorno = 1
                    )


@admin_dp.route('/Projetos/')
def Projetos_Admin():
    if 'user_type' in session:
        user = [x for x in users if x.user_type == session['user_type']][0]
        g.user = user
        Select_Func_Data(g.user.codigo)        
        func = [x for x in funcionarios if x.codigo_usuario == g.user.codigo][0]
        if func:
            g.func = func
    return render_template(
        'Projetos_admin.html'
    )

@admin_dp.route('/Lista_Projetos_Admin/', methods=['GET'])
def Lista_Projetos_Admin():
    print("passei aqui")
    return render_template(
        'lista_projetos_admin.html'
    )