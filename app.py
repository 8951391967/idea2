import streamlit as st
import google.generativeai as genai
import re

# ---------- CLEAN OUTPUT ----------
def clean_output(text):
    text = re.sub(r"\*\*", "", text)
    text = text.replace("---", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="PlotTwist AI",
    page_icon="🎬",
    layout="wide"
)

# ---------- MODERN UI ----------
st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#070b14,#0b1220);
color:white;
font-family:Arial;
}

/* NAVBAR */

.navbar{
position:fixed;
top:0;
width:100%;
height:60px;
background:rgba(10,15,30,0.85);
backdrop-filter:blur(12px);
display:flex;
justify-content:space-between;
align-items:center;
padding:0 40px;
border-bottom:1px solid rgba(255,255,255,0.08);
z-index:1000;
}

.logo{
font-size:18px;
font-weight:bold;
color:#00d4ff;
}

/* HERO */

.hero{
text-align:center;
margin-top:120px;
margin-bottom:30px;
}

.hero h1{
font-size:44px;
}

.hero p{
opacity:0.7;
}

/* INPUT CARD */

.card{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:15px;
border:1px solid rgba(255,255,255,0.1);
box-shadow:0px 0px 20px rgba(0,212,255,0.1);
}

/* OUTPUT */

.output{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:15px;
border:1px solid rgba(255,255,255,0.12);
line-height:1.8;
white-space:pre-line;
font-size:16px;
box-shadow:0px 0px 20px rgba(0,212,255,0.15);
}

/* BUTTON */

.stButton>button{
width:100%;
background:linear-gradient(90deg,#00d4ff,#0077ff);
color:white;
border-radius:10px;
padding:12px;
font-weight:bold;
font-size:16px;
border:none;
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.02);
box-shadow:0px 0px 15px rgba(0,212,255,0.3);
}

</style>
""", unsafe_allow_html=True)

# ---------- NAVBAR ----------
st.markdown("""
<div class="navbar">
<div class="logo">🎬 PlotTwist AI</div>
<div style="opacity:0.7;font-size:14px;">AI Story Writing Assistant</div>
</div>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
<h1>Create Unexpected Plot Twists</h1>
<p>Generate shocking and cinematic twists for your story instantly</p>
</div>
""", unsafe_allow_html=True)

# ---------- API KEY ----------
api_key = st.text_input("🔑 Enter Gemini API Key", type="password")

# ---------- INPUT SECTION ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    genre = st.text_input("🎭 Story Genre")
    characters = st.text_input("🧑 Main Characters")

with col2:
    setting = st.text_input("🌍 Story Setting")
    tone = st.selectbox(
        "🎬 Story Tone",
        ["Dark", "Mystery", "Emotional", "Thriller", "Epic", "Funny"]
    )

twist_level = st.slider(
    "🔥 Twist Intensity",
    1, 10, 7
)

generate = st.button("🚀 Generate Plot Twists")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- PROMPT ----------
def prompt():
    return f"""
You are a world-class Hollywood screenwriter.

Create extremely creative and unexpected plot twists.

Rules:
- cinematic
- surprising
- emotional
- short but powerful
- use emojis
- twists must be shocking

Story details:

Genre: {genre}
Characters: {characters}
Setting: {setting}
Tone: {tone}
Twist Intensity: {twist_level}/10


FORMAT:

🎬 STORY IDEA
Short exciting concept

🔥 PLOT TWISTS
1.
2.
3.
4.
5.

💥 FINAL SHOCKING TWIST
The biggest twist that completely changes the story.
"""


# ---------- GENERATE ----------
if generate:

    if not api_key:
        st.error("⚠️ Please enter API key")

    else:

        genai.configure(api_key=api_key)

        # ---------- MODEL DETECTION ----------
        models = genai.list_models()

        model_name = None

        for m in models:
            if "generateContent" in m.supported_generation_methods and "gemini" in m.name:
                model_name = m.name
                break

        if not model_name:
            st.error("❌ No compatible Gemini model found")
            st.stop()

        model = genai.GenerativeModel(model_name)

        with st.spinner("🧠 AI is crafting shocking plot twists..."):

            response = model.generate_content(prompt())
            output = response.text

        cleaned_output = clean_output(output)

        st.markdown("## ✨ Your Plot Twists")

        formatted_output = cleaned_output.replace("\n", "<br>")

        st.markdown(f"""
<div class="output">
{formatted_output}
</div>
""", unsafe_allow_html=True)

        st.download_button(
            "📥 Download Story",
            cleaned_output,
            file_name="plot_twist_story.txt"
        )