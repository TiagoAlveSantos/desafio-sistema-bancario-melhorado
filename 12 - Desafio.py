#!/usr/bin/env python
# coding: utf-8

# In[10]:


import datetime as dt
from datetime import timezone, timedelta, datetime
import os
import platform
import sys
import re


# In[22]:


def menu():
    menu = '''

    [d] Depositar  
    [s] Sacar      
    [e] Extrato
    [u] Cadastrar Usuário
    [uv] Validar Usuário
    [c] Cadastrar Conta 
    [cv] Validar Conta
    [q] Sair       
    
    => '''
    return input(menu).lower()

def clear_terminal():
    """Limpa o terminal, independentemente do sistema operacional ou se está no Jupyter Notebook."""
    try:
        # Verifica se está rodando no Jupyter Notebook
        if 'ipykernel' in sys.modules:
            from IPython.display import clear_output
            clear_output(wait=True)
        else:
            os.system('cls' if platform.system() == 'Windows' else 'clear')
    except Exception as e:
        print(f"Erro ao limpar o terminal: {e}")

def current_datetime():  
    return dt.datetime.now(timezone(timedelta(hours=-3)))
    
def format_complete_date(date):  
    return date.strftime("%d/%m/%Y %H:%M:%S")

def format_simple_date(date):  
    return date.strftime("%d/%m/%Y")    

def transactions_number(transactions, date, limit): 
    return transactions.count(date) < limit

def transactions_daily(transactions, date):
    return transactions.count(date) 

def sanitize_cpf(cpf):
    return re.sub(r'\D', '', cpf)  # Remove tudo que não for número

def validate_date(date_str):
    pattern = r'^\d{2}/\d{2}/\d{4}$'  # Formato DD/MM/AAAA
    if not re.match(pattern, date_str):
        return False  # Rejeita se não estiver no formato correto
    
    try:
        datetime.strptime(date_str, "%d/%m/%Y")  # Verifica se a data realmente existe
        return True
    except ValueError:
        return False  # Se a data for inválida (ex: 31/02/2024), retorna falso

def withdraw(*, balance, statement, current_date):
    if(transactions_number(transactions, format_simple_date(current_datetime()), TRANSACTIONS_LIMIT)):
        try:
            withdraw_value = float(input('Digite o valor que deseja sacar:'))  # valor_saque -> withdraw_value
            clear_terminal()
            if (withdraw_value <= 0):
                print("Valor Inválido, tente novamente.")
            elif (withdraw_value <= DAILY_LIMIT and balance >= withdraw_value):
                transactions.append(current_date)
                balance -= float(withdraw_value)
                print(f'Saque de {withdraw_value} realizado com sucesso.')
                return withdraw_value, balance
            elif withdraw_value > balance:
                print('Saldo insuficiente.')
            else:
                print("Operação Inválida, confira seu extrato.")
        except ValueError:
            print("Erro: Você deve inserir um valor numérico válido para o saque.")
            return None, balance
    else:
        print("Limite de Operações Excedido. Confira seu extrato")
        return None, balance
        
def deposit (balance, current_date, /):
    if(transactions_number(transactions, format_simple_date(current_datetime()), TRANSACTIONS_LIMIT)):
        try:
            deposit_value = float(input('Digite o valor que deseja depositar:')) 
            clear_terminal()
            if (deposit_value <= 0):
                print("Valor Inválido, tente novamente.")
            else:
                balance += float(deposit_value)
                transactions.append(current_date)
                print(f"Depósito de R${deposit_value:.2f} realizado com sucesso.")
                return deposit_value, balance
        except ValueError:
            print("Erro: Você deve inserir um valor numérico válido para o depósito.")
            return None, balance
    else:
        print("Limite de Operações Excedido. Confira seu extrato")
        return None, balance

def register_user (user_id, user_registry):
    cpf = input('Digite seu CPF (apenas numeros): ')
    cpf = sanitize_cpf(cpf)
    
    while len(cpf) != 11:
        print('CPF Inválido: Precisa conter 11 digitos.')
        cpf = input('Digite seu CPF (apenas numeros): ')
        cpf = sanitize_cpf(cpf)
        
    if any(user['CPF'] == cpf for user in user_registry.values()):
        print('CPF já cadastrado.')
        return None
   
    name = input('Digite seu nome: ').strip().upper()
    date_of_birth = input('Informe sua data de nascimento (DD/MM/AAAA): ').strip()
    while not validate_date(date_of_birth):
        clear_terminal()
        print('Data Inválida!')
        date_of_birth = input('Informe corretamente sua data de nascimento (DD/MM/AAAA): ').strip()
    address = input('Informe seu endereço: ').strip().upper()
    
    user_registry[user_id] = {
        'CPF': cpf,
        'name': name,
        'date_of_birth': date_of_birth,
        'address': address
    }
    
    print('Usuário cadastrado com sucesso!')
    print(f'ID de Usuário: {user_id}')
    return user_registry

