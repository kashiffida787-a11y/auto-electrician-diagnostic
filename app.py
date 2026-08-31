import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

st.set_page_config(page_title="Auto Electrician Diagnostic", page_icon="🚗")

st.title("🚗 Auto Electrician Diagnostic")
st.subheader("گاڑی کا الیکٹریکل مسئلہ درج کریں یا بول کر بتائیں اور حل تجویز کروائیں")

# API Key Input
api_key = st.text_input("درج کریں Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    tab1, tab2 = st.tabs(["📝 لکھ کر بتائیں (Text)", "🎤 بول کر بتائیں (Voice Input)"])
    
    user_query = ""
    audio_value = None
    
    with tab1:
        text_input = st.text_area("مسئلے کی تفصیل درج کریں:", height=150, placeholder="مثلاً: گاڑی کا سیلف سٹارٹ نہیں ہو رہا یا ہائبرڈ بیٹری وارننگ لائٹ آن ہے...")
        if text_input:
            user_query = text_input

    with tab2:
        st.info("مائیک کے بٹن پر کلک کر کے بولیں اور ریکارڈنگ مکمل ہونے پر دوبارہ کلک کریں۔")
        audio_value = st.audio_input("یہاں آواز ریکارڈ کریں:")
        if audio_value:
            st.audio(audio_value)
            st.success("آواز موصول ہو گئی ہے!")

    if st.button("ڈائیگنوز کریں"):
        if not user_query and not audio_value:
            st.warning("براہ کرم مسئلہ ٹائپ کریں یا آواز ریکارڈ کریں۔")
        else:
            with st.spinner("تجزیہ کیا جا رہا ہے... براہ کرم انتظار کریں۔"):
                try:
                    model = genai.GenerativeModel("models/gemini-3.6-flash")
                    system_prompt = """آپ ایک استاد اٹو الیکٹریشن ہیں۔ گاڑی کے مسئلے کو دیکھ کر سب سے پہلے پریکٹیکل اور عام وجوہات بتائیں (مثلاً: بیٹری ٹرمینل، ڈھیلی ارتھ والی تار، گرپ یا فیوز)۔ 

جواب دیتے وقت:
1. سب سے پہلے سب سے اہم اور فوری چیک کرنے والا حل بتائیں (خاص طور پر وائرنگ اور ارتھ کا کنکشن)۔
2. لمبی فہرستیں بنانے کے بجائے صرف 2 سے 3 بنیادی اور پکے حل بتائیں۔
3. سادہ اور عام فہم اردو زبان استعمال کریں۔"""
                    
                    if audio_value:
                        audio_bytes = audio_value.read()
                        audio_part = {
                            "mime_type": audio_value.type,
                            "data": audio_bytes
                        }
                        prompt = system_prompt + "\nبرائے مہربانی اس آڈیو ریکارڈنگ میں گاڑی کے مسئلے کا جائزہ لے کر اردو میں حل بتائیں۔"
                        response = model.generate_content([prompt, audio_part])
                    else:
                        prompt = system_prompt + f"\nگاڑی کا مسئلہ: {user_query}"
                        response = model.generate_content(prompt)
                    
                    answer_text = response.text
                    st.success("ڈائیگنوسس کی تفصیلات:")
                    st.markdown(answer_text)

                    # جواب کو آواز میں تبدیل کرنا (Text-to-Speech)
                    tts = gTTS(text=answer_text, lang='ur')
                    audio_file = "response.mp3"
                    tts.save(audio_file)
                    
                    st.audio(audio_file, format="audio/mp3", autoplay=True)
                    
                except Exception as e:
                    st.error(f"کوئی غلطی پیش آئی ہے: {e}")
else:
    st.info("ایپ استعمال کرنے کے لیے اوپر اپنی Gemini API Key درج کریں۔")
