from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Paciente, caminhodb
from datetime import date
from pycep import Cep
from validate_docbr import CPF
from math import floor


ano_atual = date.today()
db = create_engine(caminhodb)
Session = sessionmaker(bind=db)
session = Session()


def linha50():
    print("|"+"="*48+"|")


def calcular_idade(data_nascimento):
    idade = ano_atual - data_nascimento
    return (idade.days/365)


def cadastrarPaciente():
    try:
        cpf = input("|Digite o cpf: ").strip()
        validarcpf = CPF()
        if validarcpf.validate(cpf) is False:
            linha50()
            string_erro = "|CPF INVÁLIDO"
            print(string_erro+" "*(49-len(string_erro))+"|")
            linha50()
            start()

        nome = input("|Digite o nome: ").strip()
        dia_nascimento = int(input("|Digite dia de nascimento: "))
        if dia_nascimento < 1 or dia_nascimento > 31:
            linha50()
            print("| DIA TEM QUE SER ENTRE 1 E 31")
            linha50()
            start()

        mes_nascimento = int(input("|Digite mes de nascimento: "))
        if mes_nascimento < 1 or mes_nascimento > 12:
            linha50()
            print("| MÊS TEM QUE SER ENTRE 1 E 12")
            linha50()
            start()

        ano_nascimento = int(input("|Digite ano de nascimento: "))
        if ano_nascimento > ano_atual.year or ano_nascimento < 1850:
            linha50()
            print(f"| O ANO PRECISA SER ENTRE 1850 e {ano_atual.year}")
            linha50()
            start()

        cep = str(input("|Digite o seu CEP: ")).strip()

        endereco_completo = Cep(cep)
        numero_rua = input("|Digite o número da sua rua: ")
        estado = endereco_completo.state
        cidade = endereco_completo.city
        bairro = endereco_completo.district
        rua = endereco_completo.street
        paciente = Paciente(
            cpf=cpf,
            nome=nome.lower(),
            data_nascimento=date(
                day=dia_nascimento,
                month=mes_nascimento,
                year=ano_nascimento
            ),
            cep=cep,
            estado=estado,
            cidade=cidade,
            bairro=bairro,
            rua=rua,
            numero_rua=numero_rua
        )
        session.add(paciente)
        session.commit()
        linha50()
        string_ok = "|PACIENTE CADASTRADO COM SUCESSO!"
        print(string_ok+" "*(49-len(string_ok))+"|")
        linha50()
        start()
    except ValueError:
        linha50()
        string_erro = "|DADO INVÁLIDO"
        print(string_erro+" "*(49-len(string_erro))+"|")
        linha50()
        session.rollback()
        start()
    except Exception:
        linha50()
        string_erro = "|Erro ao cadastrar paciente! DADOS INVÁLIDOS!"
        print(string_erro+" "*(49-len(string_erro))+"|")
        linha50()
        session.rollback()
        start()


