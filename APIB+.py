#Bibliotecas
import requests
from bs4 import BeautifulSoup
from configparser import ConfigParser
import datetime
import logging
import urllib.parse

#Diretório dos dados
dirDados = "C:\\Bancamais\\Fastcommerce\\DadosLoja" 

#Objeto time
today_datetime = datetime.datetime.today()
time = today_datetime.strftime('%d/%m/%Y %H:%M:%S')

#Configuração do logger
logger = logging.getLogger('my_logger') #Cria o objeto de log
logger.setLevel(logging.INFO) #Configura o nível de log
handler = logging.FileHandler('C:\\Bancamais\\Fastcommerce\\Log2\\log_file.log') #Cria arquivo handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S') #Define o formato do log
handler.setFormatter(formatter) #Define o formato do log para o handler
logger.addHandler(handler) #Adiciona o handler ao logger

#Funções para tratamento de erros
def tratamento():
    global errodesc
    errodesc = []
    index1 = checkresponse.find("<ErrCod>1</ErrCod>")
    index2 = checkresponse.find("<ErrCod>2</ErrCod>")
    index3 = checkresponse.find("<ErrCod>3</ErrCod>")
    index4 = checkresponse.find("<ErrCod>4</ErrCod>")
    index5 = checkresponse.find("<ErrCod>5</ErrCod>")
    index6 = checkresponse.find("<ErrCod>6</ErrCod>")
    index7 = checkresponse.find("<ErrCod>7</ErrCod>")
    index9 = checkresponse.find("<ErrCod>9</ErrCod>")
    index10 = checkresponse.find("<ErrCod>10</ErrCod>")
    index11 = checkresponse.find("<ErrCod>11</ErrCod>")
    index12 = checkresponse.find("<ErrCod>12</ErrCod>")
    index13 = checkresponse.find("<ErrCod>13</ErrCod>")
    index14 = checkresponse.find("<ErrCod>14</ErrCod>")
    index15 = checkresponse.find("<ErrCod>15</ErrCod>")
    index17 = checkresponse.find("<ErrCod>17</ErrCod>")
    if index1 > 1:
        errodesc = " A loja informada não foi encontrada"
    elif index2 > 1:
        errodesc = "O usuario informado é inválido"
    elif index3 > 1:
        errodesc = "A senha não foi informada"
    elif index4 > 1:
        errodesc = "Erro no login"
    elif index5 > 1:
        errodesc = "Seu endereço IP foi bloqueado pelo servidor do Fastcommerce"
    elif index6 > 1:
        errodesc = "Devido a muitas tentativas o usuario foi suspenso por 3 minutos"
    elif index7 > 1:
        errodesc = "Erro de login, o próximo login inválido suspenderá o usuario por 3 minutos"
    elif index9 > 1:
        errodesc = "Método Report/Utility não encontrado ou acesso negado. O limite de 20 acessos por hora foi atingido"
    elif index10 > 1:
        errodesc = "O accesso à API foi negado"
    elif index11 > 1:
        errodesc = "Erro de no método Report/Utility"
    elif index12 > 1:
        errodesc = "O ID da loja virtual é inválido para este login"
    elif index13 > 1:
        errodesc = "O ID da loja virtual não foi informado"
    elif index14 > 1:
        errodesc = "A loja virtual informada está suspensa"
    elif index15 > 1:
        errodesc = "O periodo de demostração da loja informada foi finalizado"
    elif index17 > 1:
        errodesc = "O acesso foi negado"
def erro(errodesc):
    with open(dirErros,"w+") as e:
        e.write(time)
        e.write("\n")
        e.write(str(errodesc))
        e.close()

#Administração do arquivo .cfg
config_object = ConfigParser()
config_object.read(f"{dirDados}\\StoreData.cfg")
STOREINFO = config_object["STOREINFO"]
StoreName = STOREINFO["StoreName"]
StoreID = STOREINFO["StoreID"]
Username = STOREINFO["Username"]
password = STOREINFO["password"]

DataInicial = STOREINFO["data"] + " 00:00:01"
DataInicialEncoded = urllib.parse.quote(DataInicial)

DataFinal = DataInicial[0:10] + " 23:59:59"
DataFinalEncoded = urllib.parse.quote(DataFinal)

#Troca simbolos para poder colocar a data no título do XML
DI = DataInicial.replace("/","-")

#Diretório do XML e do arquivo de erro
dirXML = f"C:\\Bancamais\\Fastcommerce\\XML\\FC[{DI[0:10]}].txt"
dirErros = f"C:\\Bancamais\\Fastcommerce\\Erros2\\ERRO[{DI[0:10]}].txt" 

#Bloco que manda a request com os parâmetros formatados
url = "https://www.rumo.com.br/sistema/adm/APILogon.asp"
payload= (f"""StoreName={StoreName}&StoreID={StoreID}&Username={Username}
            &method=ReportView&password={password}&ObjectID=427&Fields=IDProduto, Qtd&Par2={DataInicialEncoded}&Par3={DataFinalEncoded}""")
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
try:
    response = requests.request("POST", url, headers=headers, data=payload)
except:
    with open(dirErros,"w+") as e:
        e.write(time)
        e.write("\n")
        e.write("ERRO de CONEXÃO ou de CERTIFICADO SSL. Se asegure de que seu PC está conectado à internet e que a data não esteja muito adiantada.")
        e.close()
        logger.error(f"Houve um erro na request")
        exit()

#Tratamento de erro
checkresponse = response.text
tratamento()
if errodesc == []:
    pass
else:
    erro(errodesc)
    logger.error(f"Houve um erro na request")
    exit()

#Formatação da resposta do servidor 
soup = BeautifulSoup(response.text, "xml")
report_tag = soup.find('Report')
attrs_copy = dict(report_tag.attrs)

for attribute in attrs_copy:
    del report_tag[attribute]

xml_string = str(report_tag)

#Cria o arquivo XML no diretorio atribuído
with open(dirXML,"w+") as r:
    r.write(xml_string)
    r.close()

logger.info(f"Request enviada com sucesso, o XML foi recebido")