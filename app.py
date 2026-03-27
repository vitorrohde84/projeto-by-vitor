import streamlit as st
from openai import OpenAI

# Configuração da chave
client = OpenAI(api_key=st.secrets["general"]["api_key"])

# Configuração da página
st.set_page_config(page_title="Carai", page_icon="🚗")

st.title("🚗 Carai: Meu Carro Quebrou!")
st.markdown("Selecione os sintomas do seu veículo e descubra o que pode estar acontecendo.")

# --- INTERFACE ---
with st.sidebar:
    st.header("Dados do Veículo")

    tipo_veiculo = st.selectbox(
        "Tipo de veículo:",
        ["Carro de passeio", "Caminhonete", "Moto", "Caminhão", "Van"]
    )

    combustivel = st.selectbox(
        "Combustível:",
        ["Gasolina", "Álcool (Etanol)", "Flex", "Diesel", "Elétrico", "Híbrido"]
    )

    st.markdown("---")
    st.header("Sintomas")

    sintomas_visuais = st.multiselect(
        "🔴 Luzes acesas no painel:",
        ["Check Engine", "Bateria", "Temperatura do motor", "Pressão do óleo",
         "ABS", "Airbag", "Combustível baixo", "Direção hidráulica"]
    )

    sintomas_barulho = st.multiselect(
        "🔊 Barulhos:",
        ["Batida no motor", "Rangido ao frear", "Barulho ao virar o volante",
         "Chiado ao acelerar", "Tranco ao trocar marcha", "Barulho no escapamento"]
    )

    sintomas_comportamento = st.multiselect(
        "⚠️ Comportamento estranho:",
        ["Não liga", "Liga mas apaga", "Superaquecendo", "Perdendo potência",
         "Consumo de combustível alto", "Fumaça pelo escapamento",
         "Vazamento de líquido", "Vibração ao freiar", "Puxando para um lado"]
    )

    observacao = st.text_area(
        "Observação adicional (opcional):",
        placeholder="Ex: O barulho começa após 10 minutos rodando..."
    )

    botao_diagnosticar = st.button("🔍 Diagnosticar")


# --- LÓGICA DE PROCESSAMENTO ---
if botao_diagnosticar:

    todos_sintomas = sintomas_visuais + sintomas_barulho + sintomas_comportamento

    if not todos_sintomas:
        st.warning("Por favor, selecione ao menos um sintoma!")

    else:

        with st.spinner("Analisando os sintomas do veículo..."):

            sintomas_texto = ", ".join(todos_sintomas)
            obs_texto = f"\nObservação do motorista: {observacao}" if observacao else ""

            prompt = f"""
            Você é um mecânico especialista com mais de 20 anos de experiência.

            Um(a) motorista tem um {tipo_veiculo} movido a {combustivel} e está relatando os seguintes sintomas:
            {sintomas_texto}.{obs_texto}

            Com base nesses sintomas, forneça:

            1. **Diagnóstico provável** — Qual é o problema mais provável?
            2. **Nível de urgência** — Pode continuar dirigindo? (Seguro / Atenção / Pare imediatamente)
            3. **O que pode ter causado** — Explique de forma simples o motivo.
            4. **O que fazer agora** — Orientações práticas imediatas (ligar guincho, ir ao mecânico, verificar algo etc.).
            5. **Peças ou sistemas envolvidos** — Quais componentes provavelmente precisam de verificação ou troca?

            Use linguagem simples e direta, como se estivesse explicando para alguém que não entende de mecânica.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                resultado = response.choices[0].message.content

                st.success("Diagnóstico concluído!")
                st.markdown("---")
                st.write(resultado)

                # --- FEEDBACK ---
                st.markdown("---")
                st.markdown("### O diagnóstico foi útil?")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("👍 Sim, ajudou!"):
                        with open("feedback.csv", "a") as f:
                            f.write(f'"{sintomas_texto}","{tipo_veiculo}","{combustivel}","Útil"\n')
                        st.success("Obrigado pelo feedback positivo!")

                with col2:
                    if st.button("👎 Não ajudou"):
                        with open("feedback.csv", "a") as f:
                            f.write(f'"{sintomas_texto}","{tipo_veiculo}","{combustivel}","Não útil"\n')
                        st.info("Feedback registrado. Vamos melhorar!")

            except Exception as e:
                st.error(f"Erro ao conectar com a IA: {e}")

st.caption("Desenvolvido na disciplina de IHC - Graduação em IA e Ciência de Dados – Universidade Franciscana (UFN)")