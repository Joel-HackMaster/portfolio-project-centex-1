# main.py
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# Importa tu clase cliente
from api_net import ApisNetPe
load_dotenv()

API_TOKEN = os.getenv("APIS_NET_PE_TOKEN")
if not API_TOKEN:
    raise ValueError("No se encontró el token en la variable de entorno APIS_NET_PE_TOKEN")

cliente = ApisNetPe(token=API_TOKEN)

app = FastAPI(
    title="API de Consultas Centralizada",
    description="Microservicio que utiliza apis.net.pe para consultas de RUC",
    version="1.0.0", # Versión 1, prueba de API externa
)

@app.get("/v2/sunat/ruc/{ruc}", tags=["SUNAT"])
def obtener_datos_ruc(ruc: str):
    datos_empresa = cliente.get_company(ruc)
    
    if datos_empresa:
        return datos_empresa
    else:
        raise HTTPException(status_code=404, detail=f"No se encontró información para el RUC {ruc} o hubo un error en la consulta.")


@app.get("/v2/reniec/dni/{dni}", tags=["RENIEC"])
def obtener_datos_dni(dni: str):
    datos_persona = cliente.get_person(dni)
    
    if datos_persona:
        return datos_persona
    else:
        raise HTTPException(status_code=404, detail=f"No se encontró información para el DNI {dni} o hubo un error en la consulta.")

@app.get("/v2/sunat/tipo-cambio/hoy", tags=["SUNAT"])
def obtener_tipo_cambio_hoy():
    tipo_cambio = cliente.get_exchange_rate_today()

    if tipo_cambio:
        return tipo_cambio
    else:
        raise HTTPException(status_code=503, detail="No se pudo obtener el tipo de cambio en este momento.")