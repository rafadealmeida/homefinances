from flask import Flask,render_template,request, flash,redirect,url_for,session
import urllib.parse
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from Usuario import Usuario
from Despesas import Despesas

app = Flask(__name__)

app.secret_key = 'sdaghbduj31igdasdojhasjdaidjioasgh7568duisd3489yu5t89wre4f'

user = "root"
password = urllib.parse.quote_plus("senac")
host = "localhost"
database = "homefinance"

connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

engine = create_engine(connection_string)

metadata = MetaData()
metadata.reflect(engine)
Base = automap_base(metadata=metadata)
Base.prepare()

# Animal =  Base.classes.animal
Usuario = Base.classes.user
Despesas = Base.classes.despesas



Session = sessionmaker(bind=engine)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/registra')
def registra():
  return render_template('cadatraUsuario.html')

@app.route('/despesas')
def despesas():
    usuario_id = session.get('usuario_id') 
    if not usuario_id:
        flash('Você precisa estar logado para ver suas despesas.')
        return redirect(url_for('index'))

    session_db = Session()
    despesas_lista = []

    try:
        despesas_lista = session_db.query(Despesa).filter_by(usuario_id=usuario_id).all()
    except Exception as e:
        flash('Erro ao carregar as despesas: ' + str(e))
    finally:
        session_db.close()

    return render_template('listaDespesa.html', despesas=despesas_lista)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        if not email or not senha:  
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('index'))

        session_db = Session()  

        try:
            usuario = session_db.query(Usuario).filter_by(email_user=email).first()
            
            if usuario and usuario.password_user == senha: 
                session['usuario_id'] = usuario.id
                session['usuario_logado'] = usuario.name_user
                flash(usuario.name_user + ' logado com sucesso!')
                return redirect(url_for('despesas'))
            else:
                flash('Email ou senha incorretos.')
                return redirect(url_for('index'))
        
        except Exception as e:
            flash('Erro ao processar o login: ' + str(e))
            return redirect(url_for('index'))
        
        finally:
            session_db.close()
    
    return render_template('index.html')


@app.route('/cadastra', methods=['POST'])
def cadastra_usuario():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    
    session = Session()

    usuario = Usuario(name_user=nome, email_user=email, password_user=senha)

    try:
        session.add(usuario)
        session.commit()
        flash('Usuário criado com sucesso!')
    except Exception as e:
        session.rollback()
        flash('Erro ao criar o Usuário: ' + str(e))
    finally:
        session.close()
    
    return redirect(url_for('index'))

@app.route('/cadastraDespesa', methods= ['GET','POST'])
def cadastra_despesa():
    if request.method == 'POST':
        valor = request.form['valor']
        data = request.form['data']
        tipo = request.form['tipo']
        nome = request.form['nome']
        
        usuario_id = session.get('usuario_id')  

        session_db = Session()

        despesas = Despesas(valor=valor, data=data, tipo=tipo, usuario_id=usuario_id,nome=nome)

        try:
            session_db.add(despesas)
            session_db.commit()
            flash('Despesas cadastrada com sucesso!')
        except Exception as e:
            session_db.rollback()
            flash('Erro ao cadastrar a Despesas: ' + str(e))
        finally:
            session_db.close()
        
        return redirect(url_for('despesas'))
    
    return render_template('cadastrarDespesa.html')


app.run(debug=True)
