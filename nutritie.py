import streamlit as st
import pandas as pd

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Aplicația Mariei", layout="wide", page_icon="🍎")

# 2. SECURITATE
if "autentificat" not in st.session_state:
    st.session_state.autentificat = False

if not st.session_state.autentificat:
    st.title("🔒 Acces Protejat")
    parola = st.text_input("Introdu parola:", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state.autentificat = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
    st.stop()

# 3. INTERFAȚĂ PRINCIPALĂ
st.title("🍎 Aplicația Mariei")

tab1, tab2, tab3 = st.tabs(["📊 Calculator Metodic", "🍱 Planificator cu Gramaje", "🛒 Listă Cumpărături"])

# --- TAB 1: CALCULATOR ---
if 'tinta_kcal' not in st.session_state:
    st.session_state.tinta_kcal = 1500 # Valoare default

with tab1:
    st.subheader("📊 Calcul Necesar Caloric (GA x IC)")
    col1, col2 = st.columns(2)
    with col1:
        ga = st.number_input("Greutate Actuală (GA) - kg:", 40.0, 200.0, 75.0)
        sex = st.radio("Sex:", ["Masculin", "Feminin"], horizontal=True)
        ic_optiuni = {
            "Activitate sedentară (25-30 kcal/kg)": [25, 30],
            "Activități zilnice ușoare (30-35 kcal/kg)": [30, 35],
            "Activități zilnice medii (35-40 kcal/kg)": [35, 40],
            "Activități zilnice mari (40-45 kcal/kg)": [40, 45],
            "Activități zilnice foarte mari (45-50 kcal/kg)": [45, 50]
        }
        nivel = st.selectbox("Nivel de activitate (IC):", list(ic_optiuni.keys()))
        valori_ic = ic_optiuni[nivel]
    with col2:
        st.info("💡 Obiectiv: Scădere în Greutate")
        deficit = st.slider("Valoare scădere (kcal/zi):", 500, 1000, 500)
        
    if st.button("CALCULEAZĂ INTERVALUL DE REFERINȚĂ"):
        factor_rmb = 1.0 if sex == "Masculin" else 0.9
        rmb_val = factor_rmb * ga * 24
        necesar_min = ga * valori_ic[0]
        necesar_max = ga * valori_ic[1]
        tinta_min = max(rmb_val, necesar_min - deficit)
        tinta_max = max(rmb_val, necesar_max - deficit)
        
        st.session_state.tinta_kcal = (tinta_min + tinta_max) / 2
        st.session_state.rezultate = {"rmb": rmb_val, "n_min": necesar_min, "n_max": necesar_max, "t_min": tinta_min, "t_max": tinta_max}
        st.session_state.calculat = True

    if st.session_state.get('calculat'):
        res = st.session_state.rezultate
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("📉 RMB", f"{res['rmb']:.0f} kcal")
        c2.metric("⚖️ Menținere", f"{res['n_min']:.0f}-{res['n_max']:.0f} kcal")
        c3.warning(f"🎯 Țintă Medie: {st.session_state.tinta_kcal:.0f} kcal")

# --- TAB 2: PLANIFICATOR CU GRAMAJE ---
with tab2:
    st.subheader(f"🍱 Meniu Săptămânal adaptat la {st.session_state.tinta_kcal:.0f} kcal")
    
    # Proporții calorice pe mese
    distributie = {"MD": 0.25, "G1": 0.10, "PZ": 0.35, "G2": 0.10, "CN": 0.20}
    
    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    
    # Bază de date simplificată (kcal/100g)
    db = {
        "Omletă": 150, "Ovăz": 350, "Pâine avocado": 220, "Iaurt grecesc": 100,
        "Măr": 52, "Nuci": 650, "Baton proteic": 380, "Brânză cottage": 98,
        "Pui grătar": 165, "Pește cuptor": 120, "Curcan": 140, "Salată ton": 110,
        "Supă cremă": 50, "Pește alb": 90, "Iaurt semințe": 130
    }

    def calc_gr(masa, kcal_tinta):
        kcal_masa = st.session_state.tinta_kcal * distributie[masa]
        return kcal_masa

    tabel_date = []
    for zi in zile:
        with st.expander(f"📅 Configurează {zi}"):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1: 
                md = st.selectbox("Mic Dejun", list(opt for opt in db.keys() if opt in ["Omletă", "Ovăz", "Pâine avocado"]), key=f"md_{zi}")
                gr_md = (calc_gr("MD", st.session_state.tinta_kcal) / db[md]) * 100
            with col2: 
                g1 = st.selectbox("Gustare 1", ["Măr", "Nuci", "Iaurt grecesc"], key=f"g1_{zi}")
                gr_g1 = (calc_gr("G1", st.session_state.tinta_kcal) / db[g1]) * 100
            with col3: 
                pz = st.selectbox("Prânz", ["Pui grătar", "Pește cuptor", "Curcan", "Salată ton"], key=f"pz_{zi}")
                gr_pz = (calc_gr("PZ", st.session_state.tinta_kcal) / db[pz]) * 100
            with col4: 
                g2 = st.selectbox("Gustare 2", ["Baton proteic", "Brânză cottage", "Nuci"], key=f"g2_{zi}")
                gr_g2 = (calc_gr("G2", st.session_state.tinta_kcal) / db[g2]) * 100
            with col5: 
                cn = st.selectbox("Cină", ["Supă cremă", "Pește alb", "Iaurt semințe"], key=f"cn_{zi}")
                gr_cn = (calc_gr("CN", st.session_state.tinta_kcal) / db[cn]) * 100
            
            tabel_date.append({
                "Ziua": zi, 
                "Mic Dejun": f"{md} ({gr_md:.0f}g)", 
                "Gustare 1": f"{g1} ({gr_g1:.0f}g)", 
                "Prânz": f"{pz} ({gr_pz:.0f}g)", 
                "Gustare 2": f"{g2} ({gr_g2:.0f}g)", 
                "Cină": f"{cn} ({gr_cn:.0f}g)"
            })

    st.markdown("---")
    df_plan = pd.DataFrame(tabel_date)
    st.table(df_plan)

    csv = df_plan.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Descarcă Planul cu Gramaje", data=csv, file_name="meniu_gramaje.csv", mime="text/csv")

# --- TAB 3: LISTA ---
with tab3:
    st.subheader("🛒 Lista de Cumpărături")
    st.write("Cumpără alimentele selectate și cântărește-le conform indicațiilor din tabel.")
