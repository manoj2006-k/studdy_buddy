import streamlit as st

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        PdfReader = None

# App Configuration
st.set_page_config(page_title="Local AI Study Buddy", page_icon="🎓")

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    pipeline = None
    TRANSFORMERS_AVAILABLE = False

# --- Load Instruction-Tuned Model ---
@st.cache_resource
def load_ai():
    if not TRANSFORMERS_AVAILABLE:
        return None

    try:
        return pipeline("text-generation", model="MBZUAI/LaMini-GPT-124M")
    except Exception:
        return None

with st.spinner("Loading Local AI (LaMini-GPT)..."):
    ai_engine = load_ai()

if ai_engine is None:
    st.info("The AI model is unavailable right now, so the app will use a lightweight fallback response.")

# --- Helper Functions ---
def extract_text(file):
    if file.type == "application/pdf":
        if PdfReader is None:
            return "PDF text extraction is unavailable because the PDF dependency is not installed."
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    return file.read().decode("utf-8", errors="ignore")

def generate_fallback_response(instruction, context=""):
    instruction_lower = instruction.lower()
    text = (context or "").strip()

    if "summarize" in instruction_lower:
        if not text:
            return "Please upload a document with content to summarize."
        sentences = [sentence.strip() for sentence in text.replace("\n", " ").split(".") if sentence.strip()]
        return " ".join(sentences[:3])[:700]

    if "explain" in instruction_lower:
        concept = instruction.replace("Explain the concept of", "", 1).replace("in simple terms", "", 1).strip()
        if concept:
            return f"{concept} is easier to understand when you break it into smaller parts and connect it to familiar examples."
        return "A concept becomes clearer when you explain it using simple, everyday language."

    if "question" in instruction_lower:
        if text:
            return "What is the main idea of the provided material?"
        return "Create a study question from the provided topic."

    return "The AI model is unavailable right now, so this fallback response is being shown instead."


def ask_ai(instruction, context=""):
    if ai_engine is None:
        return generate_fallback_response(instruction, context)

    # Formatting prompt specifically for LaMini (Instruction-tuned)
    prompt = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction} using this text: {context}\n\n### Response:"

    try:
        # max_new_tokens controls how long the answer is
        res = ai_engine(prompt, max_new_tokens=100, do_sample=True, temperature=0.7, return_full_text=False)
        return res[0]['generated_text'].strip()
    except Exception:
        return generate_fallback_response(instruction, context)

# --- UI Layout ---
st.title("🎓 AI Study Buddy (Offline)")
st.info("Task: text-generation | Model: LaMini-GPT-124M")

tab1, tab2, tab3 = st.tabs(["📝 Summarizer", "💡 Explainer", "❓ Quiz"])

# --- TAB 1: SUMMARIZER ---w
with tab1:
    st.header("Summarize Notes")
    doc = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    if st.button("Summarize Now"):
        if doc:
            raw_text = extract_text(doc)[:800] # Limit for speed
            with st.spinner("Summarizing..."):
                summary = ask_ai("Summarize the main points", raw_text)
                st.subheader("Summary Result:")
                st.write(summary)
        else:
            st.error("Please upload a file first.")

# --- TAB 2: CONCEPT EXPLAINER ---
with tab2:
    st.header("Concept Explainer")
    concept = st.text_input("Enter a concept to explain:")
    if st.button("Explain Simply"):
        if concept:
            with st.spinner("Thinking..."):
                explanation = ask_ai(f"Explain the concept of {concept} in simple terms", "")
                st.success(explanation)

# --- TAB 3: QUIZ ---
with tab3:
    st.header("Quiz Generator")
    quiz_input = st.text_area("Paste text to generate a question:")
    if st.button("Create Question"):
        if quiz_input:
            with st.spinner("Generating..."):
                # Asking specifically for a question
                question = ask_ai("Create a simple study question", quiz_input[:800])
                st.subheader("Question:")
                st.write(question)
                
                with st.expander("Show Answer"):
                    answer = ask_ai(f"Provide the answer to this question: {question}", quiz_input[:800])
                    st.write(answer)
