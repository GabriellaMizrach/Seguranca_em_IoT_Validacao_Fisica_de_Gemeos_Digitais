import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# ==========================================
# CONFIGURAÇÃO DA PÁGINA E MEMÓRIA
# ==========================================
st.set_page_config(page_title="Gêmeo Digital - Segurança", layout="centered")
st.title("🏭 Gêmeo Digital: Monitoramento e Defesa")
st.write("Acompanhamento em tempo real da integridade física do maquinário.")

MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "projeto_iot/gemeo_digital/telemetria"

@st.cache_resource
def get_memoria_dados():
    return {
        "fluxo": 0.0,
        "temperatura": 0.0,
        "vibracao": 0.0,
        "status": "Aguardando conexão com a Borda (Edge)...",
        "hist_fluxo": [], 
        "hist_temp": []   
    }

dados = get_memoria_dados()

# ==========================================
#  CONEXÃO COM A NUVEM 
# ==========================================
def ao_receber_mensagem(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        novos_dados = json.loads(payload)
        
        
        dados.update(novos_dados)
        
        
        dados["hist_fluxo"].append(novos_dados["fluxo"])
        dados["hist_temp"].append(novos_dados["temperatura"])
        
        
        dados["hist_fluxo"] = dados["hist_fluxo"][-30:]
        dados["hist_temp"] = dados["hist_temp"][-30:]
        
    except Exception as e:
        print("Erro ao decodificar:", e)

@st.cache_resource
def iniciar_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = ao_receber_mensagem
    client.connect(MQTT_BROKER, 1883, 60)
    client.subscribe(MQTT_TOPIC)
    client.loop_start()
    return client

iniciar_mqtt()

# ==========================================
#  DASHBOARD
# ==========================================
col1, col2, col3 = st.columns(3)
col1.metric(label="💧 Fluxo de Fluido", value=f"{dados['fluxo']} %")
col2.metric(label="🌡️ Temperatura", value=f"{dados['temperatura']} °C")
col3.metric(label="⚙️ Vibração", value=f"{dados['vibracao']} G")

st.divider()

st.subheader("📈 Análise de Tendências (Tempo Real)")
if len(dados["hist_fluxo"]) > 1:
    
    st.line_chart({
        "Fluxo (%)": dados["hist_fluxo"], 
        "Temperatura (°C)": dados["hist_temp"]
    })
else:
    st.info("Coletando dados da máquina para gerar o gráfico...")

st.divider()


st.subheader("🛡️ Status do Validador Físico (Edge)")
if "INTEGRO" in dados['status']:
    st.success(f"✅ **{dados['status']}**: As leis da física confirmam as leituras.")
elif "ATAQUE" in dados['status']:
    st.error(f"🚨 **ALERTA CRÍTICO - {dados['status']}**: Inconsistência física detectada! Possível envenenamento de dados do Gêmeo Digital.")
else:
    st.warning(f"⏳ {dados['status']}")


time.sleep(2)
st.rerun()