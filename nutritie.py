import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="wide", page_icon="🍎")

# 2. Stil Vizual
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar pentru Autentificare
st.sidebar.title("🔐 Acces Proiect")
parola = st.sidebar.text_input("Introdu parola:", type="password")

if parola == "nutrifit2026":
    st.title("🍎 Aplicația Mariei - Dashboard Nutrițional")
    
    # Date în Sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Datele Tale")
    greutate = st.sidebar.number_input("Greutate (kg):", 40, 150, 70)
    obiectiv = st.sidebar.selectbox("Obiectivul tău:", ["Slăbire", "Menținere", "Masă Musculară"])
    
    proteine_g = st.sidebar.slider("Proteine (g/zi):", 50, 250, 120)
    carbo_g = st.sidebar.slider("Carbohidrați (g/zi):", 50, 500, 200)
    grasimi_g = st.sidebar.slider("Grăsimi (g/zi):", 20, 150, 60)

    # 4. Calcule
    cal_prot = proteine_g * 4
    cal_carb = carbo_g * 4
    cal_gras = grasimi_g * 9
    total_kcal = cal_prot + cal_carb + cal_gras

    # 5. Afișare Cifre Sus
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.metric("Total Calorii", f"{total_kcal} kcal")
    with col_b: st.metric("Obiectiv", obiectiv)
    with col_c: st.metric("Proteine/kg", f"{(proteine_g/greutate):.1f} g")

    st.markdown("---")

    # 6. Grafic și Meniu Zilnic
    tab1, tab2 = st.tabs(["📊 Analiză Macros", "📋 Meniu Zilnic Recomandat"])

    with tab1:
        date_nutritie = pd.DataFrame({
            "Nutrient": ["Proteine", "Carbohidrați", "Grăsimi"],
            "Calorii": [cal_prot, cal_carb, cal_gras]
        })
        fig = px.pie(date_nutritie, values='Calorii', names='Nutrient', hole=0.5,
                     color_discrete_sequence=['#2ca02c', '#1f77b4', '#ff7f0e'])
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader(f"🍴 Sugestie de meniu pentru {obiectiv}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🌅 Mic Dejun")
            st.write("- Omletă din 3 ouă cu spanac și brânză feta")
            st.write("- O felie de pâine integrală")
            
            st.markdown("### 🥗 Prânz")
            st.write("- Piept de pui la grătar (150g) cu quinoa")
            st.write("- Salată verde cu lămâie și ulei de măsline")

        with col2:
            st.markdown("### 🍎 Gustare")
            st.write("- Un iaurt grecesc cu câteva nuci sau migdale")
            
            st.markdown("### 🐟 Cină")
            st.write("- File de somon sau păstrăv la cuptor")
            st.write("- Sparanghel sau broccoli tras la tigaie")

    st.success(f"Bravo, Maria! Mergi pe drumul cel bun spre obiectivul de {obiectiv.lower()}!")

else:
    st.info("Introdu parola corectă pentru a vedea meniul și calculele.")
