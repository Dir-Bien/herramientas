import json
import datetime
from datetime import datetime

def excel_date(date1):
    temp = datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

def criterio():
    return ['cantMes']

def textoGrado(p):
    if "CB" in p["grado"]:
        if "CB Art 11" in p["grado"]:
            return "Cabo Art. 11"
        elif "CB EC" in p["grado"]:
            return "Cabo En Comisión"
        else:
            return "Cabo"
    elif "CI" in p["grado"]:
        if "CI Art 11" in p["grado"]:
            return "Cabo Primero Art. 11"
        else:
            return "Cabo Primero"
    elif "SG" in p["grado"]:
        if "SG Ley 20.508" in p["grado"]:
            return "Sargento Ley 20.508"
        else:
            return "Sargento"
    elif "SI" in p["grado"]:
        if "SI Ley 20.508" in p["grado"]:
            return "Sargento Primero Ley 20.508"
        else:
            return "Sargento Primero"
    elif "SA" in p["grado"]:
        if "SA Ley 20.508" in p["grado"]:
            return "Sargento Ayudante Ley 20.508"
        else:
            return "Sargento Ayudante"
    elif "SP" in p["grado"]:
        if "SP Ley 20.508" in p["grado"]:
            return "Suboficial Principal Ley 20.508"
        else:
            return "Suboficial Principal"
    elif "SM" in p["grado"]:
        if "SM Ley 20.508" in p["grado"]:
            return "Suboficial Mayor Ley 20.508"
        else:
            return "Suboficial Mayor"
    elif "ST" in p["grado"]:
        if "ST Ley 20.508" in p["grado"]:
            return "Subteniente Ley 20.508"
        else:
            return "Subteniente"
    elif "TT" in p["grado"]:
        if "TT Ley 20.508" in p["grado"]:
            return "Teniente Ley 20.508"
        if "TT EC" in p["grado"]:
            return "Teniente En Comisión"
        else:
            return "Teniente"
    elif "TP" in p["grado"]:
        if "TP Ley 20.508" in p["grado"]:
            return "Teniente Primero Ley 20.508"
        else:
            return "Teniente Primero"
    elif "CT" in p["grado"]:
        if "CT Ley 20.508" in p["grado"]:
            return "Capitán Ley 20.508"
        else:
            return "Capitán"
    elif "MY" in p["grado"]:
        if "MY Ley 20.508" in p["grado"]:
            return "Mayor Ley 20.508"
        else:
            return "Mayor"
    elif "TC" in p["grado"]:
        if "TC Ley 20.508" in p["grado"]:
            return "Teniente Coronel Ley 20.508"
        else:
            return "Teniente Coronel"
    elif "CR" in p["grado"]:
        if "CR Ley 20.508" in p["grado"]:
            return "Coronel Ley 20.508"
        else:
            return "Coronel"
    elif "CY" in p["grado"]:
        if "CY Ley 20.508" in p["grado"]:
            return "Coronel Mayor Ley 20.508"
        else:
            return "Coronel Mayor"
    elif "GB" in p["grado"]:
        if "GB Ley 20.508" in p["grado"]:
            return "General de Brigada Ley 20.508"
        else:
            return "General de Brigada"
    elif "GD" in p["grado"]:
        if "GD Ley 20.508" in p["grado"]:
            return "General de División Ley 20.508"
        else:
            return "General de División"
    elif "TG" in p["grado"]:
        if "TG Ley 20.508" in p["grado"]:
            return "Teniente General Ley 20.508"
        else:
            return "Teniente General"
    else:
        return p["grado"]

fall = open("fallecidos.json", encoding="utf-8")
vvg = open("fallecidosVVG.json", encoding="utf-8")
fallecidos = json.load(fall)
veteranos = json.load(vvg)

i = 0
for p in fallecidos:
    p["fechfallec"] = p["fechfallec"][:2] + "/" + p["fechfallec"][2:4] + "/" + p["fechfallec"][4:]
    p["fechaNac"] = p["fnac"][:2] + "/" + p["fnac"][2:4] + "/" + p["fnac"][4:]
    
    fechaObj = datetime.strptime(p["fechfallec"],"%d/%m/%Y")

    p["cantMes"] = "0" # default
    p["cantMes"] = str(int(excel_date(fechaObj)))
    p["ano"] = str(datetime.strftime(fechaObj,"%Y"))
    p["mes"] = str(datetime.strftime(fechaObj,"%m"))
    p["dia"] = str(datetime.strftime(fechaObj,"%d"))
    p["nombreMesFall"] = str(datetime.strftime(fechaObj,"%b"))

    p["apellido"] = p["apynom"].split("*")[0]
    try: 
        p["nombre"] = p["apynom"].split("*")[1]
    except:
        print(p)

    if p["grado"] not in ["Grl Jus","CI EC","CB EC","TT EC","Grl Int","Grl Med","SA Ley 20.508","CI Art 11","CB Art 11","CB","CI","SG","SI","SA","SP","SM","ST","TT","TP","CT","MY","TC","CR","CY","GB","GD","TG", "S/D"] and "Ley" not in p["grado"]:
        # print(p)
        pass
    
    p["nombreGrado"] = textoGrado(p)


    p["img"] = "imgPlaceholder"
    p["fraseMotiv"] = "frasePlaceholder"
    p["descanso"] = "descansoPlaceholder"

    for v in veteranos:
        if v["DNI"] == p["dni"]:
            p["grado"] = p["grado"] + " \"VGM\""
    i += 1

fallecidos.sort(reverse=True,key=lambda e : e["cantMes"])

s = open("salida.json", "w")

salida = json.dumps(fallecidos)
s.write(salida)
s.close()


fall.close()
vvg.close()