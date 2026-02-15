import streamlit as st
from groq import Groq

# --- INITIALIZATION ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Clinical Scribe (Beta)", page_icon="🩺", layout="centered")

# --- CUSTOM CSS: CLINICAL THEME ---
st.markdown("""
    <style>
    /* Clean, soft medical background */
    .stApp {
        background-color: #f4f7f6;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Hide Streamlit branding */
    footer {visibility: hidden;}
    
    /* Professional Header */
    h1 {
        color: #1a365d;
        font-weight: 700;
        text-align: center;
        padding-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #4a5568;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }

    /* Beta/HIPAA Warning Banner */
    .beta-warning {
        background-color: #fff5f5;
        border-left: 5px solid #e53e3e;
        padding: 15px;
        border-radius: 4px;
        color: #c53030;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 25px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER & WARNING ---
st.title("🩺 AI Clinical Scribe")
st.markdown('<div class="subtitle">Automated SOAP Note Generator • Beta v1.0</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="beta-warning">
        ⚠️ BETA TESTING MODE: This application is currently running on a public API. 
        <b>DO NOT enter real patient names, DOBs, or any identifying Protected Health Information (PHI).</b> 
        Use dummy identifiers (e.g., "Mickey Mouse" or "Patient X") for testing purposes.
    </div>
""", unsafe_allow_html=True)

# --- SYSTEM PROMPT ---
scribe_prompt = """
You are an expert medical scribe assisting a Family Nurse Practitioner. 
Your job is to take the raw, unstructured dictation provided by the NP and format it into a highly professional, standard medical SOAP note.

CRITICAL RULES:
1. Format clearly with headings: SUBJECTIVE, OBJECTIVE, ASSESSMENT, PLAN.
2. Filter out any filler words, verbal stumbles, or casual conversational text.
3. Use standard medical terminology and abbreviations where appropriate.
4. If a section has no data in the dictation, write "No data provided."
5. Do not invent or hallucinate any symptoms, vitals, or treatments not explicitly stated in the dictation.
"""

# --- USER INPUT ---
st.subheader("📝 Raw Dictation")
dictation_input = st.text_area(
    "Paste or type the patient dictation below. (Tip: Use your device's native microphone to dictate!)", 
    height=200, 
    placeholder="Example: Patient is a 45-year-old male coming in today complaining of a sore throat for the last 3 days. Vitals are stable, BP 120/80..."
)

# --- PROCESSING & OUTPUT ---
if st.button("Generate SOAP Note", type="primary", use_container_width=True):
    if dictation_input.strip():
        with st.spinner("Structuring clinical note..."):
            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": scribe_prompt},
                        {"role": "user", "content": dictation_input}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.2, 
                    max_tokens=1000
                )
                
                st.subheader("📋 Structured SOAP Note")
                structured_note = response.choices[0].message.content
                
                # Success message and instructions for the clipboard
                st.success("✅ Note generated successfully! Hover over the box below and click the copy icon in the top right corner to copy to your clipboard.")
                
                # Using st.code with language="text" provides a native, clean copy-to-clipboard button
                st.code(structured_note, language="text")
                
                # The Download Button
                st.download_button(
                    label="📥 Download as Text File",
                    data=structured_note,
                    file_name="SOAP_Note.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"API Error: {e}")
    else:
        st.warning("Please enter dictation text before generating.")