def printar_lista(lista_pacientes):
    linha50()
    for i in lista_pacientes:
        string_id = f"|ID: {i.id}"
        print(string_id+" "*(49-len(string_id))+"|")
        string_cpf = f"""|CPF: {i.cpf[0]}{i.cpf[1]}{i.cpf[2]}.
{i.cpf[3]}{i.cpf[4]}{i.cpf[5]}.{i.cpf[6]}{i.cpf[7]}{i.cpf[8]}-
{i.cpf[9]}{i.cpf[10]}""".replace("\n", "")
        print(string_cpf+" "*(49-len(string_cpf))+"|")
        string_nome = f"|NOME: {str(i.nome).title()}"
        print(string_nome+" "*(49-len(string_nome))+"|")
        data = i.data_nascimento.strftime("%d/%m/%Y")
        string_data = f"|DATA NASCIMENTO: {data}"
        print(string_data+" "*(49-len(string_data))+"|")
        idade = calcular_idade(i.data_nascimento)
        string_idade = f"|IDADE: {floor(idade)}"
        print(string_idade+" "*(49-len(string_idade))+"|")
        string_cep = f"""|CEP: {i.cep[0]}{i.cep[1]}{i.cep[2]}{i.cep[3]}
{i.cep[4]}{i.cep[5]}-{i.cep[6]}{i.cep[7]}""".replace("\n", "")
        print(string_cep+" "*(49-len(string_cep))+"|")
        string_estado = f"|ESTADO: {i.estado}"
        print(string_estado+" "*(49-len(string_estado))+"|")
        string_cidade = f"|CIDADE: {i.cidade}"
        print(string_cidade+" "*(49-len(string_cidade))+"|")
        string_bairro = f"|BAIRRO: {i.bairro}"
        print(string_bairro+" "*(49-len(string_bairro))+"|")
        string_rua = f"|RUA: {i.rua}"
        print(string_rua+" "*(49-len(string_rua))+"|")
        string_numero_rua = f"|NÚMERO ENDEREÇO: {i.numero_rua}"
        print(string_numero_rua+" "*(49-len(string_numero_rua))+"|")
        linha50()


def listarPacientes():
    lista_pacientes = session.query(Paciente).all()
    printar_lista(lista_pacientes)
    start()


def pesquisar_cpf():
    cpf = input("|Digite o cpf a ser pesquisado: ")
    lista_pacientes = session.query(Paciente).where(Paciente.cpf == cpf).all()
    if lista_pacientes != []:
        printar_lista(lista_pacientes)
        start()
    else:
        linha50()
        string_erro = "|CPF NÃO CONSTA NO BANCO DE DADOS"
        print(string_erro+" "*(49-len(string_erro))+"|")
        linha50()
        start()


def pesquisar_cep():
    cep = input("|Digite o CEP a ser pesquisado: ").title()
    lista_pacientes = session.query(Paciente).where(
            Paciente.cep == cep).all()
    if lista_pacientes != []:
        linha50()
        string_cep = f"| Exibindo pacientes com o CEP: {cep.title()}"
        print(string_cep+" "*(49-len(string_cep))+"|")
        printar_lista(lista_pacientes)
        string_qt = f"|Total de pacientes encontrados: {len(lista_pacientes)}"
        print(string_qt+" "*(49-len(string_qt))+"|")
        linha50()
        start()
    else:
        linha50()
        string_erro = "|CEP NÃO CONSTA NO BANCO DE DADOS"
        print(string_erro+" "*(49-len(string_erro))+"|")
        linha50()
        start()


def pesquisar_nome():
    nome = input("|Digite o nome a ser pesquisado: ").lower()
    lista_pacientes = session.query(Paciente).where(
            Paciente.nome.like(f"%{nome}%")).all()
    if lista_pacientes != []:
        linha50()
        string_nome = f"|Exibindo pacientes com o NOME: {nome.title()}"
        print(string_nome+" "*(49-len(string_nome))+"|")
        printar_lista(lista_pacientes)
        string_qt = f"|Total de pacientes encontrados: {len(lista_pacientes)}"
        print(string_qt+" "*(49-len(string_qt))+"|")
        linha50()
        start()
    else:
        linha50()
        string_erro = "|NOME NÃO CONSTA NO BANCO DE DADOS"
        print(string_erro+" "*(49-len(string_erro))+"|")
        linha50()
        start()


def pesquisar_estado():
    estado = input("|Digite o ESTADO a ser pesquisado: ").upper()
    linha50()
    lista_pacientes = session.query(Paciente).where(
            Paciente.estado == estado).all()
    if lista_pacientes != []:
        linha50()
        print(f"|Exibindo pacientes com o ESTADO: {estado}             |")
        printar_lista(lista_pacientes)
        string_qt = f"|Total de pacientes encontrados: {len(lista_pacientes)}"
        print(string_qt+" "*(49-len(string_qt))+"|")
        linha50()
        start()
    else:
        linha50()
        string_erro = "|ESTADO NÃO CONSTA NO BANCO DE DADOS"
        print(string_erro+" "*(49-len(string_erro))+"|")
        linha50()
        start()


