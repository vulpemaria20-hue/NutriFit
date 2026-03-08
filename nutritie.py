import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="wide", page_icon="🍎")

# 2. Stil Vizual (VARIANTA REPARATĂ)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar pentru Autentificare
st.sidebar.title("🔐 Acces Proiect")
parola = st.sidebar.text_input("Introdu parola:", type="password")

if parola == "nutrifit2026":
    st.title("🍎 Aplicația Mariei - Calculator Nutrițional")
    
    # Date în Sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Datele Tale")
    greutate = st.sidebar.number_input("Greutate (kg):", 40, 150, 70)
    proteine_g = st.sidebar.slider("Proteine (g/zi):", 50, 250, 120)
    carbo_g = st.sidebar.slider("Carbohidrați (g/zi):", 50, 500, 200)
    grasimi_g = st.sidebar.slider("Grăsimi (g/zi):", 20, 150, 60)

    # 4. Calcule Calorice
    cal_prot = proteine_g * 4
    cal_carb = carbo_g * 4
    cal_gras = grasimi_g * 9
    total_kcal = cal_prot + cal_carb + cal_gras

    # 5. Afișare Metrică Principală
    st.metric("Total Calorii Zilnice", f"{total_kcal} kcal")
    st.markdown("---")

    # 6. Grafic și Recomandări
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 Distribuția Calorică")
        date_nutritie = pd.DataFrame({
            "Nutrient": ["Proteine", "Carbohidrați", "Grăsimi"],
            "Calorii": [cal_prot, cal_carb, cal_gras]
        })
        
        fig = px.pie(date_nutritie, values='Calorii', names='Nutrient', 
                     hole=0.5,
                     color_discrete_sequence=['#2ca02c', '#1f77b4', '#ff7f0e'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📝 Recomandări")
        ratio = proteine_g / greutate
        st.write(f"La o greutate de **{greutate} kg**, consumul tău este de **{ratio:.1f}g proteine / kg corp**.")
        
        if ratio < 1.2:
            st.warning("Sfat: Încearcă să crești proteinele pentru a proteja masa musculară.")
        else:
            st.success("Aportul de proteine este optim!")

else:
    st.info("Introdu parola 'nutrifit2026' în meniul lateral pentru a vedea datele.")
