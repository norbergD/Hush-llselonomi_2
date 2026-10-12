import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Hushållsekonomi", page_icon="💰", layout="wide")

st.title("🏡 Hushållsekonomi & Bolånekalkyl")

# ==========================================
# 1. BERÄKNINGAR (Körs först för att nå toppen)
# ==========================================

# Inkomster
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

# Huslån
rant_extra = st.slider("Simulera ränteändring alla lån (%-enheter)", min_value=-2.0, max_value=5.0, value=0.0, step=0.25)

skuld_1 = 1162500
ranta_1 = 2.25 + rant_extra
tot_lan_1 = ((skuld_1 * (ranta_1 / 100)) / 12) * 0.70

skuld_2 = 1162500
ranta_2 = 2.25 + rant_extra
tot_lan_2 = ((skuld_2 * (ranta_2 / 100)) / 12) * 0.70

skuld_3 = 236598
ranta_3 = 1.70 + rant_extra
amortering_3 = int((skuld_3 * 0.02) / 12)
tot_lan_3 = ((skuld_3 * (ranta_3 / 100)) / 12) * 0.70 + amortering_3

summa_huslan = tot_lan_1 + tot_lan_2 + tot_lan_3

# Fasta utgifter (inkl. nya poster och separerade personliga)
billan = 4100
pellets = 2000
transport = 1500
el_tibber = 0
el_ellevio = 0
bredband = 0
tv = 0
mobil = 0
vatten_sopor = 0
forskola = 0
ovriga_fasta = 0

# Personliga fasta
a_kassa_fack_david = 400
a_kassa_fack_elin = 400
csn_david = 1250
csn_elin = 1250

summa_fasta = (summa_huslan + billan + pellets + transport + el_tibber + el_ellevio + 
               bredband + tv + mobil + vatten_sopor + forskola + ovriga_fasta + 
               a_kassa_fack_david + a_kassa_fack_elin + csn_david + csn_elin)

# Rörliga utgifter
mat = 7000
fickpeng_d = 5000
fickpeng_e = 5000
summa_rorliga = mat + fickpeng_d + fickpeng_e

# Sparande & Mål
pension_manad = 1000
isk_manad = 1300
buffert_manad = 500
gemensamt_manad = 3000
renovering_manad = 1000

summa_sparande = pension_manad + isk_manad + buffert_manad + gemensamt_manad + renovering_manad

totalt_ut = summa_fasta + summa_rorliga
netto_kvar = totalt_inkomster - totalt_ut - summa_sparande

# ==========================================
# 2. RESULTAT & ÖVERSIKT (PLACERAD ÖVERST)
# ==========================================
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

st.divider()

# ==========================================
# 3. SPARANDE & MÅLDATUM
# ==========================================
st.header("🎯 Sparande & Mål")

col_s1, col_s2 = st.columns(2)

with col_s1:
    st.subheader("Buffert")
    buffert_nuvarande = st.number_input("Nuvarande saldo Buffert (kr)", value=50000, step=1000)
    buffert_mal = 120000
    st.write(f"Mål: **{buffert_mal:,.0f} kr** (Sparar {buffert_manad:,.0f} kr/mån)")
    
    if buffert_manad > 0 and buffert_nuvarande < buffert_mal:
        kvar_att_spara = buffert_mal - buffert_nuvarande
        manader_kvar = kvar_att_spara / buffert_manad
        dagar_kvar = int(manader_kvar * 30.44)
        mal_datum = datetime.now() + timedelta(days=dagar_kvar)
        st.info(f"📅 Beräknat måldatum för bufferten: **{mal_datum.strftime('%Y-%m-%d')}** (~{manader_kvar:.1f} månader)")
    elif buffert_nuvarande >= buffert_mal:
        st.success("🎉 Buffertmålet är uppnått!")

    st.subheader("Pension")
    pension_nuvarande = st.number_input("Nuvarande saldo Pension (kr)", value=100000, step=5000)
    st.write(f"Månatligt sparande: **{pension_manad:,.0f} kr/mån**")

with col_s2:
    st.subheader("ISK-sparande")
    isk_nuvarande = st.number_input("Nuvarande saldo ISK (kr)", value=75000, step=1000)
    st.write(f"Månatligt sparande: **{isk_manad:,.0f} kr/mån**")

    st.subheader("Övrigt sparande")
    gemensamt_nuv = st.number_input("Nuvarande saldo Gemensamt / Resor (kr)", value=15000, step=1000)
    renovering_nuv = st.number_input("Nuvarande saldo Renovering (kr)", value=20000, step=1000)
    st.write(f"Gemensamt: {gemensamt_manad} kr/mån | Renovering: {renovering_manad} kr/mån")

st.divider()

# ==========================================
# 4. INKOMSTER (INPUT)
# ==========================================
st.header("1. Inkomster (Netto)")
st.write(f"Netto David: **{netto_david:,.0f} kr** | Netto Elin: **{netto_elin:,.0f} kr** | Övrigt: **{ovrig_inkomst:,.0f} kr**")

# ==========================================
# 5. HUSLÅN
# ==========================================
st.header("2. Huslån & Bolån")
col_l1, col_l2, col_l3 = st.columns(3)

with col_l1:
    st.subheader("Lån 1 (Större)")
    st.write(f"Skuld: {skuld_1:,.0f} kr")
    st.write(f"Efter ränteavdrag: **{tot_lan_1:,.0f} kr/mån**")

with col_l2:
    st.subheader("Lån 2 (Större)")
    st.write(f"Skuld: {skuld_2:,.0f} kr")
    st.write(f"Efter ränteavdrag: **{tot_lan_2:,.0f} kr/mån**")

with col_l3:
    st.subheader("Lån 3 (Mindre)")
    st.write(f"Skuld: {skuld_3:,.0f} kr")
    st.write(f"Efter ränteavdrag: **{tot_lan_3:,.0f} kr/mån**")

# ==========================================
# 6. FASTA UTGIFTER
# ==========================================
st.header("3. Övriga Fasta Utgifter")
col_f1, col_f2 = st.columns(2)

with col_f1:
    st.markdown("### Boende & Drift")
    st.write(f"- Pellets: {pellets} kr")
    st.write(f"- Transport: {transport} kr")
    st.write(f"- Billån: {billan} kr")
    st.write(f"- El (Tibber/Ellevio): {el_tibber + el_ellevio} kr")
    st.write(f"- Bredband / TV / Mobil: {bredband + tv + mobil} kr")
    st.write(f"- Vatten / Sopor: {vatten_sopor} kr")

with col_f2:
    st.markdown("### Personliga & Övriga Fasta")
    st.write(f"- A-kassa & Fack David: {a_kassa_fack_david} kr")
    st.write(f"- A-kassa & Fack Elin: {a_kassa_fack_elin} kr")
    st.write(f"- CSN David: {csn_david} kr")
    st.write(f"- CSN Elin: {csn_elin} kr")
    st.write(f"- Förskola: {forskola} kr")

# ==========================================
# 7. RÖRLIGA UTGIFTER
# ==========================================
st.header("4. Rörliga Utgifter")
col_r1, col_r2 = st.columns(2)
with col_r1:
    st.write(f"- Mat & livsmedel: {mat} kr")
    st.write(f"- Fickpeng David: {fickpeng_d} kr")
    st.write(f"- Fickpeng Elin: {fickpeng_e} kr")