def create_account (account_number, user_registry, account_registry):
    user_id = int(input("Informe seu numero de usuário: "))
    if user_id in user_registry:
        account_registry[account_number] = {
            "agency_number": AGENCY_NUMBER,
            "user_id": user_id
        }
        print('Conta cadastrada com sucesso')
        print(f'Agencia: {AGENCY_NUMBER}')
        print(f'ID do Usuário: {user_id}')
        print(f'Numero da conta: {account_number}')
        return account_registry
    else:
        print('Usuário não localizado.')
        return None

def account_statement (balance, /, *, statement):
    print("\n=============== EXTRATO =================")
    print('Não foram realizadas movimentações' if not statement else statement)
    print(f'Saldo: R${balance:.2f}')
    print(f'Seu limite diário de saque é de: R${DAILY_LIMIT:.2f}')
    print(f'Você já realizou {transactions_daily(transactions, format_simple_date(current_datetime()))} transações hoje.')
    print("==========================================")

def check_user(user_registry):
    cpf = input('Digite seu CPF (apenas numeros): ')
    cpf = sanitize_cpf(cpf)
    
    while len(cpf) != 11:
        print('CPF Inválido: Precisa conter 11 digitos.')
        cpf = input('Digite seu CPF (apenas numeros): ')
        cpf = sanitize_cpf(cpf)

    user_found = None
    for user_id, user in user_registry.items():
        if user['CPF'] == cpf:
            user_found = user
            print(f"Cadastro encontrado para o CPF {cpf}:")
            print(f"ID do Usuário: {user_id}")
            print(f"Nome: {user['name']}")
            print(f"Data de Nascimento: {user['date_of_birth']}")
            print(f"Endereço: {user['address']}")
    
    # Se nenhum usuário for encontrado, exibe uma mensagem
    if user_found is None:
        print(f"Nenhum usuário encontrado com o CPF {cpf}.")
        
def check_account(account_registry):
    user_id = int(input("Informe seu numero de usuário: "))
    for account_number, user in account_registry.items():
        if user['user_id'] == user_id:
            print(f'Agencia: {user["agency_number"]}')
            print(f'ID do Usuário: {user["user_id"]}')
            print(f'Numero da conta: {account_number}', end='\n\n')


DAILY_LIMIT = 500
TRANSACTIONS_LIMIT = 10
AGENCY_NUMBER = '0001'

user_id = 1
account_number = 1
user_registry = {}
account_registry = {}
balance = float(0)  # saldo -> balance
statement = ""  # extrato -> statement
transactions = []  

while True:
    clear_terminal()
    option = menu()
    current_date = format_simple_date(current_datetime()) 
    
    if option == 'd':
        clear_terminal()
        deposit_value, balance = deposit(balance, current_date)
        if deposit_value is not None:
            statement += f'Depósito de {deposit_value} realizado em {format_complete_date(current_datetime())}\n'
        
    elif option == 's':
        clear_terminal()
        withdraw_value, balance = withdraw(balance=balance, statement=statement, current_date=current_date)
        if withdraw_value is not None:
            statement += f'Saque de {withdraw_value} realizado em {format_complete_date(current_datetime())}\n'
        
    elif option == 'e':
        clear_terminal()
        account_statement(balance, statement=statement)

    elif option == 'u':
        clear_terminal()
        new_registry = register_user(user_id, user_registry)
        if new_registry is not None:
            user_registry = new_registry
            user_id += 1
            
    elif option == 'c':
        clear_terminal()
        new_account = create_account(account_number, user_registry, account_registry)
        if new_account is not None:
            account_registry = new_account
            account_number += 1

    elif option == 'uv':
        clear_terminal()
        check_user(user_registry)
        
    elif option == 'cv':
        clear_terminal()
        check_account(account_registry)
    
    elif option == 'q':
        clear_terminal()
        break
    else:
        print("Operação inválida. Selecione um menu.")

