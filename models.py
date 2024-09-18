from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base

caminhodb = "sqlite:///banco.db"
db = create_engine(caminhodb)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()


class Paciente(Base):
    __tablename__ = "Pacientes"
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    cpf = Column(
        String,
        unique=True,
        nullable=False
    )
    nome = Column(
        String
    )
    data_nascimento = Column(
        Date
    )
    cep = Column(
        String
    )
    estado = Column(
        String
    )
    cidade = Column(
        String
    )
    bairro = Column(
        String
    )
    rua = Column(
        String
    )
    numero_rua = Column(
        String
    )

    def __init__(
            self,
            cpf,
            nome,
            data_nascimento,
            cep,
            estado,
            cidade,
            bairro,
            rua,
            numero_rua):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cep = cep
        self.estado = estado
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero_rua = numero_rua


Base.metadata.create_all(bind=db)
