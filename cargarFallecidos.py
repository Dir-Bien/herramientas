import requests
import json
import datetime
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


url = "https://bienestar.mil.ar/fallecidos/json/fallecidos.json" 
opt = input("Desea obtener el JSON desde la Web, o leer un JSON de la carpeta actual?\n1.Web\n2.Carpeta actual\n")
if (opt == 1):
  try:
    f = requests.get(url)
    print(f"Archivo JSON obtenido con exito de {url}!")
    fall = json.loads(f.content)
  except:
    print(f"No se pudo obtener el archivo JSON desde la web")
    quit()
else:
  f = open("fallecidos.json", encoding='utf-8')
  fall = json.load(f)

f.close()


# recibir JSON original
def excel_date(date1):
    temp = datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

def main():
  
  print("Elija lo que desea hacer:")
  print("1. Cargar fallecido")
  print("2. Salir")
  try:
    accion = int(input())
    if accion < 1 or accion > 2:
        raise ValueError
  except ValueError:
    print("OPCION INVALIDA. Vuelva a intentar")
  if accion == 1:
    grado = input("Ingrese el grado ABREVIADO por ejemplo: CR\n")
    txgrado = input("Ingrese el grado sin abreviar, ejemplo CORONEL\n")
    arma = input("Ingrese el arma ABREVIADA por ejemplo: ARS\n")
    txarma = input("Ingrese el arma por ejemplo: ARSENALES\n")
    apellido = input("Ingrese el/los Apellido/s (separar con espacios)\n")
    nombre = input("Ingrese el/los Nombre/s separados con espacios\n")
    vgm = input("Es Veterano de Guerra? Ingrese 0 si NO ES, 1 SI ES\n")
    tibaj = input("Ingrese el tipo de baja, R para retirados fallecidos, FALL para muertos en activ.\n")
    fechaFall = input("Ingrese la fecha de fallecimiento en formato 15/06/2023\n")
    fechaNac = input("Ingrese la fecha de nacimiento en formato: 15/06/2023\n")
    
    muerto = {}

    muerto["grado"] = grado
    if (tibaj == 'R'):
      muerto["grado"] += " (R)"
    muerto["nombreGrado"] = txgrado
    muerto["arma"] = arma
    muerto["armaNombre"] = txarma
    muerto["tibaj"] = tibaj
    muerto["apellido"] = apellido
    muerto["nombre"] = nombre

    objFechaFall = datetime.strptime(fechaFall,"%d/%m/%Y")

    muerto["ano"] = str(datetime.strftime(objFechaFall,"%Y"))
    muerto["mesFall"] = str(datetime.strftime(objFechaFall,"%m"))
    muerto["diaFall"] = str(datetime.strftime(objFechaFall,"%d"))
    muerto["nombreMesFall"] = str(datetime.strftime(objFechaFall,"%b"))
    muerto["fechaFall"] = fechaFall
    muerto["fechaNac"] = fechaNac
    muerto["cantMes"] = str(int(excel_date(objFechaFall)))
    
    if vgm == "1":
      muerto["grado"] += " `VGM`" 

    muerto["img"] = f"/fallecidos/img/{muerto['nombreGrado']}.png"
    muerto["trayectoria"] = ""  
    
    fall.append(muerto)
    fall.sort(reverse=True,key=lambda e : e["cantMes"])

    s = open("fallecidos.json", "w")
    salida = json.dumps(fall)
    s.write(salida)
    s.close()
    main()
  else:
    return
main()


