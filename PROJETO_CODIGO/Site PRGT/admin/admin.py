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
            idProjeto = int(form.get("txtcodigo_pro"))
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
    return render_template(
        'Projetos_admin.html',
        clientes = clientes,
        status = status,
        funcionarios = func,
        osProjetos = osProjetos,
        servicos = servicos,
        ImagensProjeto = ImagensProjeto
    )



@admin_dp.route('/Lista_Projetos_Admin/', methods=['GET', 'POST'])
def Lista_Projetos_Admin():
    if request.method == 'GET':
        projetos = Listar_Todos_Projetos()
        return render_template(
            'lista_projetos_admin.html',
            projetos = projetos
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
    for cnt in statusPro:
        if cnt[2] == 'checked':
            stServico.append(cnt[1])
            stProgress.append(cnt[3])
    return render_template(
        'projetos_clientes.html',
        stServico = stServico,
        stProgress=stProgress
        )


def pegaExtencaoImg(nomeImagem):
    lista_N = nomeImagem.split('.')
    return lista_N[len(lista_N)-1]

