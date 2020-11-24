import threading
import math
import time

THREADS = 8
contador_CNPJ = 0
contador_CPF = 0

def validate_cpf(cpf):
    v1 = 0
    v2 = 0
    for i in range(0, len(cpf)):
        v1 = v1 + int(cpf[i]) * (9 - (i % 10))
        v2 = v2 + int(cpf[i]) * (9 - ((i + 1) % 10))
    v1 = (v1 % 11) % 10
    v2 = v2 + v1 * 9
    v2 = (v2 % 11) % 10
    return f'{v1}{v2}'


def validate_cnpj(str_cnpj):
    cnpj = [int(d) for d in str_cnpj]
    v1 = 0
    v2 = 0
    v1 = 5*cnpj[0] + 4*cnpj[1]  + 3*cnpj[2]  + 2*cnpj[3]
    v1 += 9*cnpj[4] + 8*cnpj[5]  + 7*cnpj[6]  + 6*cnpj[7]
    v1 += 5*cnpj[8] + 4*cnpj[9] + 3*cnpj[10] + 2*cnpj[11]
    v1 = 11 - v1 % 11
    if v1 >= 10:
        v1 = 0

    v2 = 6*cnpj[0] + 5*cnpj[1]  + 4*cnpj[2]  + 3*cnpj[3]
    v2 += 2*cnpj[4] + 9*cnpj[5]  + 8*cnpj[6]  + 7*cnpj[7]
    v2 += 6*cnpj[8] + 5*cnpj[9] + 4*cnpj[10] + 3*cnpj[11]
    v2= 2*v1
    v2 = 11 - v2 % 11
    if v2 >= 10:
        v2 = 0

    return f'{v1}{v2}'

def comparacao(base):
    global contador_CNPJ 
    global contador_CPF
    for linha in base:
        if len(linha) == 9:
            validate_cpf(linha)
            contador_CPF += 1
        elif len(linha) == 12:
            validate_cnpj(linha)
            contador_CNPJ +=1


if __name__ == "__main__":
    tempo_inicial = time.time()
    threads = []

    with open('BASE.txt', 'r') as fp:
        base = [line.strip() for line in fp.read().splitlines()]

    tamanho = math.floor(len(base)/THREADS)
    
    for i in range(1, THREADS + 1):
        threads.append(threading.Thread(target=comparacao, args=(base[((i-1)*tamanho):(i*tamanho)],), daemon=True))
    
    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()
    
    
    
    print(f'quantidade total de CNPJ =  {contador_CNPJ} ')
    print(f'quantidade total de CPF =  {contador_CPF} ')
    print(f'A soma total e de = {contador_CPF + contador_CNPJ} ')
    print('tempo necessario para a execucao : ' , (time.time()-tempo_inicial)*1000)