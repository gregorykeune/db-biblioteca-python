from sqlalchemy import create_engine, Column, String, Integer, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import date, datetime, timedelta
import pandas as pd
from decimal import Decimal

db = create_engine("sqlite:///banco_de_dados.db")
#cria a sessao
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()
#tabelas

class Usuario(Base):  # Conta do cliente
    __tablename__ = "usuarios" #nome da tabela

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    nome = Column("nome", String)
    data_nascimento = Column("data_nascimento", Date)
    endereco = Column("endereco", String)
    telefone = Column("telefone", String)
    data_registro = Column("data_registro", Date)
    email = Column("email", String)
    senha = Column("senha", String)

    def __init__(self, nome, data_nascimento, endereco, telefone, data_registro, email, senha):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.telefone = telefone
        self.data_registro = data_registro
        self.email = email
        self.senha = senha

class Funcionario(Base):
    __tablename__ = "funcionarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    data_nascimento = Column("data_nascimento", Date)
    endereco = Column("endereco", String)
    telefone = Column("telefone", String)
    data_contratacao = Column("data_contratacao", Date)
    id_cargo = Column("id_cargo", Integer, ForeignKey("cargos.id"))

    def __init__(self, nome, data_nascimento, endereco, telefone, data_contratacao, id_cargo):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.telefone = telefone
        self.data_contratacao = data_contratacao
        self.id_cargo = id_cargo

class Cargo(Base):
    __tablename__ = "cargos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    descricao_cargo = Column("descricao_cargo", String)
    salario = Column("salario", DECIMAL(8, 2))
    carga_horaria = Column("carga_horaria", String)

    def __init__(self, descricao_cargo, salario, carga_horaria):
        self.descricao_cargo = descricao_cargo
        self.salario = salario
        self.carga_horaria = carga_horaria

class Livro(Base):
    __tablename__ = "livros"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo", String)
    autor = Column("autor", String)
    isbn = Column("isbn", Integer)
    data_publicacao = Column("data_publicacao", Date)
    estoque = Column("estoque", Integer)
    valor = Column("valor", DECIMAL(8,2))
    id_editora = Column("id_editora", Integer, ForeignKey("editoras.id"))

    def __init__(self, titulo, autor, isbn, data_publicacao, estoque, valor, id_editora):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.data_publicacao = data_publicacao
        self.estoque = estoque
        self.valor = valor
        self.id_editora = id_editora

class Editora(Base):
    __tablename__ = "editoras"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    endereco = Column("endereco", String)

    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco

class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    data_emprestimo = Column("data_emprestimo", Date)
    data_devolucao = Column("data_devolucao", Date)
    id_cliente = Column("id_cliente", Integer, ForeignKey("usuarios.id"))
    id_funcionario = Column("id_funcionario", Integer, ForeignKey("funcionarios.id"))
    id_livro = Column("id_livro", Integer, ForeignKey("livros.id"))

    def __init__(self, data_emprestimo, data_devolucao, id_usuario, id_funcionario, id_livro):
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao
        self.id_usuario = id_usuario
        self.id_funcionario = id_funcionario
        self.id_livro = id_livro

class Venda(Base):
    __tablename__ = 'vendas'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    valor = Column("valor", DECIMAL(8,2), ForeignKey("livros.valor"))
    id_usuario = Column("id_usuario", Integer, ForeignKey("usuarios.id"))
    id_funcionario = Column("id_funcionario", Integer, ForeignKey("func ionarios.id"))
    id_livro = Column("id_livro", Integer, ForeignKey("livros.id"))

    def __init__(self, valor, id_usuario, id_funcionario, id_livro):
        self.valor = valor
        self.id_usuario = id_usuario
        self.id_funcionario = id_funcionario
        self.id_livro = id_livro

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=db)

# Função para verificar a senha de admin
def senha_adm():
    for i in range(3):
        senha = input('Senha: ')
        if senha == 'GregoryKeune':
            return True
        else:
            print('\33[1;49;31m \nSenha inválida\33[0m\n')
            if i == 2:
                print('Redirecionando para o modo consumidor\n')
                return False
            
# Função para criar um novo
def criar_usuario():
    nome = input("Nome: ")
    data_nascimento_str = input("Data de nascimento (DD/MM/AAAA): ")
    data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y").date()
    endereco = input("Endereço: ")
    telefone = input("Telefone: ")
    data_registro =  date.today()

    # Loop para verificar se ja existe um usuario com o email do cadastro
    while True:
        email = input("Email: ")

        email_existe = session.query(Usuario).filter_by(email=email).first()  

        if not email_existe:
            senha = input("Senha: ")

            novo_usuario = Usuario(
                nome=nome,
                data_nascimento=data_nascimento,
                endereco=endereco,
                telefone=telefone,
                data_registro=data_registro,
                email=email,
                senha=senha
            )
            session.add(novo_usuario)
            session.commit()
            print("Usuário criado com sucesso!")
            break
        print("Ja existe um usuario com esse email")
    