def pesquisar_cidade():
    cidade = input("|Digite o CIDADE a ser pesquisado: ").title()
    linha50()
    lista_pacientes = session.query(Paciente).where(
            Paciente.cidade == cidade).all()
    if lista_pacientes != []:
        linha50()
        print(f"|Exibindo pacientes com o CIDADE: {cidade}             |")
        printar_lista(lista_pacientes)
        string_qt = f"|Total de pacientes encontrados: {len(lista_pacientes)}"
        print(string_qt+" "*(49-len(string_qt))+"|")
        linha50()
        start()
    else:
        linha50()
        string_erro = "|CIDADE NÃO CONSTA NO BANCO DE DADOS"
        print(string_erro+" "*(49-len(string_erro))+"|")
        linha50()
        start()


def pesquisar_bairro():
    bairro = input("|Digite o BAIRRO a ser pesquisado: ").title()
    linha50()
    lista_pacientes = session.query(Paciente).where(
            Paciente.bairro == bairro).all()
    if lista_pacientes != []:
        linha50()
        string_exb = f"|Exibindo pacientes com o BAIRRO: {bairro}"
        print(string_exb+" "*(49-len(string_exb))+"|")
        printar_lista(lista_pacientes)
        string_qt = f"|Total de pacientes encontrados: {len(lista_pacientes)}"
        print(string_qt+" "*(49-len(string_qt))+"|")
        linha50()
        start()
    else:
        linha50()
        string_erro = "|BAIRRO NÃO CONSTA NO BANCO DE DADOS"
        print(string_erro+" "*(49-len(string_erro))+"|")
        linha50()
        start()


def menu_principal():
    print("|======================|")
    print("|    Menu Principal    |")
    print("|----------------------|")
    print("|[C] Cadastrar Paciente|")
    print("|[L] Listar Pacientes  |")
    print("|[P] Pesquisar         |")
    print("|[S] Sair              |")
    print("|======================|")


def tela_pesquisar():
    print("|======================|")
    print("|     Menu Pesquisa    |")
    print("|----------------------|")
    print("|   [1] CPF            |")
    print("|   [2] NOME           |")
    print("|   [3] CEP            |")
    print("|   [4] ESTADO         |")
    print("|   [5] CIDADE         |")
    print("|   [6] BAIRRO         |")
    print("|   [7] VOLTAR MENU    |")
    print("|   [8] SAIR           |")
    print("|======================|")


def pesquisar_paciente():
    tela_pesquisar()
    opcao = input("|Digite a opção: ")
    if opcao == "1":
        pesquisar_cpf()
    elif opcao == "2":
        pesquisar_nome()
    elif opcao == "3":
        pesquisar_cep()
    elif opcao == "4":
        pesquisar_estado()
    elif opcao == "5":
        pesquisar_cidade()
    elif opcao == "6":
        pesquisar_bairro()
    elif opcao == "7":
        start()
    elif opcao == "8":
        exit()
    else:
        linha50()
        string_erro = "|OPCÃO INVALIDA"
        print(string_erro+" "*(49-len(string_erro))+"|")
        linha50()
        start()


def start():
    menu_principal()
    opcao = input("|Digite a opçao: ").lower()
    if opcao == "c":
        cadastrarPaciente()
    elif opcao == "l":
        listarPacientes()
    elif opcao == "p":
        pesquisar_paciente()
    elif opcao == "s":
        exit()
    else:
        linha50()
        string_erro = "|OPCÃO INVALIDA"
        print(string_erro+" "*(49-len(string_erro))+"|")
        linha50()
        start()


if __name__ == "__main__":
    start()
