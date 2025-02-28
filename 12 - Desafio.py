#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime as dt
from datetime import timezone, timedelta


# In[ ]:


def menu():
    menu = '''

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    
    => '''
    return input(menu).lower()

def data():
    return dt.datetime.now(timezone(timedelta(hours=-3)))
    
def data_format_complete(data):
    return data.strftime("%d/%m/%Y %H:%M:%S")

def data_format_simple(data):
    return data.strftime("%d/%m/%Y")    

def transactions_number(transactions, data, limit):
    return transactions.count(data) < limit

def transactions_daily(transactions, data):
    return transactions.count(data) 

DAILY_LIMIT = 500
TRANSACTIONS_LIMIT = 10

balance = float(0)
statement = ""
transactions = []

while True:
    option = menu()
    current_date = data_format_simple(data())
    
    if option == 'd':
        if(transactions_number(transactions, data_format_simple(data()), TRANSACTIONS_LIMIT)):
            try:
                valor_deposito = float(input('Digite o valor que deseja depositar:'))
                if (valor_deposito <= 0):
                    print("Valor Inválido, tente novamente.")
                else:
                    balance += float(valor_deposito)
                    transactions.append(current_date)
                    print(f"Depósito de R${valor_deposito:.2f} realizado com sucesso.")
                    statement += f'Depóstido de {valor_deposito} realizado em {data_format_complete(data())}\n'
            except ValueError:
                print("Erro: Você deve inserir um valor numérico válido para o depósito.")
        else:
            print("Limite de Operações Excedido. Confira seu extrato")
    elif option == 's':
        if(transactions_number(transactions, data_format_simple(data()), TRANSACTIONS_LIMIT)):
            try:
                valor_saque = float(input('Digite o valor que deseja sacar:'))
                if (valor_saque <= 0):
                    print("Valor Inválido, tente novamente.")
                elif (valor_saque <= DAILY_LIMIT and balance >= valor_saque) :
                    transactions.append(current_date)
                    balance -= float(valor_saque)
                    print(f'Saque de {valor_saque} realizado com sucesso.')
                    statement += f'Saque de {valor_saque} realizado em {data_format_complete(data())}\n'
                elif valor_saque > balance:
                    print('Saldo insuficiente.')
                else:
                    print("Operação Inválida, confira seu extrato.")
            except ValueError:
                print("Erro: Você deve inserir um valor numérico válido para o depósito.")
        else:
            print("Limite de Operações Excedido. Confira seu extrato")
    elif option == 'e':
        print("\n=============== EXTRATO =================")
        print('Não foram realizadas movimentações' if not statement else statement)
        print(f'Saldo: R${balance:.2f}')
        print(f'Seu limite diário de saque é de: R${DAILY_LIMIT:.2f}')
        print(f'Você já realizou {transactions_daily(transactions, data_format_simple(data()))} transações hoje.')
        #if len(extrato) > 0:
            #print('\n' + extrato)
        print("==========================================")
    elif option == 'q':
        break
    else:
        print("Operação inválida. Selecione um menu.")