# Função para fazer o print organizado das tabelas
def printar_tabela(tabela, nome_tabela):
    id_tabelas = session.query(tabela).order_by(tabela.id).all()
    print(id_tabelas)        
    ver_tabelas = pd.read_sql_table(nome_tabela,session.bind)
    print("\n", ver_tabelas, "\n")


# Função para atualizar os atributos de uma tabela
def update_tabela(tabela, id_objeto, atributos):
    # Busca o objeto na tabela pelo ID (id_objeto)
    objeto_modificado = session.get(tabela, id_objeto)
    
    if objeto_modificado:
        for atributo in atributos:
            # Obtém o valor atual do atributo
            valor_atual = getattr(objeto_modificado, atributo)
            alterar = int(input(f"Deseja alterar '{atributo}' (valor atual: {valor_atual})?\n[1] SIM\n[2] NÃO\n-> "))
            
            if alterar == 1:
                # Captura o novo valor do usuário
                if atributo == ('data_nascimento' or atributo == 'data_contracao' or atributo == 'data_publicacao'):
                    data_str = input(f"{atributo} (DD/MM/AAAA): ")
                    novo_valor = datetime.strptime(data_str, "%d/%m/%Y").date()
                else:
                    novo_valor = input(f"Digite o novo valor para '{atributo}': ")
                    
                    # Converte o tipo se necessário, baseado no tipo atual
                    if isinstance(valor_atual, int):
                        novo_valor = int(novo_valor)
                    elif isinstance(valor_atual, float):
                        novo_valor = float(novo_valor)
                    elif isinstance(valor_atual, Decimal):
                        novo_valor= Decimal(novo_valor)
                
                # Define o novo valor do atributo no objeto
                setattr(objeto_modificado, atributo, novo_valor)
        
        # Salva as alterações no banco de dados
        session.commit()
        print("Tabela atualizada com sucesso!")
    else:
        print("Objeto não encontrado!")

# Função para criar objetos no banco
def criar_objeto(tabela, atributos):
    #dicionario para armazenar os valores dos novos atributos antes de inserir no banco
    valores = {}

    #loop com nome dos atributos a serem inseridos no banco 
    for atributo in atributos:
        if atributo in ('data_nascimento', 'data_contratacao', 'data_publicacao'):
            data_str = input(f"{atributo} (DD/MM/AAAA): ")
            novo_valor = datetime.strptime(data_str, "%d/%m/%Y").date() #transforma a data do tipo string para date
        else:
            novo_valor = input(f"{atributo}: ")
            coluna = getattr(tabela, atributo)

            #isinstance(coluna.type, tipo)
            if isinstance(coluna.type, Integer):
                novo_valor = int(novo_valor)
            elif isinstance(coluna.type, DECIMAL):
                novo_valor = Decimal(novo_valor)

        valores[atributo] = novo_valor

    novo_objeto = tabela(**valores)           
    session.add(novo_objeto)
    session.commit()
                
# Menu inicial
adm = int(input('[1] Usuário\n[2] Adm\n-> '))


