from flask import render_template, request, redirect, Blueprint, url_for, g, session
from path import Path
from app import app
import os.path
from conexao import *
from PRGT_Bot_Telegram import *




@app.route('/', methods=['GET','POST'])
def index():
    Tabela = selecionarTabela()
    slide = selecionarImagens('slide_home')
    gallery_container = selecionarImagens('galery_container_home')
    if request.method == 'GET':
        session.pop('user_type', None)
        session['tentativa_login'] = 0  
        return render_template(
            'index.html',
            Tabela = Tabela,
            slide = slide,
            gallery_container = gallery_container,
            msgLog=''       
        )
    elif request.method == 'POST':
        form = request.form
        if form["btn_home"] == "btn_login":
            usuario = form.get("usuario")
            senha = form.get("senha")
            retur = Autentic_Usuario(usuario, senha)
            if retur > 0:
                if retur == 2:
                    session['tentativa_login'] = session['tentativa_login'] + 1
                    msgLog = 'Usuário logado em outro aparelho! <br> +' + str((3 - session['tentativa_login'])) + ' tentativas o ele será deslogado'
                    if session['tentativa_login'] == 3:
                        for cnt in range(len(users)):
                            if users[cnt].username == usuario:
                                users.pop(cnt)
                                msgLog = 'O usuário foi derrubado <br> Por favor, tente logar novamente.'
                                break
                    return render_template(
                    'index.html',
                    titulo = 'Falha na autenticação.',
                    msgLog = msgLog
                    )
                user = [x for x in users if x.username == usuario][0]
                if user:
                    session['user_type'] = user.user_type
                    session['username'] = user.username
                    return redirect(url_for('profile'))
            else:
                return render_template(
                    'index.html',
                    titulo = 'Falha na autenticação.',
                    msgLog = 'Usuario ou senha errado!'
                    )
        elif form["btn_home"] == "btn_msg":            
            nome = form.get("name")
            email = form.get("email")
            tele = form.get("phone")
            msg = form.get("message")
            mensagem = "Nome: " + nome + "\nTelefone: " + tele + "\nEmail: " + email + "\n\nMensagem: \n" + msg
            bot = TelegramBot()
            bot.Iniciar(mensagem)
            return render_template(
                'index.html'
                )

@app.route('/blog/', methods=['GET', 'POST'])
def blog():
    slide = selecionarImagens('slide_home')
    img_blog = selecionarImagens_Blog('blog_pg')
    if request.method == 'GET':        
        return render_template(
            'blog.html',
            slide = slide,
            img_blog = img_blog
        )
    elif request.method == 'POST':
        form = request.form                
        usuario = form.get("usuario")
        senha = form.get("senha")
        retur = Autentic_Usuario(usuario, senha)
        if retur > 0:
            if retur == 2:
                return render_template(
                'blog.html',
                titulo = 'Falha na autenticação.',
                msgLog = 'Usuário logado em outro aparelho!'
                )
            user = [x for x in users if x.username == usuario][0]
            if user:
                session['user_type'] = user.user_type
                session['username'] = user.username
                return redirect(url_for('profile'))
        else:
            return render_template(
                'blog.html',
                titulo = 'Falha na autenticação.',
                msgLog = 'Usuario ou senha errado!'
                )

    
@app.route('/Deslogar/', methods=['GET', 'POST'])
def Deslogar():
    form = request.args
    usuario = form.get("txtUsuarioLogado")
    for cnt in range(len(users)):
        if users[cnt].username == usuario:
            users.pop(cnt)
            break
    return redirect('/')


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    if 'user_type' in session:
        user = [x for x in users if x.username == session['username']][0]
        g.user = user
        if g.user.user_type == 'Dev' or g.user.user_type == 'admin':
            return redirect('/admin/')        
        elif g.user.user_type == 'func':    
            return render_template('admin.html')
        elif g.user.user_type == 'cliente':
            return redirect('/cliente/')
        

