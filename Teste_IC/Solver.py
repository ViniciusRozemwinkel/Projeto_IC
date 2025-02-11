import os
import subprocess
from flask import url_for, redirect


def alocar_pecas(forno, pecas):
    """
    Função para alocar as peças no forno usando a heurística Bottom-Left.

    :param forno: Dicionário com as dimensões do forno.
    :param pecas: Lista de dicionários com as informações das peças.
    :return: Caminho do PDF com a solução ou mensagem de erro.
    """
    try:
        # Verifica se os dados do forno e das peças são válidos
        if not forno or not pecas:
            return "Dados do forno ou das peças inválidos."

        # Chama a função bottom_left para processar a alocação
        resultado = bottom_left(forno, pecas)

        return resultado

    except Exception as e:
        return f"Erro ao alocar peças: {str(e)}"

    except Exception as e:
        return f"Erro ao alocar peças: {str(e)}"





def bottom_left(forno, pecas, id=None):
    """
    Função para executar a heurística Bottom-Left e gerar a solução em PDF.

    :param forno: Dicionário com as dimensões do forno.
    :param pecas: Lista de dicionários com as informações das peças.
    :param id: ID para nomear o arquivo de saída (opcional).
    :return: Caminho do PDF com a solução ou mensagem de erro.
    """
    basedir = os.path.abspath("app")

    if not id:
        id = 10  # ID padrão para o arquivo de saída

    # Cria o arquivo do forno
    kiln_file = basedir + url_for('static', filename='bottom-left/kiln.txt')
    try:
        with open(kiln_file, 'w') as f:
            f.write(f"{forno['comprimento']} {forno['largura']} {forno['altura']}\n")
            if 'prateleiras' in forno:
                f.write(f"{len(forno['prateleiras'])}\n")
                for altura in forno['prateleiras']:
                    f.write(f"{altura}\n")
    except IOError as e:
        return f"Erro ao criar o arquivo do forno: {str(e)}"

    # Cria o arquivo das peças
    items_file = basedir + url_for('static', filename='bottom-left/items.txt')
    try:
        with open(items_file, 'w') as f:
            f.write(f"{len(pecas)}\n")
            for peca in pecas:
                if peca['type'] == 1:
                    f.write(
                        f"1 {peca['quantity']} {peca['length']} {peca['width']} {peca['height']} {peca['description']}\n")
                elif peca['type'] == 2:
                    f.write(f"2 {peca['quantity']} {peca['side']} {peca['height']} {peca['description']}\n")
                elif peca['type'] == 3:
                    f.write(
                        f"3 {peca['quantity']} {math.ceil(peca['diameter'] / 2)} {peca['height']} {peca['description']}\n")
                elif peca['type'] == 4:
                    f.write(
                        f"1 {peca['quantity']} {peca['length']} {peca['width']} {peca['height']} {peca['description']}\n")
    except IOError as e:
        return f"Erro ao criar o arquivo das peças: {str(e)}"

    # Executa o programa em C
    cmd_run = [basedir + url_for('static', filename='bottom-left/main'), \
               kiln_file, items_file, \
               basedir + "/static/solution/solution_" + str(id) + ".tex"]
    try:
        p_run = subprocess.Popen(cmd_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_run = p_run.wait()
        a_run, b_run = p_run.communicate()

        if p_run.returncode != 0:
            return f"Falha ao executar a heurística Bottom-Left: {b_run.decode('utf-8')}"

        # Gera o PDF
        cmd_pdf = ["pdflatex", "-output-directory=" + basedir + "/static/solution", \
                   basedir + url_for('static', filename='solution/solution_' + str(id) + '.tex')]
        p_pdf = subprocess.Popen(cmd_pdf, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_pdf = p_pdf.wait()
        a_pdf, b_pdf = p_pdf.communicate()

        if p_pdf.returncode != 0:
            return f"Falha ao converter o arquivo .tex para .pdf: {b_pdf.decode('utf-8')}"

        return redirect(url_for('static', filename='solution/solution_' + str(id) + '.pdf'))

    except Exception as e:
        return f"Erro inesperado: {str(e)}"