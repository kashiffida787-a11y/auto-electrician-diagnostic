import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="Auto Electrician Diagnostic", page_icon="🚗")

st.title("🚗 Auto Electrician Diagnostic")
st.write("گاڑی کا الیکٹریکل مسئلہ درج کریں اور حل تجویز کروائیں۔")

api_key = st.text_input("اپنی Gemini API Key درج کریں:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    user_query = st.text_area("مسئلے کی تفصیل لکھیں:")

    if st.button("ڈائیگنوز کریں"):
        if user_query:
            with st.spinner("تجزیہ کیا جا رہا ہے..."):
                prompt = f"You are an expert auto electrician. Diagnose and suggest solutions in clear Urdu language for: {user_query}"
                response = model.generate_content(prompt)
                st.write("### تجویز کردہ حل:")
                st.write(response.text)
        else:
            st.warning("براہ کرم پہلے اپنا مسئلہ درج کریں۔")
