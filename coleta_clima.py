import os
import schedule
import datetime as dt
import glob
import time
from metar import Metar


def write_to_file(filename, data):
    from json import dump
    with open(filename, 'w') as fp:
        dump(data, fp)


def coleta(t):
    ultimo_arq = open("ultimo.txt", 'r').read()
    try:
        open(ultimo_arq, "r")
        arquivo_foto = glob.glob('/home/fernando/Documentos/UFF/ic-leandro/'+ultimo_arq)[0]
        hora = time.strftime('%Y%m%d%H', time.localtime(os.path.getctime(arquivo_foto)))
        os.system(
            "wget --user-agent=\"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\" --base=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --referer=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --post-data=\"&local=sbrj&msg=metar&data_ini=" + hora + "&data_fim=" + hora + "\" -O resultado.txt http://www.redemet.aer.mil.br/api/consulta_automatica/index.php")
        d = {}
        linha = open("resultado.txt", 'r').readline()
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

        write_to_file(ultimo_arq[:-4]+".json", d)
        numeracao = str(int(ultimo_arq[4:-4])+1)
        numeracao = "DSC_" + "".join(["0"]*(9-len(numeracao))) + numeracao + ".jpg"
        open("ultimo.txt", "w").write(numeracao)
        return 1
    except IOError:
        return 0


def executa(t):
    while True:
        if not coleta(t):
            break
    return

schedule.every().day.at("17:30").do(executa,'17:30')

while True:
    print(".", end="")
    schedule.run_pending()
    time.sleep(10)