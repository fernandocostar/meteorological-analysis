import os
import schedule
import time
import datetime as dt
from metar import Metar


def write_to_file(filename, data):
    from json import dump
    with open(filename, 'w') as fp:
        dump(data, fp)


def coleta(t):
    diretorio_saida = ""
    ultimo = int(open("ultimo.txt", 'r').readline())

    data = (dt.date.today() - dt.timedelta(1)).isoformat()
    wget_inicio = data[:4] + data[5:7] + data[8:] + "00"
    wget_fim = data[:4] + data[5:7] + data[8:] + "23"
    print("\nColetando em:", data)

    os.system(
        "wget --user-agent=\"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\" --base=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --referer=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --post-data=\"&local=sbrj&msg=metar&data_ini=" + wget_inicio + "&data_fim=" + wget_fim + "\" -O resultado.txt http://www.redemet.aer.mil.br/api/consulta_automatica/index.php")

    arq_in = open("resultado.txt", 'r')
    for i in range(24):
        d = {}
        linha = arq_in.readline()
        traduzido = Metar.Metar(linha[13:-2])

        vento = traduzido.wind()
        vento_dir = str(traduzido.wind_dir)
        vento_vel = vento.split(" ")[2]

        nuvens = traduzido.sky_conditions()
        visibilidade = traduzido.visibility()
        temperatura = str(traduzido.temp)
        pressao = str(traduzido.press)

        d['vento'] = [vento_dir, vento_vel]
        d['nuvens'] = nuvens
        d['visibilidade'] = visibilidade
        d['temperatura'] = temperatura
        d['pressao'] = pressao

        write_to_file(diretorio_saida+str(ultimo)+".json", d)
        ultimo += 1
    open("ultimo.txt", "w").write(str(ultimo))
    return


schedule.every().day.at("14:52").do(coleta,'14:52')

while True:
    print(".", end="")
    schedule.run_pending()
    time.sleep(60)