import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="wide", page_icon="🍎")

# 2. Stil Vizual (Opțional)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_index=True)

# 3. Sidebar pentru Autentificare și Date
st.sidebar.title("🔐 Acces Proiect")
parola = st.sidebar.text_input("Introdu parola:", type="password")

if parola == "nutrifit2026":
    st.title("🍎 Aplicația Mariei - Calculator Nutrițional")
    st.info("Completează datele în stânga pentru a vedea analiza dietei tale.")
    
    # Introducere Date în Sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Datele Tale")
    greutate = st.sidebar.number_input("Greutate (kg):", 40, 150, 70)
    proteine_g = st.sidebar.slider("Proteine (g/zi):", 50, 250, 120)
    carbo_g = st.sidebar.slider("Carbohidrați (g/zi):", 50, 500, 200)
    grasimi_g = st.sidebar.slider("Grăsimi (g/zi):", 20, 150, 60)

    # 4. Calcule (1g Prot=4kcal, 1g Carb=4kcal, 1g Grasime=9kcal)
    cal_prot = proteine_g * 4
    cal_carb = carbo_g * 4
    cal_gras = grasimi_g * 9
    total_kcal = cal_prot + cal_carb + cal_gras

    # 5. Afișare Rezultate în Coloane
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Calorii", f"{total_kcal} kcal")
    c2.metric("Proteine", f"{proteine_g}g ({int(cal_prot/total_kcal*100)}%)")
    c3.metric("Obiectiv", "Menținere" if total_kcal < 2500 else "Masă Musculară")

    st.markdown("---")

    # 6. Graficul Circular Interactiv
    col_stanga, col_dreapta = st.columns([1, 1])

    with col_stanga:
        st.subheader("📊 Distribuția Calorică")
        date_nutritie = pd.DataFrame({
            "Nutrient": ["Proteine", "Carbohidrați", "Grăsimi"],
            "Calorii": [cal_prot, cal_carb, cal_gras]
        })
        
        fig = px.pie(date_nutritie, values='Calorii', names='Nutrient', 
                     hole=0.5, 
                     color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c'])
        st.plotly_chart(fig, use_container_width=True)

    with col_dreapta:
        st.subheader("📝 Recomandări")
        st.write(f"La o greutate de **{greutate} kg**, consumul tău de proteine este de **{(proteine_g/greutate):.1f}g/kg corp**.")
        if proteine_g/greutate < 1.2:
            st.warning("Ar putea fi util să crești aportul de proteine pentru susținerea masei musculare.")
        else:
            st.success("Aportul de proteine este optim pentru un stil de viață activ!")

else:
    st.warning("Te rugăm să introduci parola corectă în meniul lateral pentru a vedea aplicația.")
    st.image("https://images.unsplash.com/photo-1490818387583-1baba5e638af?q=80&w=1000", caption="Nutriție Sănătoasă")
