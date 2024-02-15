#pip install openai streamlit
#python -m pip install scipy



#import streamlit as st
#import ast
#import pandas as pd
#import requests
#import nltk
#from wordcloud import WordCloud
#import matplotlib.pyplot as plt
#from fpdf import FPDF
#mport json
#from nltk.corpus import stopwords
#import base64
#from PIL import Image
#import datetime
#from openai import OpenAI
#from scipy import spatial

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def calculate_cosine_distance(emb1, emb2):
    return spatial.distance.cosine(emb1, emb2)

def create_context(question, df):
    q_embedding = get_embedding(question)
    df['distance'] = df['embedding'].apply(lambda emb: calculate_cosine_distance(q_embedding, emb))
    sorted_df = df.sort_values('distance')
    relevant_tramites = sorted_df['Trámite'].unique()[:3]
    return relevant_tramites

def build_context_for_selected_tramite(df, tramite_elegido, max_len=1800, pregunta=None):
    if pregunta:
        df_filtrado = df[(df['Trámite'] == tramite_elegido) & (df['Pregunta_Completa'] == pregunta)]
    else:
        df_filtrado = df[df['Trámite'] == tramite_elegido]
    context = ""
    total_len = 0
    for _, row in df_filtrado.iterrows():
        text_len = len(row['Combined'].split())
        if total_len + text_len > max_len:
            break
        context += row['Combined'] + "\n\n"
        total_len += text_len
    return context

def answer_questions(questions, context="", model="gpt-3.5-turbo", max_tokens=300):
    responses = []
    for question in questions:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Eres un especialista en temas fiscales en México. Vas a responder consultas sobre los trámites del anexo 1-A de la Resolución Miscelánea Fiscal 2023 de México responde de forma amable, si la respuesta consiste en múltiples pasos o documentos responde enlistando la información."},
                    {"role": "user", "content": f"Context: {context}\n\n---\n\nQuestion: {question}\nAnswer:"}
                ],
                temperature=0.5,
                max_tokens=max_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            text_response = response.choices[0].message.content
            responses.append(text_response.strip())
        except Exception as e:
            print(e)
            responses.append("")
    return responses

def main():
    st.title("Asistente para Trámites Fiscales")

    df = pd.read_csv("./data/tramitespreguntasEMBVFfundamento.csv")

    df2 = pd.read_csv("./data/tramitespreguntasEMBVFfundamentoVF.csv")
    df['Pregunta_Completa'] = df2['Pregunta_Completa']
    df['Fundamento jurídico'] = df2['Fundamento jurídico']

    df['embedding'] = df['embedding'].astype(str).apply(ast.literal_eval)
    #df['embedding'] = df['embedding'].astype(str).apply(eval)
    #df['embedding'] = df['embedding'].apply(lambda emb: json.loads(emb) if isinstance(emb, str) else emb)

    busqueda_opcion = st.radio("¿Cómo deseas buscar?", ('Por Fundamento Jurídico', 'Describir Trámite o Pregunta'))

    if busqueda_opcion == 'Por Fundamento Jurídico':
        fundamentos_legales = df['Fundamento jurídico'].dropna().unique()
        fundamento_seleccionado = st.selectbox("Selecciona el fundamento legal de tu interés:", [''] + list(fundamentos_legales))

        if fundamento_seleccionado:
            tramites_asociados = df[df['Fundamento jurídico'] == fundamento_seleccionado]['Trámite'].unique()
            tramite_seleccionado = st.selectbox("Selecciona el trámite asociado:", [''] + list(tramites_asociados))

    else:
        question = st.text_input("Ingresa tu pregunta o describe el trámite que te interesa:")
        if question:
            relevant_tramites = create_context(question, df)
            tramite_elegido = st.selectbox("Trámites sugeridos basados en tu descripción:", relevant_tramites)

    if 'tramite_seleccionado' in locals() or 'tramite_elegido' in locals():
        selected_tramite = tramite_seleccionado if 'tramite_seleccionado' in locals() else tramite_elegido
        preguntas_df = df[df['Trámite'] == selected_tramite]
        preguntas = preguntas_df['Pregunta_Completa'].dropna().unique()
        pregunta_seleccionada = st.selectbox("Selecciona una pregunta de tu interés o escribe una nueva abajo:", [''] + list(preguntas))
        
        nueva_pregunta = st.text_input("O ingresa tu nueva pregunta aquí:")
        
        if st.button("Obtener Respuesta"):
            pregunta_final = nueva_pregunta if nueva_pregunta else pregunta_seleccionada
            if pregunta_final:
                context = build_context_for_selected_tramite(df, selected_tramite, pregunta=pregunta_final)
                response = answer_questions([pregunta_final], context=context)[0]
                st.text_area("Respuesta:", value=response, height=150)

if __name__ == "__main__":
    main()



#App
#def main():
#    st.set_page_config(page_title="Chat de Trámites Fiscales", page_icon="📎")
#    st.sidebar.header("Asistente de  IA para Trámites Fiscales")
#    st.title("IA Trámites Fiscales")
#    st.header(':blue[Asistente de  IA para Trámites Fiscales]', divider='blue')
#   st.subheader(':grey[Nuestro asistente automatizado responde tus preguntas sobre trámites fiscales]', divider='blue')

#if "openai_model" not in st.session_state:
#    st.session_state["openai_model"] = "gpt-3.5-turbo"

#if "messages" not in st.session_state:
#    st.session_state.messages = []
#st.write(df)

#for message in st.session_state.messages:
#    with st.chat_message(message["role"]):
#        st.markdown(message["content"])

#if prompt := st.chat_input("What is up?"):
#    st.session_state.messages.append({"role": "user", "content": prompt})
#    with st.chat_message("user"):
#        st.markdown(prompt)

#    with st.chat_message("assistant"):
#        stream = client.chat.completions.create(
#            model=st.session_state["openai_model"],
 #           messages=[
 #               {"role": m["role"], "content": m["content"]}
 #               for m in st.session_state.messages
#            ],
 #           stream=True,
 #       )
#        response = st.write_stream(stream)
 #   st.session_state.messages.append({"role": "assistant", "content": response})
