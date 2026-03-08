import streamlit as st
import pandas as pd
import io

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
    st.session_state.tinta_kcal = 1500

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
        
    if st.button("CALCULEAZĂ"):
        factor_rmb = 1.0 if sex == "Masculin" else 0.9
        rmb_val = factor_rmb * ga * 24
        necesar_min = ga * valori_ic[0]
        necesar_max = ga * valori_ic[1]
        tinta_min = max(rmb_val, necesar_min - deficit)
        tinta_max = max(rmb_val, necesar_max - deficit)
        
        st.session_state.tinta_kcal = (tinta_min + tinta_max) / 2
        st.session_state.rezultate = {"rmb": rmb_val, "t_min": tinta_min, "t_max": tinta_max}
        st.session_state.calculat = True

    if st.session_state.get('calculat'):
        res = st.session_state.rezultate
        st.success(f"🎯 Țintă: {st.session_state.tinta_kcal:.0f} kcal (Min: {res['t_min']:.0f} | RMB: {res['rmb']:.0f})")

# --- TAB 2: PLANIFICATOR ---
with tab2:
    st.subheader(f"🍱 Planificator (Țintă: {st.session_state.tinta_kcal:.0f} kcal)")
    distributie = {"MD": 0.25, "G1": 0.10, "PZ": 0.35, "G2": 0.10, "CN": 0.20}
    db = {
        "Omletă": 150, "Ovăz": 350, "Pâine avocado": 220, "Iaurt grecesc": 100,
        "Măr": 52, "Nuci": 650, "Baton proteic": 380, "Brânză cottage": 98,
        "Pui grătar": 165, "Pește cuptor": 120, "Curcan": 140, "Salată ton": 110,
        "Supă cremă": 50, "Pește alb": 90, "Iaurt semințe": 130
    }

    tabel_date = []
    lista_alimente_selectate = []

    for zi in ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]:
        with st.expander(f"📅 {zi}"):
            cols = st.columns(5)
            # MD
            md = cols[0].selectbox("Mic Dejun", ["Omletă", "Ovăz", "Pâine avocado"], key=f"md_{zi}")
            gr_md = (st.session_state.tinta_kcal * distributie["MD"] / db[md]) * 100
            # G1
            g1 = cols[1].selectbox("Gustare 1", ["Măr", "Nuci", "Iaurt grecesc"], key=f"g1_{zi}")
            gr_g1 = (st.session_state.tinta_kcal * distributie["G1"] / db[g1]) * 100
            # PZ
            pz = cols[2].selectbox("Prânz", ["Pui grătar", "Pește cuptor", "Curcan", "Salată ton"], key=f"pz_{zi}")
            gr_pz = (st.session_state.tinta_kcal * distributie["PZ"] / db[pz]) * 100
            # G2
            g2 = cols[3].selectbox("Gustare 2", ["Baton proteic", "Brânză cottage", "Nuci"], key=f"g2_{zi}")
            gr_g2 = (st.session_state.tinta_kcal * distributie["G2"] / db[g2]) * 100
            # CN
            cn = cols[4].selectbox("Cină", ["Supă cremă", "Pește alb", "Iaurt semințe"], key=f"cn_{zi}")
            gr_cn = (st.session_state.tinta_kcal * distributie["CN"] / db[cn]) * 100
            
            tabel_date.append({
                "Ziua": zi, "Mic Dejun": f"{md} ({gr_md:.0f}g)", "Gustare 1": f"{g1} ({gr_g1:.0f}g)",
                "Prânz": f"{pz} ({gr_pz:.0f}g)", "Gustare 2": f"{g2} ({gr_g2:.0f}g)", "Cină": f"{cn} ({gr_cn:.0f}g)"
            })
            lista_alimente_selectate.extend([(md, gr_md), (g1, gr_g1), (pz, gr_pz), (g2, gr_g2), (cn, gr_cn)])

    df_plan = pd.DataFrame(tabel_date)
    st.table(df_plan)

    # EXPORT EXCEL
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_plan.to_excel(writer, index=False, sheet_name='Meniu')
    st.download_button(label="📥 Descarcă Meniul în EXCEL", data=output.getvalue(), file_name="meniu_mariei.xlsx", mime="application/vnd.ms-excel")

# --- TAB 3: LISTA CUMPĂRĂTURI ---
with tab3:
    st.subheader("🛒 Lista de Cumpărături Automată")
    if lista_alimente_selectate:
        df_lista = pd.DataFrame(lista_alimente_selectate, columns=['Aliment', 'Cantitate'])
        totaluri = df_lista.groupby('Aliment')['Cantitate'].sum().reset_index()
        for _, row in totaluri.iterrows():
            st.write(f"✅ **{row['Aliment']}**: {row['Cantitate']/1000:.2f} kg / {row['Cantitate']:.0f} g")
    else:
        st.info("Configurează meniul în Tab-ul 2 pentru a genera lista.")
