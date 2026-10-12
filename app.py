import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Hushållsekonomi", page_icon="💰", layout="wide")

st.title("🏡 Hushållsekonomi & Bolånekalkyl")

# ==========================================
# 1. INMATNING (Här fyller ni i era siffror)
# ==========================================

# --- INKOMSTER ---
st.header("1. Inkomster (Netto)")
col1, col2 = st.columns(2)
with col1:
    brutto_david = st.number_input("Bruttolön David (kr)", value=47500, step=500)
    skatt_pct = st.slider("Beräknad skatt (%)", min_value=20.0, max_value=50.0, value=34.0, step=0.5)
    netto_david = brutto_david * (1 - (skatt_pct / 100))
with col2:
    brutto_elin = st.number_input("Bruttolön Elin (kr)", value=41500, step=500)
    netto_elin = brutto_elin * (1 - (skatt_pct / 100))

ovrig_inkomst = st.number_input("Övriga inkomster netto (kr)", value=0, step=500)
totalt_inkomster = netto_david + netto_elin + ovrig_inkomst

# --- HUSLÅN ---
st.header("2. Huslån & Bolån")
rant_extra = st.slider("Simulera ränteändring alla lån (%-enheter)", min_value=-2.0, max_value=5.0, value=0.0, step=0.25)

col_l1, col_l2, col_l3 = st.columns(3)
with col_l1:
    skuld_1 = st.number_input("Skuld Lån 1 (Större)", value=1162500, step=10000)
    ranta_1 = st.number_input("Ränta Lån 1 (%)", value=2.25, step=0.05) + rant_extra
    tot_lan_1 = ((skuld_1 * (ranta_1 / 100)) / 12) * 0.70
with col_l2:
    skuld_2 = st.number_input("Skuld Lån 2 (Större)", value=1162500, step=10000)
    ranta_2 = st.number_input("Ränta Lån 2 (%)", value=2.25, step=0.05) + rant_extra
    tot_lan_2 = ((skuld_2 * (ranta_2 / 100)) / 12) * 0.70
with col_l3:
    skuld_3 = st.number_input("Skuld Lån 3 (Mindre)", value=236598, step=5000)
    ranta_3 = st.number_input("Ränta Lån 3 (%)", value=1.70, step=0.05) + rant_extra
    amortering_3 = st.number_input("Amortering Lån 3 (kr/mån)", value=int((skuld_3 * 0.02) / 12), step=100)
    tot_lan_3 = ((skuld_3 * (ranta_3 / 100)) / 12) * 0.70 + amortering_3

summa_huslan = tot_lan_1 + tot_lan_2 + tot_lan_3

# --- FASTA UTGIFTER ---
st.header("3. Fasta Utgifter")
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.markdown("### Boende & Drift")
    pellets = st.number_input("Pellets", value=2000, step=100)
    transport = st.number_input("Transport", value=1500, step=100)
    billan = st.number_input("Billån", value=4100, step=100)
    el_tibber = st.number_input("El (Tibber)", value=0, step=100)
    el_ellevio = st.number_input("Elnät (Ellevio)", value=0, step=100)
    bredband = st.number_input("Bredband", value=0, step=50)
    tv = st.number_input("TV", value=0, step=50)
    mobil = st.number_input("Mobilabonnemang", value=0, step=50)
    vatten_sopor = st.number_input("Vatten / Sopor", value=0, step=50)
    forskola = st.number_input("Förskola", value=0, step=100)
    ovriga_fasta = st.number_input("Övrigt fast", value=0, step=100)

with col_f2:
    st.markdown("### Personliga Fasta")
    a_kassa_fack_david = st.number_input("A-kassa & Fack David", value=400, step=50)
    a_kassa_fack_elin = st.number_input("A-kassa & Fack Elin", value=400, step=50)
    csn_david = st.number_input("CSN David", value=1250, step=50)
    csn_elin = st.number_input("CSN Elin", value=1250, step=50)

