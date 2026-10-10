import streamlit as st

st.set_page_config(page_title="Hushållsekonomi", page_icon="💰", layout="wide")

st.title("🏡 Hushållsekonomi & Bolånekalkyl")

# --- 1. INKOMSTER ---
st.header("1. Inkomster (Netto)")
col1, col2 = st.columns(2)

with col1:
    brutto_david = st.number_input("Bruttolön David (kr)", value=47500, step=500)
    skatt_pct = st.slider("Beräknad skatt (%)", min_value=20.0, max_value=50.0, value=34.0, step=0.5)
    netto_david = brutto_david * (1 - (skatt_pct / 100))
    st.info(f"Netto David: **{netto_david:,.0f} kr**")

with col2:
    brutto_elin = st.number_input("Bruttolön Elin (kr)", value=41500, step=500)
    netto_elin = brutto_elin * (1 - (skatt_pct / 100))
    st.info(f"Netto Elin: **{netto_elin:,.0f} kr**")

ovrig_inkomst = st.number_input("Övriga inkomster netto (kr)", value=0, step=500)
totalt_inkomster = netto_david + netto_elin + ovrig_inkomst

# --- 2. HUSLÅN ---
st.header("2. Huslån & Bolån")
rant_extra = st.slider("Simulera ränteändring alla lån (%-enheter)", min_value=-2.0, max_value=5.0, value=0.0, step=0.25)

col_l1, col_l2, col_l3 = st.columns(3)

with col_l1:
    st.subheader("Lån 1 (Större)")
    skuld_1 = st.number_input("Skuld Lån 1 (kr)", value=1162500, step=10000)
    ranta_1 = st.number_input("Ränta Lån 1 (%)", value=2.25, step=0.05) + rant_extra
    amortering_1 = st.number_input("Amortering Lån 1 (kr/mån)", value=0, step=500)
    tot_lan_1 = ((skuld_1 * (ranta_1 / 100)) / 12) * 0.70 + amortering_1
    st.write(f"Efter ränteavdrag: **{tot_lan_1:,.0f} kr/mån**")

with col_l2:
    st.subheader("Lån 2 (Större)")
    skuld_2 = st.number_input("Skuld Lån 2 (kr)", value=1162500, step=10000)
    ranta_2 = st.number_input("Ränta Lån 2 (%)", value=2.25, step=0.05) + rant_extra
    amortering_2 = st.number_input("Amortering Lån 2 (kr/mån)", value=0, step=500)
    tot_lan_2 = ((skuld_2 * (ranta_2 / 100)) / 12) * 0.70 + amortering_2
    st.write(f"Efter ränteavdrag: **{tot_lan_2:,.0f} kr/mån**")

with col_l3:
    st.subheader("Lån 3 (Mindre)")
    skuld_3 = st.number_input("Skuld Lån 3 (kr)", value=236598, step=5000)
    ranta_3 = st.number_input("Ränta Lån 3 (%)", value=1.70, step=0.05) + rant_extra
    amortering_3 = st.number_input("Amortering Lån 3 (kr/mån)", value=int((skuld_3 * 0.02) / 12), step=100)
    tot_lan_3 = ((skuld_3 * (ranta_3 / 100)) / 12) * 0.70 + amortering_3
    st.write(f"Efter ränteavdrag: **{tot_lan_3:,.0f} kr/mån**")

summa_huslan = tot_lan_1 + tot_lan_2 + tot_lan_3

# --- 3. FASTA UTGIFTER ---
st.header("3. Övriga Fasta Utgifter")
c1, c2 = st.columns(2)
with c1:
    billan = st.number_input("Billån", value=4100)
    el_tibber = st.number_input("El (Tibber)", value=0)
    el_ellevio = st.number_input("Elnät (Ellevio)", value=0)
    bredband = st.number_input("Bredband", value=0)
    tv = st.number_input("TV", value=0)
    mobil = st.number_input("Mobil", value=0)
    vatten_sopor = st.number_input("Vatten/sopor", value=0)
with c2:
    forskola = st.number_input("Förskola", value=0)
    a_kassa_fack = st.number_input("A-kassa & Fack", value=0)
    csn = st.number_input("CSN", value=0)
    ovriga_fasta = st.number_input("Övrigt fast", value=0)

summa_fasta = summa_huslan + billan + el_tibber + el_ellevio + bredband + tv + mobil + vatten_sopor + forskola + a_kassa_fack + csn + ovriga_fasta

# --- 4. RÖRLIGA & SPARANDE ---
st.header("4. Rörliga Utgifter & Sparande")
r1, r2 = st.columns(2)
with r1:
    mat = st.number_input("Mat/livsmedel", value=7000)
    fickpeng_d = st.number_input("Fickpeng David", value=5000)
    fickpeng_e = st.number_input("Fickpeng Elin", value=5000)
    summa_rorliga = mat + fickpeng_d + fickpeng_e

with r2:
    pension = st.number_input("Pension", value=1000)
    isk = st.number_input("ISK", value=1300)
    buffert = st.number_input("Buffert", value=500)
    gemensamt = st.number_input("Gemensamt spar", value=3000)
    renovering = st.number_input("Renovering", value=1000)
    summa_spar = pension + isk + buffert + gemensamt + renovering

# --- SAMMANSTÄLLNING ---
st.divider()
st.header("📊 Resultat & Överskott")
totalt_ut = summa_fasta + summa_rorliga + summa_spar
netto_kvar = totalt_inkomster - totalt_ut

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Netto Inkomster", f"{totalt_inkomster:,.0f} kr")
col_m2.metric("Totala Utgifter (Inkl. Spar)", f"{totalt_ut:,.0f} kr")
col_m3.metric("Kvar att leva på", f"{netto_kvar:,.0f} kr")

if netto_kvar < 0:
    st.error("⚠️ Utgifterna överstiger inkomsterna!")
else:
    st.success("✅ Ekonomin går ihop med plus på sista raden.")
  
