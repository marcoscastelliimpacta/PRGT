from flask import Blueprint, render_template, redirect, request, g, session, url_for
import os.path
import json
from datetime import date
from conexao import *
import shutil


admin_dp = Blueprint(
    'profile',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/admin/'
)

class JSonStatusProAtivo:
    def __init__(self, label, data, borderColor, borderWidth, backgroundColor, fontFamily):
        self.label = label
        self.data = data
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.backgroundColor = backgroundColor
        self.fontFamily = fontFamily
    
    def __repr__(self):
        return f'Label: {self.label}'        

class StatusProjetoAtivo:
    def __init__(self, codigo_servico, servico, porcentagem):
        self.codigo_servico = codigo_servico
        self.servico = servico
        self.porcentagem = porcentagem

    def __repr__(self):
        return f'Projeto: {self.codigo_projeto}'

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
                capas = Listar_Projetos_Cliente(g.user.codigo)
                return render_template(
                    'area_clientes.html',
                    msgModal = '',
                    titulo = '',
                    retorno = 0,
                    capas = capas
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
                Select_Func_Data(g.user.codigo)
                acessos = Select_Img_Admin_Por_Permissao(g.user.codigo)
                func = [x for x in funcionarios if x.codigo_usuario == g.user.codigo][0]
                if func:
                    g.func = func
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
                g.func = 'funcao:'
                return render_template(
                    'area_clientes.html',
                    msgModal = msgModal,
                    titulo = titulo,
                    retorno = 1
                    )





@admin_dp.route('/Projetos/', methods=['GET', 'POST'])
def Projetos_Admin():
    if 'user_type' in session:
        user = [x for x in users if x.user_type == session['user_type']][0]
        g.user = user
        Select_Func_Data(g.user.codigo)
        func = [x for x in funcionarios if x.codigo_usuario == g.user.codigo][0]
        if func:
            g.func = func
    clientes = Listar_Todos_Clientes()
    status = Listar_Status_Projeto()
    osProjetos = Listar_Todos_Projetos()
    pasta = ''
    if request.method == 'GET':
        func = Listar_Todos_Funcionarios(0)
        servicos = Listar_Servicos_Projetos(0)
        projetos.append(Projeto(0,'','', '','','','',0,0, ''))
        proj = [x for x in projetos if x.codigo_projeto == 0][0]
        g.proj = proj
    else:
        form = request.form
        if form['btn_projeto'] == 'btn_salvar_projeto':
            projeto = form.get('txtProjeto')
            local = form.get('txtLocal_Projeto')
            orcamento = form.get('txtOrcamento_Projeto').replace('.','').replace(',','.')
            prazo = form.get('txtPrazo_Dias')
            dataInicio = form.get('txtData_Inicio')
            dataFim = form.get('txtData_Fim')
            idCliente = form.get('cbCliente')
            idStatus = form.get('cbStatus')
            obs = form.get('txtObs')
            Insert_New_Project(projeto, local, orcamento, prazo, dataInicio, dataFim, idCliente, idStatus, obs, g.func.codigo_func)
            idProjeto = Select_Top_Projeto()
            pasta = 'static/imgs/Projetos/'+str(idProjeto)+'/'
            funcio = form.getlist('ckFunc')
            for cnt in funcio:
                Insert_Func_Proj(idProjeto, cnt)
            func = Listar_Todos_Funcionarios(idProjeto)
            servicos = Listar_Servicos_Projetos(idProjeto)
            proj = [x for x in projetos if x.codigo_projeto == idProjeto][0]
            if proj:
                g.proj = proj
                g.proj.orcamento = str(g.proj.orcamento)[0:-3]
            else:
                proj = [x for x in projetos if x.codigo_projeto == idProjeto][0]
                g.proj = proj
        elif form['btn_projeto'] == 'btn_alterar_projeto':
            idProjeto = int(form.get('txtCodigoProjeto'))
            projeto = form.get('txtProjeto')
            local = form.get('txtLocal_Projeto')
            orcamento = form.get('txtOrcamento_Projeto').replace('.','').replace(',','.')
            prazo = form.get('txtPrazo_Dias')
            dataInicio = form.get('txtData_Inicio')
            dataFim = form.get('txtData_Fim')
            idCliente = form.get('cbCliente')
            idStatus = form.get('cbStatus')
            obs = form.get('txtObs')
            Alterar_Project(idProjeto, projeto, local, orcamento, prazo, dataInicio, dataFim, idCliente, idStatus, obs, g.func.codigo_func)
            pasta = 'static/imgs/Projetos/'+str(idProjeto)+'/'
            Select_Projeto_Selecionado(idProjeto)
            servicos = Listar_Servicos_Projetos(idProjeto)
            funcio = form.getlist('ckFunc')
            codigos_funcs = ''
            for cnt in funcio:
                Insert_Func_Proj(idProjeto, cnt)
                codigos_funcs = codigos_funcs + cnt + ','
            if codigos_funcs:
                Alterar_Func_Projeto(idProjeto, codigos_funcs[:len(codigos_funcs)-1])
            else:
                Limpar_Func_Projeto(idProjeto)
            func = Listar_Todos_Funcionarios(idProjeto)
            proj = [x for x in projetos if x.codigo_projeto == idProjeto][0]
            if proj:
                g.proj = proj
                g.proj.orcamento = str(g.proj.orcamento)[0:-3]
        elif form['btn_projeto'] == 'btn_select_projeto':
            idProjeto = int(form.get('idProjeto'))
            pasta = 'static/imgs/Projetos/'+str(idProjeto)+'/'
            func = Listar_Todos_Funcionarios(idProjeto)
            Select_Projeto_Selecionado(idProjeto)
            servicos = Listar_Servicos_Projetos(idProjeto)
            proj = [x for x in projetos if x.codigo_projeto == idProjeto][0]
            if proj:
                g.proj = proj
                g.proj.orcamento = str(g.proj.orcamento)[0:-3]
        elif form['btn_projeto'] == 'btn_insert_servio':
            idProjeto = int(form.get("txtcodigo_pro"))
            pasta = 'static/imgs/Projetos/'+str(idProjeto)+'/'
            func = Listar_Todos_Funcionarios(idProjeto)
            osServico = form.getlist("ckServicos")
            Delete_All_Servicos(idProjeto)
            for cnt in osServico:
                Insert_and_Update_Servicos(idProjeto, cnt, int(form.get(cnt)))
            servicos = Listar_Servicos_Projetos(idProjeto)
            proj = [x for x in projetos if x.codigo_projeto == idProjeto][0]
            if proj:
                g.proj = proj
                g.proj.orcamento = str(g.proj.orcamento)[0:-3]
        elif form['btn_projeto'] == "btn_insert_img":   
            idProjeto = int(form.get("txtcodigo_pro"))
            pasta = 'static/imgs/Projetos/'+str(idProjeto)+'/'
            func = Listar_Todos_Funcionarios(idProjeto)
            #img = form.get('fileImagens')
            if not os.path.isdir(pasta):
                os.mkdir(pasta)
            if request.files:
                file = request.files["fileImagens"]
                #if os.path.isfile(pasta+file.filename):
                #    os.remove(pasta+file.filename)
                checkCapa = form.get("checkCapa")
                if checkCapa:
                    setor = 'Projeto_Capa_'+str(idProjeto)
                    extencao = pegaExtencaoImg(file.filename)
                    nomeImg = "Capa."+extencao
                else:
                    setor = 'Projeto_'+str(idProjeto)
                    nomeImg = file.filename
                file.save(pasta+'/'+nomeImg)
                Insert_Imagem('/'+pasta, nomeImg, setor,'','1')
            #shutil.copy(img,pasta)            
            servicos = Listar_Servicos_Projetos(idProjeto)
            proj = [x for x in projetos if x.codigo_projeto == idProjeto][0]
            if proj:
                g.proj = proj
                g.proj.orcamento = str(g.proj.orcamento)[0:-3]
        elif form['btn_projeto'] == "btn_delete_img":
            idProjeto = form.get("txtcodigo_pro")
            idProjeto = int(idProjeto)
            imagemName = form.get("img_projeto")
            pasta = 'static/imgs/Projetos/'+str(idProjeto)+'/'
            func = Listar_Todos_Funcionarios(idProjeto)
            if os.path.isfile(pasta+imagemName):
                os.remove(pasta+imagemName)
            Delete_Img_Projeto('/'+pasta, imagemName)
            servicos = Listar_Servicos_Projetos(idProjeto)
            proj = [x for x in projetos if x.codigo_projeto == idProjeto][0]
            if proj:
                g.proj = proj
                g.proj.orcamento = str(g.proj.orcamento)[0:-3]
        elif form['btn_projeto'] == "btn_apagar_projeto":
            idProjeto = int(form.get('idProjeto'))
            pasta = 'static/imgs/Projetos/'+str(idProjeto)+'/'
            if os.path.isdir(pasta):
                shutil.rmtree(pasta)
            Delete_Todo_Projeto(idProjeto)
            return redirect('/profile/Projetos/')
    ImagensProjeto = Listar_Imagem_Projetos('/'+pasta)
    retorno=0
    msgModal=""
    titulo=''
    return render_template(
        'Projetos_admin.html',
        clientes = clientes,
        status = status,
        funcionarios = func,
        osProjetos = osProjetos,
        servicos = servicos,
        ImagensProjeto = ImagensProjeto,
        retorno=retorno,
        msgModal=msgModal,
        titulo=titulo
    )



@admin_dp.route('/Lista_Projetos_Admin/', methods=['GET', 'POST'])
def Lista_Projetos_Admin():
    if request.method == 'GET':
        projetos = Listar_Todos_Projetos()
        return render_template(
            'lista_projetos_admin.html',
            projetos = projetos,
            retorno = retorno,
            titulo = titulo,
            msgModal = msgModal
        )
    else:
        form = request.form
        if form['btn_projeto'] == 'btn_select_projeto':
           return redirect('/Projetos_Admin/')
        

@admin_dp.route('/Projeto_Cliente/<codigo_projeto>/', methods=['GET', 'POST'])
def Projeto_Cliente(codigo_projeto):
    if 'user_type' in session:
        user = [x for x in users if x.user_type == session['user_type']][0]
        g.user = user
    g.func = 'funcao:'
    Select_Projeto_Selecionado(codigo_projeto)
    proj = [x for x in projetos if x.codigo_projeto == int(codigo_projeto)][0]
    if proj:
        g.proj = proj
        g.proj.orcamento = str(g.proj.orcamento)[0:-3]
    statusPro = Listar_Servicos_Projetos(g.proj.codigo_projeto)    
    stServico = []
    stProgress = []
    stCoresBarra = []
    for cnt in statusPro:
        if cnt[2] == 'checked':
            stServico.append(cnt[1])
            stProgress.append(cnt[3])
            stCoresBarra.append(coresBarra(cnt[3]))
    pasta = 'static/imgs/Projetos/'+str(codigo_projeto)+'/'
    ImagensProjeto = Listar_Imagem_Projetos('/'+pasta)
    retorno = ''
    titulo = ''
    msgModal = ''
    return render_template(
        'projetos_clientes.html',
        stServico = stServico,
        stProgress=stProgress,
        stCoresBarra=stCoresBarra,
        ImagensProjeto=ImagensProjeto,
        retorno = retorno,
        titulo = titulo,
        msgModal = msgModal
        )


@admin_dp.app_template_filter()
def formatingTelefone(value):
    if value:
        strValue = str(value)
        if len(strValue) == 9:
            telefone = str(strValue[0]) + ' ' + str(strValue[1:5]) + '-' + str(strValue[5:])
        else:
            telefone = str(strValue[1:4]) + '-' + str(strValue[4:])
    else:
        telefone = ''
    return telefone

@admin_dp.app_template_filter()
def formatingCPF(value):
    if value:
        strValue = str(value)
        cpf = str(strValue[:3]) + "." + str(strValue[3:6]) + "." + str(strValue[6:9]) + "-" + str(strValue[9:])
    else:
        cpf = ''
    return cpf


@admin_dp.route('/Funcionarios/', methods=['GET', 'POST'])
def Funcionarios():
    if 'user_type' in session:
        user = [x for x in users if x.user_type == session['user_type']][0]
        g.user = user
        Select_Func_Data(g.user.codigo)
        func = [x for x in funcionarios if x.codigo_usuario == g.user.codigo][0]
        if func:
            g.func = func
            Listar_Todos_Funcionarios_Cadastrados()
        g.umFunc = ''
    usuario = [['','','']]
    retorno = 0
    titulo = ''
    msgModal = ''
    cargos = Listar_Cargos()
    tpUsuario = Listar_Tipo_Usuario()
    if request.method == 'GET':
        func = Listar_Todos_Funcionarios(0)
        usuario = [['','','']]
        perUsuario = Listar_Permissoes_Usuarios(0)
    elif request.method == 'POST':        
        form = request.form
        if form['btn_admin_func'] == 'btn_select_func':
            codigo_func = form.get('codigo_func')
            umFunc = [x for x in todos_Func if x.codigo_func == int(codigo_func)][0]
            if umFunc:
                g.umFunc = umFunc
        elif form['btn_admin_func'] == 'btn_apagar_func':
            codigo_func = form.get('codigo_func')
            oFunc = [x for x in todos_Func if x.codigo_func == int(codigo_func)][0]
            Delete_Todo_Func(int(codigo_func), int(Nz(oFunc.codigo_usuario)))
            Listar_Todos_Funcionarios_Cadastrados()
        elif form['btn_admin_func'] == 'btn_salvar_func':
            nome = form.get('txtNome')
            cpf = form.get('txtCPF').replace(".","").replace("-","")
            email = form.get('txtemail')
            cargo = form.get('cbCargo')
            check = form.get('chkUsuario')
            perm = form.getlist('ckPermisao')
            result = Insert_New_Func(nome, cpf, email, cargo)
            if result[0] == 1062:
                retorno = 1
                titulo = 'Erro: ' + str(result[0])
                msgModal = 'Já existe esse ' + result[1].upper() + ' Cadastrado! <br> Tente outro ' + result[1].upper() + '.'
                umFunc = todos_Func[0]
                if umFunc:
                    g.umFunc = umFunc
                g.umFunc.codigo_func = 0
                g.umFunc.nome = nome
                g.umFunc.cpf = cpf
                g.umFunc.email = email
                g.umFunc.codigo_funcao = int(cargo)
                g.umFunc.codigo_usuario = 0
            else:
                retorno = 0
                titulo = ''
                msgModal = ''
                codigo_func = Select_Top_Func()
                if not check is None:
                    usuario = form.get('txtUsuario')
                    tpUsua = form.get('cbUsuario')
                    Insert_New_Usuario(usuario, usuario, tpUsua)
                    codigo_usuario = Select_Top_Usuario()
                    Insert_Usuario_Func(codigo_func, codigo_usuario)
                    Delete_All_Permissoes(codigo_usuario)
                    for cnt in perm:
                        Insert_Permisao_Usuario(int(cnt), codigo_usuario)
                Listar_Todos_Funcionarios_Cadastrados()
                umFunc = [x for x in todos_Func if x.codigo_func == int(codigo_func)][0]
                if umFunc:
                    g.umFunc = umFunc
        elif form['btn_admin_func'] == 'btn_alterar_func':
            codigo_func = form.get('txtCodigoFuncionario')
            nome = form.get('txtNome')
            cpf = form.get('txtCPF').replace(".","").replace("-","")
            email = form.get('txtemail')
            cargo = form.get('cbCargo')
            check = form.get('chkUsuario')
            perm = form.getlist('ckPermisao')
            Alterar_Dados_Func(codigo_func, nome, cpf, email, cargo)
            if not check is None:
                codigo_usuario = form.get('txtcodigo_usuario')
                usuario = form.get('txtUsuario')
                senha = None
                tpUsua = form.get('cbUsuario')
                if codigo_usuario:
                    Alterar_Dados_usuario(codigo_usuario, senha, tpUsua)
                else:
                    result = Insert_New_Usuario(usuario, usuario, tpUsua)
                    if result[0] == 1062:
                        retorno = 1
                        titulo = 'Erro: ' + str(result[0])
                        msgModal = 'Já existe o ' + result[1] + ' ' + usuario.upper() + ' Cadastrado! <br> Tente um novo usuário.'
                        usuario = [['',usuario,int(tpUsua)]]
                    else:
                        retorno = 0
                        titulo = ''
                        msgModal = ''
                    codigo_usuario = Select_Top_Usuario()
                    Insert_Usuario_Func(codigo_func, codigo_usuario)
                Delete_All_Permissoes(codigo_usuario)
                for cnt in perm:
                    Insert_Permisao_Usuario(int(cnt), codigo_usuario)
            Listar_Todos_Funcionarios_Cadastrados()
            umFunc = [x for x in todos_Func if x.codigo_func == int(codigo_func)][0]
            if umFunc:
                g.umFunc = umFunc
        if g.umFunc:
            if g.umFunc.codigo_usuario:
                usuario = Listar_Usuario_Func(g.umFunc.codigo_usuario)
                perUsuario = Listar_Permissoes_Usuarios(g.umFunc.codigo_usuario)
            else:
                perUsuario = Listar_Permissoes_Usuarios(0)
                g.umFunc.codigo_usuario = 0
        else:
            perUsuario = Listar_Permissoes_Usuarios(0)
    tFunc = [x for x in todos_Func if x.codigo_func > 0]
    if tFunc:
        g.tFunc = tFunc
    return render_template(
            'cadastro_funcionarios.html',
            funcionarios = func,
            cargos=cargos,
            usuario=usuario,
            tpUsuario=tpUsuario,
            perUsuario=perUsuario,
            retorno=retorno,
            msgModal=msgModal,
            titulo=titulo
        )







@admin_dp.route('/Clientes/', methods=['GET', 'POST'])
def Clientes():
    if 'user_type' in session:
        user = [x for x in users if x.user_type == session['user_type']][0]
        g.user = user
        Select_Func_Data(g.user.codigo)        
        func = [x for x in funcionarios if x.codigo_usuario == g.user.codigo][0]
        if func:
            g.func = func
        Listar_Todos_Clientes_Cadastrados()     
        retorno = 0
        titulo = ''
        msgModal = ''
        func = Listar_Todos_Funcionarios(0)
        g.umClie = ''
    if request.method == 'GET':
        usuario=[['','','']]
    elif request.method == 'POST':
        form = request.form
        if form['btn_admin_cli'] == 'btn_select_cli':
            codigo_cli = form.get('codigo_cli')
            umClie = [x for x in todos_cli if x.codigo_cli == int(codigo_cli)][0]
            if umClie:
                g.umClie = umClie
                usuario = Listar_Usuario_Func(g.umClie.codigo_usuario)
        elif form['btn_admin_cli'] == 'btn_salvar_func':
            usuario = form.get('txtUsuario')
            Insert_New_Usuario(usuario, usuario, 3)
            codigo_usuario = Select_Top_Usuario()
            nome_cli = form.get('txtNome')
            email = form.get('txtemail')
            telefone = form.get('txtTelefone')
            Insert_New_Cliente(codigo_usuario, nome_cli, email, telefone)
            Listar_Todos_Clientes_Cadastrados()
            umClie = [x for x in todos_cli if x.codigo_cli == todos_cli[-1].codigo_cli][0]
            if umClie:
                g.umClie = umClie
                usuario = Listar_Usuario_Func(todos_cli[-1].codigo_usuario)
        elif form['btn_admin_cli'] == 'btn_apagar_cli':
            pass
        elif form['btn_admin_cli'] == 'btn_resete_password':
            pass
        elif form['btn_admin_cli'] == 'btn_alterar_func':
            pass
    tclie = [x for x in todos_cli if x.codigo_cli > 0]
    if tclie:
        g.tclie = tclie
    return render_template(
        'cadastro_clientes.html',
        funcionarios=func,
        usuario=usuario,
        retorno = retorno,
        titulo = titulo,
        msgModal = msgModal
    )





@admin_dp.route('/Home_Page/', methods=['GET', 'POST'])
def Home_Page():
    if 'user_type' in session:
        user = [x for x in users if x.user_type == session['user_type']][0]
        g.user = user
        Select_Func_Data(g.user.codigo)        
        func = [x for x in funcionarios if x.codigo_usuario == g.user.codigo][0]
        if func:
            g.func = func
    if request.method == 'GET':
        func = Listar_Todos_Funcionarios(0)
        retorno=0
        msgModal=''
        titulo=''
        return render_template(
            'manutencao_home.html',
            funcionarios = func,
            retorno=retorno,
            msgModal=msgModal,
            titulo=titulo
        )
    else:
        pass




@admin_dp.route('/Blog/', methods=['GET', 'POST'])
def Blog():
    if 'user_type' in session:
        user = [x for x in users if x.user_type == session['user_type']][0]
        g.user = user
        Select_Func_Data(g.user.codigo)        
        func = [x for x in funcionarios if x.codigo_usuario == g.user.codigo][0]
        if func:
            g.func = func
    if request.method == 'GET':
        func = Listar_Todos_Funcionarios(0)
        retorno=0
        msgModal=''
        titulo=''
        return render_template(
            'manutencao_blog.html',
            funcionarios = func,
            retorno=retorno,
            msgModal=msgModal,
            titulo=titulo
        )
    else:
        pass


















def Nz(valor):
    if valor is None:
        return 0
    return valor

def pegaExtencaoImg(nomeImagem):
    lista_N = nomeImagem.split('.')
    return lista_N[len(lista_N)-1]

def coresBarra(val):
    cor = ''
    if val <= 25:
        cor = 'rgba(133, 0, 0, 0.9)'
    elif val <=50:
        cor = 'rgba(255, 165, 0, 0.9)'
    elif val <= 75:
        cor = 'rgba(200, 200, 0, 0.9)'
    elif val < 100:
        cor = 'rgba(0, 123, 0, 0.9)'
    else:
        cor = 'rgba(0, 0, 200, 0.9)'
    return cor