summa_fasta = (summa_huslan + pellets + transport + billan + el_tibber + el_ellevio + 
               bredband + tv + mobil + vatten_sopor + forskola + ovriga_fasta + 
               a_kassa_fack_david + a_kassa_fack_elin + csn_david + csn_elin)

# --- RÖRLIGA UTGIFTER ---
st.header("4. Rörliga Utgifter")
col_r1, col_r2 = st.columns(2)
with col_r1:
    mat = st.number_input("Mat & livsmedel", value=7000, step=100)
    fickpeng_d = st.number_input("Fickpeng David", value=5000, step=100)
    fickpeng_e = st.number_input("Fickpeng Elin", value=5000, step=100)
summa_rorliga = mat + fickpeng_d + fickpeng_e

# --- SPARANDE & MÅL (KOMPAKT) ---
st.header("5. Sparande & Nuvarande Saldon")
col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown("### Buffert (Mål: 120 000 kr)")
    buffert_nuv = st.number_input("Nuvarande saldo (Buffert)", value=50000, step=1000)
    buffert_manad = st.number_input("Sparande/mån (Buffert)", value=500, step=100)

with col_s2:
    st.markdown("### ISK & Pension")
    isk_nuv = st.number_input("Nuvarande saldo (ISK)", value=75000, step=1000)
    isk_manad = st.number_input("Sparande/mån (ISK)", value=1300, step=100)
    pension_nuv = st.number_input("Nuvarande saldo (Pension)", value=100000, step=5000)
    pension_manad = st.number_input("Sparande/mån (Pension)", value=1000, step=100)

with col_s3:
    st.markdown("### Övrigt Sparande")
    gemensamt_nuv = st.number_input("Nuvarande saldo (Gemensamt/Resor)", value=15000, step=1000)
    gemensamt_manad = st.number_input("Sparande/mån (Gemensamt)", value=3000, step=100)
    renovering_nuv = st.number_input("Nuvarande saldo (Renovering)", value=20000, step=1000)
    renovering_manad = st.number_input("Sparande/mån (Renovering)", value=1000, step=100)

summa_sparande = buffert_manad + isk_manad + pension_manad + gemensamt_manad + renovering_manad

# Totala utgifter inklusive sparande för resultatberäkning
totalt_ut = summa_fasta + summa_rorliga
netto_kvar = totalt_inkomster - totalt_ut - summa_sparande


# ==========================================
# 2. RESULTAT & ÖVERSIKT (LIGGER HÖGST UPP)
# ==========================================
st.divider()
st.header("📊 Resultat & Överskott")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Netto Inkomster", f"{totalt_inkomster:,.0f} kr")
col_m2.metric("Utgifter (exkl. spar)", f"{totalt_ut:,.0f} kr")
col_m3.metric("Totalt Sparande", f"{summa_sparande:,.0f} kr/mån")
col_m4.metric("Kvar att leva på", f"{netto_kvar:,.0f} kr")

if netto_kvar < 0:
    st.error("⚠️ Utgifterna och sparandet överstiger inkomsterna!")
else:
    st.success("✅ Ekonomin går ihop med plus på sista raden.")

# Kompakt måldatum-beräkning för buffert
buffert_mal = 120000
if buffert_manad > 0 and buffert_nuv < buffert_mal:
    kvar_att_spara = buffert_mal - buffert_nuv
    manader_kvar = kvar_att_spara / buffert_manad
    dagar_kvar = int(manader_kvar * 30.44)
    mal_datum = datetime.now() + timedelta(days=dagar_kvar)
    st.info(f"🎯 **Buffertmål (120 000 kr):** Beräknat nås den **{mal_datum.strftime('%Y-%m-%d')}** (~{manader_kvar:.1f} månader kvar med nuvarande sparande).")
elif buffert_nuv >= buffert_mal:
    st.success("🎉 Buffertmålet på 120 000 kr är nått!")
