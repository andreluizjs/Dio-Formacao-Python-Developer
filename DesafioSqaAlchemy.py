import sqlalchemy
from sqlalchemy import Column, create_engine, inspect, select, func
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship

Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'cliente_account'
    # atributos
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    endereco = Column(String)

    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    cliente_id = Column(Integer, ForeignKey('cliente_account.id'), nullable=False)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Address(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num})"

print(Cliente.__tablename__)
print(Conta.__tablename__)

# conexão com o banco de dados

engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

#Investiga a Engine
inspetor_engine = inspect(engine)

print(inspetor_engine.has_table("cliente_account"))

print(inspetor_engine.get_table_names())

print(inspetor_engine.default_schema_name)


with Session(engine) as session:
    andre = Cliente(
        nome='Andre',
        cpf='00011122288',
        endereco='Lugar Nenhum',
        conta=[Conta(num='77755543')]
    )

    jefferson = Cliente(
        nome='Jefferson',
        cpf='00011122288',
        endereco='Lugar Nenhum',
        conta=[Conta(num='77755883')]
    )

    session.add_all([andre, jefferson])

    session.commit()


stmt = select(Cliente).where(Cliente.nome.in_(['Andre','Jefferson']))
for user in session.scalars(stmt):
    print(user)

stmt_conta = select(Conta).where(Conta.cliente_id.in_([2]))
for address in session.scalars(stmt_conta):
    print(address)

stmt_order = select(Cliente).order_by(Cliente.cpf.desc())
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(Cliente.cpf, Conta.num).join_from(Conta, Cliente)
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\n Executando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Cliente)
print("\n Total de instancias em Cliente")
for result in session.scalars(stmt_count):
    print(result)
