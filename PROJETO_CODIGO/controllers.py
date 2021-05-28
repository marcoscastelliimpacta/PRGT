from flask import render_template, request, redirect, Blueprint, url_for, g, session
from app import app
import os.path
from conexao import *




@app.route('/', methods=['GET','POST'])
def index():
    Tabela = selecionarTabela()
    slide = selecionarImagens('slide_home')
    gallery_container = selecionarImagens('galery_container_home')
    if request.method == 'GET':
        session.pop('user_type', None)      
        return render_template(
            'index.html',
            Tabela = Tabela,
            slide = slide,
            gallery_container = gallery_container        
        )
    elif request.method == 'POST':
        form = request.form
                
        usuario = form.get("usuario")
        senha = form.get("senha")
        retur = Autentic_Usuario(usuario, senha)
        if retur > 0:
            if retur == 2:
                return render_template(
                'index.html',
                titulo = 'Falha na autenticação.',
                msgLog = 'Usuário logado em outro aparelho!'
                )
            user = [x for x in users if x.username == usuario][0]
            if user:
                session['user_type'] = user.user_type
                return redirect(url_for('profile'))
        else:
            return render_template(
                'index.html',
                titulo = 'Falha na autenticação.',
                msgLog = 'Usuario ou senha errado!'
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
        user = [x for x in users if x.user_type == session['user_type']][0]
        g.user = user
        if g.user.user_type == 'Dev' or g.user.user_type == 'admin':
            return redirect('/admin/')        
        elif g.user.user_type == 'func':    
            return render_template('admin.html')
        elif g.user.user_type == 'cliente':
            return redirect('/cliente/')
        

