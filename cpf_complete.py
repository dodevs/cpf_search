import cfscrape

try: import requests
except ImportError: print(" [-] \"requests\" é necessário!")

try: from bs4 import BeautifulSoup
except ImportError: print(" [-] \"BeautifulSoup\" é necessário!")

import random
import re


def cpfSearch(cpf, muni):
    scraper = cfscrape.create_scraper()
    req = scraper.get('http://tudosobretodos.se/%s' % cpf)
    soup = BeautifulSoup(req.content, 'html.parser')
    for i in soup.findAll('span', attrs={'class': 'textoTituloDetalhesPessoa'}):
        if i.text == cpf:
            return -1
    details = soup.findAll('div', attrs={'class': 'innerDetalheDir'})
    municipio = details[4].text.replace("\n", "").replace("\t", "")
    #estado = details[5].text.replace("\n", "").replace("\t", "")
    if (municipio == muni):
        return cpf
    else:
        print(cpf, municipio)
        return -1

def gera_cpf(cpfMask):

    def calcula_digito(digs):
       s = 0
       qtd = len(digs)
       for i in range(qtd):
          s += n[i] * (1+qtd-i)
       res = 11 - s % 11
       if res >= 10: return 0
       return res 

    if(cpfMask[0] == '*'):
        n = [random.randrange(2)]
    else:
        n = [cpfMask[0]]
    for dig in cpfMask[1:]:
        if dig == "*":
            r = random.randrange(10)
            n.append(r)
        else:
            n.append(dig)

    n.append(calcula_digito(n))
    n.append(calcula_digito(n))
    return n

def valdiCpf(cpfMask):
    cpfMask = [int(dig) if dig != "*" else dig for dig in cpfMask]
    cpf_retornado = gera_cpf(cpfMask[:9])
    while(cpf_retornado[9:11] != cpfMask[9:11]):
        cpf_retornado = gera_cpf(cpfMask[:9])

    return "%d%d%d%d%d%d%d%d%d%d%d" % tuple(cpf_retornado)

def main(args):
    lista_cpfs = open('possiveis_cpfs.txt', 'wt')
    cpfs_verificados = []

    cpf_mask = args[1]
    municipio = args[2]
    #cpf_mask = "*****590739"

    while(True):
        cpf_valido = valdiCpf(cpf_mask)
        if(cpf_valido not in cpfs_verificados):
            resultOfSearch = cpfSearch(cpf_valido, municipio)
            if(resultOfSearch != -1):
                lista_cpfs.write(resultOfSearch+'\n')
                lista_cpfs.flush()
            cpfs_verificados.append(cpf_valido)

if __name__ == "__main__":
    from sys import argv
    main(argv)