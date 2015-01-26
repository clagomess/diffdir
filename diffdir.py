#!/usr/bin/python
import os
import hashlib

diretorio_esquerda = "/var/www/html/sbmt/"
diretorio_direita = "/var/www/html/allsete_sbmt/"
out_diff = "## Resultado: \n\n"


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
arquivos = []
arquivos_esquerda = get_lista_arquivos(diretorio_esquerda)
arquivos = []
arquivos_direita = get_lista_arquivos(diretorio_direita)

# Pega os maiores tamanho de campo
len_field_esquerda = 0
for filepath in arquivos_esquerda:
    if filepath.__len__() > len_field_esquerda:
        len_field_esquerda = filepath.__len__()

# Compara arquivos
for filepath_esquerda in arquivos_esquerda:
    file_esquerda = filepath_esquerda.replace(diretorio_esquerda, "")
    file_direita_existe = False

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

# Verifica arquivos faltantes
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


fp = open("diff_result.txt", 'w')
fp.write(out_diff)
fp.close()