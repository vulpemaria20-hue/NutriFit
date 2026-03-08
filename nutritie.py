Ai dreptate, în ultima versiune de cod ne-am concentrat atât de mult pe formulele de calcul, încât am omis funcția de export. Pentru a putea descărca tabelul cu meniul tău în format Excel (sau CSV, care se deschide direct în Excel), trebuie să adăugăm un buton special sub tabelul de planificare.

Iată codul actualizat pentru nutritie.py care include acum și butonul de Download:

Python
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

tab1, tab2, tab3 = st.tabs(["📊 Calculator Metodic", "🍱 Planificator 5 Mese", "🛒 Listă Cumpărături"])

# --- TAB 1: CALCULATOR ---
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
        st.session_state.rezultate = {"rmb": rmb_val, "n_min": necesar_min, "n_max": necesar_max, "t_min": tinta_min, "t_max": tinta_max}
        st.session_state.calculat = True

    if st.session_state.get('calculat'):
        res = st.session_state.rezultate
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("📉 RMB (Limita inferioară)", f"{res['rmb']:.0f} kcal")
        c2.metric("⚖️ Menținere (Interval)", f"{res['n_min']:.0f} - {res['n_max']:.0f} kcal")
        c3.warning(f"🎯 Țintă Slăbire: {res['t_min']:.0f} - {res['t_max']:.0f} kcal")

# --- TAB 2: PLANIFICATOR ---
with tab2:
    st.subheader("🍱 Meniu Săptămânal (3 Mese + 2 Gustări)")
    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    
    optiuni_md = ["Omletă cu legume", "Iaurt cu ovăz", "Pâine integrală cu avocado", "Ouă ochiuri și brânză"]
    optiuni_g = ["Măr", "Nuci crude", "Iaurt", "Migdale", "Brânză cottage", "Baton proteic"]
    optiuni_p = ["Pui la grătar cu salată", "Pește la cuptor", "Curcan cu legume", "Salată cu ton și porumb"]
    optiuni_c = ["Supă cremă de legume", "Salată verde cu ou", "Pește alb și sparanghel", "Iaurt cu semințe de chia"]

    tabel_date = []
    for zi in zile:
        with st.expander(f"📅 Configurează {zi}"):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1: md = st.selectbox("Mic Dejun", optiuni_md, key=f"md_{zi}")
            with col2: g1 = st.selectbox("Gustare 1", optiuni_g, key=f"g1_{zi}")
            with col3: pz = st.selectbox("Prânz", optiuni_p, key=f"pz_{zi}")
            with col4: g2 = st.selectbox("Gustare 2", optiuni_g, key=f"g2_{zi}")
            with col5: cn = st.selectbox("Cină", optiuni_c, key=f"cn_{zi}")
            tabel_date.append({"Ziua": zi, "Mic Dejun": md, "Gustare 1": g1, "Prânz": pz, "Gustare 2": g2, "Cină": cn})

    st.markdown("---")
    st.subheader("📋 Planul tău curent")
    df_plan = pd.DataFrame(tabel_date)
    st.table(df_plan)

    # BUTON EXPORT EXCEL (CSV)
    csv = df_plan.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descarcă Meniul în Excel (CSV)",
        data=csv,
        file_name="meniu_saptamanal_mariei.csv",
        mime="text/csv",
