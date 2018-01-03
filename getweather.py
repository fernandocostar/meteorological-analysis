import os
import schedule
import time
import datetime as dt
import metarformat as mf

def coleta(t):
    diretorio_saida = ""

    data = (dt.date.today() - dt.timedelta(1)).isoformat()
    wget_inicio = data[:4] + data[5:7] + data[8:] + "00"
    wget_fim = data[:4] + data[5:7] + data[8:] + "23"
    print("\nColetando em:", data)

    os.system(
        "wget --user-agent=\"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\" --base=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --referer=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --post-data=\"&local=sbrj&msg=metar&data_ini=" + wget_inicio + "&data_fim=" + wget_fim + "\" -O resultado.txt http://www.redemet.aer.mil.br/api/consulta_automatica/index.php")

    arq_in = open("resultado.txt", 'r')
    for i in range(24):
        arq_out = open(diretorio_saida + wget_inicio[:len(wget_inicio) - 1] + str(i) + ".txt", 'w')
        linha = arq_in.readline()
        if "SPECI" in linha:
            linha = arq_in.readline()
        arq_out.write(linha)

    return

schedule.every().day.at("20:00").do(coleta,'20:00')

while True:
    print(".", end="")
    schedule.run_pending()
    time.sleep(60)