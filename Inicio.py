import streamlit as st
st.set_page_config(
    page_title="Inicio",
    page_icon="👋",
)
st.write("# Bienvenido a Analítica Boutique DOF! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Nuestra app del DOF te permite consultar todas las publicaciones
    realizadas en el Diario Oficial de la Federación (gaceta oficial
    del Gobierno de México).

    **👈 Selecciona la aplicación de tu interés en el menú de la izquierda**

    - ### 📊 Analítica de Texto
      -Elige la fecha del DOF que quieres consultar

      -Selecciona la Dependencia o institución de tu interés

      -Selecciona las publicaciones que te interesn y  listo!

      -Visualiza analítica de texto de estas publicaciones

    - ### 🔊 Resumenes de Texto y Texto a audio
     -Obten con IA el resumen de las publicaciones seleccionadas

     -Transforma con IA el texto del resumen en audio

    - ### ¿Tienes dudas o comentarios?

    - ### ¿Quieres implementar estas aplicaciones en tu negocio?

     contactanos en bussinesanalitics@analiticaboutique.com
 """
)