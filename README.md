# 🏭 Segurança em IoT: Validação Física de Gêmeos Digitais

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![MicroPython](https://img.shields.io/badge/MicroPython-2B2728?style=for-the-badge&logo=python&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-3C5280?style=for-the-badge&logo=eclipse-mosquitto&logoColor=white)

**Aluna:** Gabriella Mizrach  
**Matrícula:** 202402408097  
---

## 📖 Sobre o Projeto

Este projeto aborda um dos maiores desafios da Indústria 4.0: **a integridade dos dados em sistemas IoT**. 
A arquitetura simula um maquinário industrial ("Gêmeo Digital") e implementa um validador de segurança na borda (*Edge Computing*) focado em detectar ataques de **Envenenamento de Dados** (*Data Poisoning*).

Em vez de depender apenas de criptografia de rede, o sistema utiliza as **Leis da Física** (Conservação de Energia, Termodinâmica e Mecânica dos Fluidos) para cruzar as informações dos sensores. Se os dados não fizerem sentido físico, o alarme soa, impedindo que hackers sabotem a máquina enviando falsas métricas.

### 🛡️ Cenários de Defesa (Threat Model)
O ESP32 monitora as variáveis ambientais e aciona alertas críticos em dois cenários:
1. **Ataque Tipo 1 (Falso Negativo):** O atacante relata que o fluxo parou, mascarando uma sobrecarga. O sistema detecta a mentira pois há alta temperatura ou vibração no cano.
2. **Ataque Tipo 2 (Falso Positivo):** O atacante relata fluxo máximo para causar pânico e desligamento da fábrica. O sistema invalida o dado pois a máquina está fria e não apresenta vibração mecânica.

---

## 🏗️ Arquitetura do Sistema

* **Borda (Edge):** Microcontrolador ESP32 programado em MicroPython.
* **Sensores Virtuais:** 
  * `Potenciômetro` (Simulando Fluxo/Vazão)
  * `DHT22` (Temperatura)
  * `MPU6050` (Vibração/Aceleração Mecânica)
* **Atuadores:** LED de Emergência e Buzzer.
* **Nuvem e Mensageria:** Broker MQTT público (HiveMQ) para tráfego leve e rápido via tópicos JSON.
* **Interface (Front-End):** Aplicação em Python utilizando o framework Streamlit para visualização de KPIs e gráficos em tempo real.

---

## ⚙️ Como testar a aplicação

Para ver a aplicação funcionando de ponta a ponta:

1. Abra a [Simulação no Wokwi](https://wokwi.com/projects/462557263127282689) em uma aba do navegador.
2. Abra o [Dashboard Streamlit](https://validacaodedadosiotcontraataquesdeenvenenamento-3k77jh4ufxvgrr.streamlit.app/) em outra aba e deixe as duas lado a lado.
3. Dê o **"Play"** na simulação do Wokwi.
4. Altere os valores clicando no potenciômetro e nos sensores do Wokwi.
5. Observe os gráficos do Streamlit sendo traçados em tempo real na nuvem e tente causar uma violação física nos sensores para acionar a tela de **Alerta Crítico**!

---
*Projeto desenvolvido para fins acadêmicos - 2026.*
