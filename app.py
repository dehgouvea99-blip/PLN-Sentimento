import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="📊",
    layout="centered"
)

def main():
    st.title("📊 Analisador de Sentimentos (Versão Offline)")
    st.markdown(
        "Este aplicativo utiliza bibliotecas tradicionais de Python "
        "(`TextBlob` e `deep-translator`) para realizar a análise de sentimentos "
        "localmente, sem depender de APIs externas de inteligência artificial."
    )
    
    st.markdown("---")
    
    # Área de entrada do usuário
    texto_usuario = st.text_area(
        "Digite seu texto abaixo (pode ser em português ou inglês):",
        placeholder="Ex: Eu adorei este produto, superou todas as minhas expectativas!",
        height=150
    )
    
    # Botão de análise
    if st.button("Analisar Sentimento", type="primary"):
        if not texto_usuario.strip():
            st.warning("Por favor, digite algum texto antes de clicar em analisar.")
            return
        
        with st.spinner("Processando análise de sentimentos..."):
            try:
                # Tradução invisível para o inglês (caso o texto venha em outro idioma)
                # O deep-translator lida muito bem com detecção e tradução
                tradutor = GoogleTranslator(source='auto', target='en')
                texto_traduzido = tradutor.translate(texto_usuario)
                
                # Análise de sentimentos com TextBlob
                blob = TextBlob(texto_traduzido)
                polaridade = blob.sentiment.polarity
                subjetividade = blob.sentiment.subjectivity
                
                # Classificação baseada na polaridade (-1.0 a 1.0)
                if polaridade > 0.05:
                    sentimento = "Positivo"
                    cor_status = "success"
                elif polaridade < -0.05:
                    sentimento = "Negativo"
                    cor_status = "error"
                else:
                    sentimento = "Neutro"
                    cor_status = "warning"
                
                # Exibição dos resultados visuais
                st.markdown("### Resultados da Análise")
                
                if cor_status == "success":
                    st.success(f"**Sentimento Detectado:** {sentimento}")
                elif cor_status == "error":
                    st.error(f"**Sentimento Detectado:** {sentimento}")
                else:
                    st.warning(f"**Sentimento Detectado:** {sentimento}")
                
                # Métricas detalhadas
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Polaridade", value=f"{polaridade:.2f}", help="Varia de -1.0 (muito negativo) a 1.0 (muito positivo)")
                with col2:
                    st.metric(label="Subjetividade", value=f"{subjetividade:.2f}", help="Varia de 0.0 (objetivo) a 1.0 (subjetivo)")
                
                # Mostrar o texto traduzido para transparência técnica
                with st.expander("Ver detalhes técnicos (Tradução)"):
                    st.write(f"**Texto Original:** {texto_usuario}")
                    st.write(f"**Texto Traduzido (para o TextBlob):** {texto_traduzido}")
                    
            except Exception as e:
                st.error(f"Ocorreu um erro durante o processamento: {e}")

if __name__ == "__main__":
    main()
