import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

st.set_page_config(
    page_title="المساعد القانوني المصري",
    page_icon="⚖️",
    layout="centered"
)

st.markdown('''
    <style>
    .main { direction: rtl; text-align: right; }
    .stTextArea textarea { direction: rtl; text-align: right; }
    </style>
''', unsafe_allow_html=True)

@st.cache_resource
def load_all():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    vectordb = FAISS.load_local(
        "/kaggle/working/legal_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-Nemo-Instruct-2407")
    model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-Nemo-Instruct-2407",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return vectordb, tokenizer, model

vectordb, tokenizer, model = load_all()

def retrieve(question, k=7):
    results = vectordb.similarity_search_with_score(question, k=k)
    results.sort(key=lambda x: x[1])
    seen = set()
    unique = []
    for doc, score in results:
        key = (doc.metadata["document"], doc.metadata["article"])
        if key not in seen:
            seen.add(key)
            unique.append((doc, score))
    THRESHOLD = 1.3
    filtered = [(doc, score) for doc, score in unique if score < THRESHOLD]
    if not filtered:
        filtered = [unique[0]]
    return filtered

def build_prompt(question, docs):
    context_parts = []
    for doc in docs:
        meta = doc.metadata
        label = f"المادة {meta['article_label']}" if meta.get("article_label") else f"المادة ({meta['article']})"
        book    = f" | {meta['book']}"    if meta.get("book")    else ""
        chapter = f" | {meta['chapter']}" if meta.get("chapter") else ""
        context_parts.append(f"{label}{book}{chapter}:\\n{doc.page_content}")
    context = "\\n\\n---\\n\\n".join(context_parts)
    return f"<s>[INST] أنت مساعد قانوني متخصص في قانون العمل المصري رقم 14 لسنة 2025.\\n\\nمهمتك:\\n- اقرأ النصوص القانونية جيدًا وأجب على السؤال منها مباشرة.\\n- اذكر رقم المادة التي استندت إليها.\\n- إذا كانت النصوص تتعلق بالسؤال ولو بشكل غير مباشر، استخدمها للإجابة.\\n- حاول دائمًا استخلاص الإجابة من النصوص حتى لو لم تذكر السؤال بنفس الكلمات.\\n-  إذا لم تكن النصوص تجيب على السؤال بشكل مباشر، قدم ما هو أقرب إجابة ممكنة من النصوص المتاحة وأوضح ذلك للمستخدم و لا تقل أبدًا لا توجد معلومات إلا إذا كانت النصوص لا علاقة لها بالسؤال تمامًا.\\n- لا تخترع معلومات غير موجودة في النصوص.\\n\\nالنصوص القانونية:\\n{context}\\n\\nالسؤال: {question} [/INST]"


def generate_answer(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda:0")
    input_length = inputs["input_ids"].shape[1]
    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        do_sample=True,
        temperature=0.1,
        top_k=50,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id
    )
    new_tokens = outputs[0][input_length:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True)

st.title("⚖️ المساعد القانوني المصري")
st.caption("قانون العمل رقم 14 لسنة 2025 — الجريدة الرسمية")
st.divider()

question = st.text_area(
    "اكتب سؤالك القانوني:",
    height=100,
    placeholder="مثال: ما هي حقوقي إذا تم فصلي من العمل؟"
)

if st.button("ابحث في القانون ⚖️"):
    if not question.strip():
        st.warning("من فضلك اكتب سؤالاً.")
    else:
        with st.spinner("جاري البحث في نصوص القانون..."):
            results = retrieve(question, k=7)
            docs = [doc for doc, score in results]

        with st.spinner("جاري توليد الإجابة..."):
            prompt = build_prompt(question, docs)
            answer = generate_answer(prompt)

        st.success("الإجابة القانونية:")
        st.write(answer)
        st.divider()

        with st.expander("📖 المواد القانونية المستخدمة"):
            for doc, score in results:
                meta  = doc.metadata
                label = f"المادة {meta['article_label']}" if meta.get("article_label") else f"المادة ({meta['article']})"
                st.markdown(f"**{label}** — {meta.get('book', 'قانون الإصدار')} | Score: {score:.3f}")
                st.write(doc.page_content[:400] + "...")
                st.divider()

        st.caption("⚠️ هذا المساعد للاسترشاد فقط وليس استشارة قانونية رسمية.")