# Se o usuário for cliente
if adm == 1:
    while True:
        modo_usuario = int(input("[1] Entrar com usuário ja existente \n[2] Criar Usuário \n[3] Sair\n-> "))
        if modo_usuario == 1:
            while True:        
                confirmar_email = input("Email: ")
                confirmar_senha = input("Senha:")
                
                usuario = session.query(Usuario).filter_by(email=confirmar_email).first()

                if usuario:
                    if confirmar_senha == usuario.senha:
                        print(f"Login feito com sucesso, bem vindo {usuario.nome}")
                        break
                
                print("email ou senha incorreto")
            
            navegar_livros = int(input("[1] Ver Livros \n[2] Sair \n-> "))
            printar_tabela(Livro, 'livros')
            pegar_livro = int(input("Escolha um livro (Insira a ID, caso não queira nenhum insira '0'): "))
            if pegar_livro != 0:
                id_livro = pegar_livro
                conferir_livro = session.query(Livro).filter_by(id=id_livro).first()
                if conferir_livro:
                    tipo_transacao = int(input("[1] Comprar \n[2] Emprestar \n-> "))
                    printar_tabela(Funcionario, 'funcionarios')
                    id_funcionario = int(input("Qual funcionário te atendeu? (Insira o ID): "))
                    usuario = session.query(Usuario).filter_by(email=confirmar_email).first()
                    id_usuario = usuario.id
                    livro = session.query(Livro).filter_by(id=id_livro).first()
                    if tipo_transacao == 1:
                        valor = livro.valor

                        nova_venda = Venda(
                            valor=valor,
                            id_usuario=id_usuario,
                            id_funcionario=id_funcionario,
                            id_livro=id_livro,
                        )
                        if livro.estoque > 0:
                            livro.estoque -= 1
                            session.add(nova_venda)
                            session.commit()
                            print("Compra efetuada com sucesso!")
                        else:
                            print("Livro indisponivel.")

                    if tipo_transacao == 2:
                        data_emprestimo = date.today()
                        data_devolucao = data_emprestimo + timedelta(days=30)
                            
                        novo_emprestimo = Emprestimo(
                            id_usuario=id_usuario,
                            id_funcionario=id_funcionario,
                            id_livro=id_livro,
                            data_emprestimo=data_emprestimo,
                            data_devolucao=data_devolucao
                            )
                        if livro.estoque > 0:
                            livro.estoque -= 1
                            session.add(novo_emprestimo)
                            session.commit()
                            print("Emprestimo feito com sucesso!")
                        else:
                            print("Livro indisponivel.")

                else:    
                    print("Este livro não existe\n")
                
                break

        elif modo_usuario == 2:
            criar_usuario()

        elif modo_usuario == 3:
            print("Muito obrigado, até a próxima!")
            break

