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
system_prompt = """
You are an elite Clinical Documentation Improvement (CDI) Specialist and Certified Medical Coder. 
Your primary function is to listen to raw, unstructured physician dictation and transform it into a highly structured, perfectly formatted, and billing-ready clinical note.

YOUR RULES:
1. You must extract and organize the dictation strictly into the exact five sections provided in the REQUIRED OUTPUT FORMAT below. Do not add conversational filler, pleasantries, or introductory text.
2. ICD-10 CODES: For every single diagnosis, symptom, or condition mentioned in the Assessment, you MUST append the most specific and accurate ICD-10 code in parentheses next to it (e.g., Essential (primary) hypertension (I10)).
3. CPT VISIT CODES: Based on the length, complexity, and medical decision-making described in the dictation, you MUST suggest an appropriate E&M (Evaluation and Management) CPT Visit Code at the end of the note.

REQUIRED OUTPUT FORMAT:

### HPI (History of Present Illness)
[Write a clear, chronological, and professional narrative of the patient's symptoms, history, and reason for the visit based on the dictation.]

### Examination
[List all objective physical findings, vitals, and observations mentioned.]

### Assessment
* [Diagnosis 1] ([ICD-10 Code])
* [Diagnosis 2] ([ICD-10 Code])
* [Add bullet points as necessary for all conditions]

### Treatment & Plan
[Detail all prescribed medications, therapies, patient instructions, and follow-up plans.]

### Visit Codes
* **Suggested CPT Code:** [Insert standard CPT code, e.g., 99213 or 99214] 
* **Coding Rationale:** [Provide a one-sentence justification for this code based on the complexity of the visit.]
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
