#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import hashlib
import sys

diretorio_esquerda = None
diretorio_direita = None
out_diff = "# Resultado: \n"

if sys.argv[1:].__len__() == 2:
    diretorio_esquerda = sys.argv[1:][0]
    diretorio_direita = sys.argv[1:][1]
else:
    print u"Informe os parâmetros de diretório:\n"
    print "> diffdir.py dir_esquerdo dir_direito"
    exit()

if not os.path.isdir(diretorio_esquerda):
    print u"Diretório Esquerdo Inválido"
    exit()

if not os.path.isdir(diretorio_direita):
    print u"Diretório Direito Inválido"
    exit()


# Funcao para varrer diretorio
def get_lista_arquivos(diretorio):
    for item in os.listdir(diretorio):
        if os.path.isfile(diretorio + item):
            arquivos.append(diretorio + item)

        if os.path.isdir(diretorio + item):
            if item not in ['.idea', '.svn', 'CVS', 'cache', '.git', '_doc']:
                get_lista_arquivos(diretorio + item + '/')

    return arquivos


# Funcao row
def get_row(flag, esquerdo, meio, direito):
    row = flag + ' '
    row += esquerdo + ' ' * (len_field_esquerda - esquerdo.__len__())
    row += ' ' + meio + ' '
    row += direito + "\n"
    return row


# Monta List de arquivos
print u"# Varrendo Diretórios:"
print "-> Esquerda"
arquivos = []
arquivos_esquerda = get_lista_arquivos(diretorio_esquerda)
print "-> %s Arquivo(s)" % arquivos_esquerda.__len__()
print "-> Direita"
arquivos = []
arquivos_direita = get_lista_arquivos(diretorio_direita)
print "-> %s Arquivo(s)" % arquivos_direita.__len__()

# Pega os maiores tamanho de campo
len_field_esquerda = 0
for filepath in arquivos_esquerda:
    if filepath.__len__() > len_field_esquerda:
        len_field_esquerda = filepath.__len__()

# Compara arquivos
print u"\n\n# Iniciando Comparação: "
print u"-> ~%s Comparações" % arquivos_esquerda.__len__()
idx = 1
for filepath_esquerda in arquivos_esquerda:
    file_esquerda = filepath_esquerda.replace(diretorio_esquerda, "")
    file_direita_existe = False

    print u"-> %s de %s -- %s" % (idx, arquivos_esquerda.__len__(), file_esquerda)

    for filepath_direita in arquivos_direita:
        file_direita = filepath_direita.replace(diretorio_direita, "")

        if file_esquerda == file_direita:
            file_direita_existe = True
            fp_esquerda = open(filepath_esquerda)
            fp_direita = open(filepath_direita)

            if hashlib.md5(fp_esquerda.read()).digest() != hashlib.md5(fp_direita.read()).digest():
                out_diff += get_row('!', filepath_esquerda, '<-->', filepath_direita)

            fp_esquerda.close()
            fp_direita.close()

            break

    if not file_direita_existe:
        out_diff += get_row('-', filepath_esquerda, ' -->', '?')

    idx += 1

# Verifica arquivos faltantes
print u"\n\n# Verificando arquivos novos: "
for filepath_direita in arquivos_direita:
    file_direita = filepath_direita.replace(diretorio_direita, "")
    file_esquerda_existe = False

    for filepath_esquerda in arquivos_esquerda:
        file_esquerda = filepath_esquerda.replace(diretorio_esquerda, "")
        if file_esquerda == file_direita:
            file_esquerda_existe = True
            break

    if not file_esquerda_existe:
        out_diff += get_row('-', '?', '<-- ', filepath_direita)
        print u"-> %s" % file_direita


fp = open("diff_result.txt", 'w')
fp.write(out_diff)
fp.close()

print u"\n\n# Comparação Finalizada:"
print "-> Ver Resultado em diff_result.txt"