# Se o usuário for admin
if adm == 2:
    if senha_adm():
        while True:
            modificar = int(input('Deseja alterar algo?\n[1] Usuarios\n[2] Funcionarios'
                                '\n[3] Cargos\n[4] Livros \n[5] Editoras \n[6] Vendas \n[7] Emprestimos \n-> '))
            #modificação de usuarios
            if modificar == 1:
                tipo_modificacao = int(input("[1] Criar Usuario \n[2] Deletar Usuario \n[3] Atualizar Usuario \n[4] Ver Usuarios \n-> "))
                
                if tipo_modificacao == 1:
                    criar_usuario()

                elif tipo_modificacao == 2:
                    printar_tabela(Usuario, 'usuarios')
                    id_usuario = int(input("ID do usuário a ser deletado: "))
                    usuario_para_deletar = session.get(Usuario, id_usuario)
                    if usuario_para_deletar:
                        session.delete(usuario_para_deletar)
                        session.commit()
                        print("Usuário deletado com sucesso!")
                    else:
                        print("Usuário não encontrado.")

                elif tipo_modificacao == 3:
                    printar_tabela(Usuario, 'usuarios')
                    id_usuario_alterado = int(input("Usuario que deseja alterar (Insira a ID) -> "))
                    update_tabela(Usuario, id_usuario_alterado, ['nome', 'data_nascimento', 'email', 'senha', 'telefone', 'endereco'])

                elif tipo_modificacao == 4:
                    printar_tabela(Usuario, 'usuarios')
            
            #modificação de funcionarios
            elif modificar == 2:
                tipo_modificacao = int(input("[1] Criar Funcionario \n[2] Deletar Funcionario \n[3] Atualizar Funcionario \n[4] Ver Funcionarios \n-> "))

                if tipo_modificacao == 1:
                    criar_objeto(Funcionario, ['nome', 'data_nascimento', 'endereco', 'telefone', 'data_contratacao', 'id_cargo'])

                elif tipo_modificacao == 2:
                    id_funcionario = int(input("ID do funcionário a ser deletado: "))
                    funcionario_para_deletar = session.query(Funcionario).get(id_funcionario)
                    if funcionario_para_deletar:
                        session.delete(funcionario_para_deletar)
                        session.commit()
                        print("Funcionário deletado com sucesso!")
                    else:
                        print("Funcionário não encontrado.")

                elif tipo_modificacao == 3:
                    printar_tabela(Funcionario, 'funcionarios')
                    id_funcionario_alterado = int(input("Funcionario que deseja alterar (Insira a ID) -> "))
                    update_tabela(Funcionario, id_funcionario_alterado, ['nome', 'data_nascimento', 'endereco', 'telefone', 'data_contratacao'])

                elif tipo_modificacao == 4:
                    printar_tabela(Funcionario, 'funcionarios')

            # Modificação de Cargos
            elif modificar == 3:
                tipo_modificacao = int(input("[1] Criar Cargo \n[2] Deletar Cargo \n[3] Atualizar Cargo \n[4] Ver Cargos \n-> "))

                if tipo_modificacao == 1:
                    criar_objeto(Cargo, ['descricao_cargo', 'salario', 'carga_horaria'])

                elif tipo_modificacao == 2:
                    id_cargo = int(input("ID do cargo a ser deletado: "))
                    cargo_para_deletar = session.query(Cargo).get(id_cargo)
                    if cargo_para_deletar:
                        session.delete(cargo_para_deletar)
                        session.commit()
                        print("Cargo deletado com sucesso!")
                    else:
                        print("Cargo não encontrado.")
                
                elif tipo_modificacao == 3:
                    printar_tabela(Cargo, 'cargos')
                    id_cargo_alterado = int(input("Cargo que deseja alterar (Insira a ID) -> "))
                    update_tabela(Cargo, id_cargo_alterado, ['descricao_cargo', 'salario', 'carga_horaria'])

                elif tipo_modificacao == 4:
                    printar_tabela(Cargo, 'cargos')

            # Modificação de Livros
            elif modificar == 4:
                tipo_modificacao = int(input("[1] Criar Livro \n[2] Deletar Livro\n[3] Atualizar Livros \n[4] Ver Livros \n-> "))

                if tipo_modificacao == 1:
                    criar_objeto(Livro, ['titulo', 'autor', 'isbn', 'data_publicacao', 'estoque', 'valor', 'id_editora'])

                elif tipo_modificacao == 2:
                    id_livro = int(input("ID do livro a ser deletado: "))
                    livro_para_deletar = session.query(Livro).get(id_livro)
                    if livro_para_deletar:
                        session.delete(livro_para_deletar)
                        session.commit()
                        print("Livro deletado com sucesso!")
                    else:
                        print("Livro não encontrado.")

                elif tipo_modificacao == 3:
                    printar_tabela(Livro, 'livros')
                    id_livro_alterado = int(input("Livro que deseja alterar (Insira a ID) -> "))
                    update_tabela(Livro, id_livro_alterado, ['titulo', 'autor', 'isbn', 'data_publicacao', 'estoque', 'valor', 'id_editora'])

                elif tipo_modificacao == 4:
                    printar_tabela(Livro, 'livros')

            # Modificação de Editoras
            elif modificar == 5:
                tipo_modificacao = int(input("[1] Criar Editora \n[2] Deletar Editora \n[3] Atualizar Editora \n[4] Ver Editoras \n-> "))

                if tipo_modificacao == 1:
                    criar_objeto(Editora, ['nome', 'endereco'])

                elif tipo_modificacao == 2:
                    id_editora = int(input("ID da editora a ser deletada: "))
                    editora_para_deletar = session.query(Editora).get(id_editora)
                    if editora_para_deletar:
                        session.delete(editora_para_deletar)
                        session.commit()
                        print("Editora deletada com sucesso!")
                    else:
                        print("Editora não encontrada.")

                elif tipo_modificacao == 3:
                    printar_tabela(Editora, 'editoras')
                    id_editora_alterado = int(input("Editora que deseja alterar (Insira a ID) -> "))
                    update_tabela(Editora, id_editora_alterado, ['nome', 'endereco'])

                elif tipo_modificacao == 4:
                    printar_tabela(Editora, 'editoras')

            elif modificar == 6:
                tipo_modificacao = int(input("[1] Atualizar Venda \n[2] Ver Vendas \n->"))
                if tipo_modificacao == 1:
                    printar_tabela(Venda, 'vendas')
                    id_venda_alterado = int(input("Venda que deseja alterar (Insira a ID) -> "))
                    update_tabela(Venda, id_venda_alterado, ['valor', 'id_usuario', 'id_funcionario', 'id_livro'])

                elif tipo_modificacao == 2:
                    printar_tabela(Venda, 'vendas')

            elif modificar == 7:
                tipo_modificacao = int(input("[1] Atualizar Emprestimo \n[2] Ver Emprestimos \n->"))
                if tipo_modificacao == 1:
                    printar_tabela(Emprestimo, 'emprestimos')
                    id_emprestimo_alterado = int(input("Venda que deseja alterar (Insira a ID) -> "))
                    update_tabela(Emprestimo, id_emprestimo_alterado, ['id_usuario', 'id_funcionario', 'id_livro', 'data_emprestimo', 'data_devolucao'])

                elif tipo_modificacao == 2:
                    printar_tabela(Emprestimo, 'emprestimos')

            encerrar = int(input("[1] Continuar navegando \n[2] Encerrar programa \n-> "))
            if encerrar == 2:
                print("Operação finalizada!")
                break
                