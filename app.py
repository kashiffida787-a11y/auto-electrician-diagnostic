import streamlit as st
import google.generativeai as genai

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
                    # ایکٹیو Flash ماڈل خودکار طریقے سے منتخب کریں
                    all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    flash_models = [m for m in all_models if 'flash' in m]
                    
                    target_model = flash_models[0] if flash_models else "models/gemini-3.6-flash"
                    
                    model = genai.GenerativeModel(target_model)
                    system_prompt = "آپ ایک ماہر اٹو الیکٹریشن (Auto Electrician) ہیں۔ گاڑی کے الیکٹریکل یا مکینیکل مسئلے کو سمجھ کر آسان اور جامع اردو میں تفصیل، ممکنہ وجوہات اور حل تجویز کریں۔\n\n"
                    
                    if audio_value:
                        audio_bytes = audio_value.read()
                        audio_part = {
                            "mime_type": audio_value.type,
                            "data": audio_bytes
                        }
                        prompt = system_prompt + "برائے مہربانی اس آڈیو ریکارڈنگ میں گاڑی کے مسئلے کا جائزہ لے کر اردو میں حل بتائیں۔"
                        response = model.generate_content([prompt, audio_part])
                    else:
                        prompt = system_prompt + f"گاڑی کا مسئلہ: {user_query}"
                        response = model.generate_content(prompt)
                    
                    st.success("ڈائیگنوسس کی تفصیلات:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"کوئی غلطی پیش آئی ہے: {e}")
else:
    st.info("ایپ استعمال کرنے کے لیے اوپر اپنی Gemini API Key درج کریں۔")
