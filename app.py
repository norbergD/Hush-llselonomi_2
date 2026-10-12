import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Hushållsekonomi", page_icon="💰", layout="wide")

# ==========================================
# 1. BERÄKNINGAR (Körs först för att visas överst)
# ==========================================

# Inkomster
brutto_david = 47500
skatt_pct = 34.0
netto_david = brutto_david * (1 - (skatt_pct / 100))

brutto_elin = 41500
netto_elin = brutto_elin * (1 - (skatt_pct / 100))

ovrig_inkomst = 0
totalt_inkomster = netto_david + netto_elin + ovrig_inkomst

# Huslån (skuld och ränta)
skuld_1 = 1162500
ranta_1 = 2.25
tot_lan_1 = ((skuld_1 * (ranta_1 / 100)) / 12) * 0.70

skuld_2 = 1162500
ranta_2 = 2.25
tot_lan_2 = ((skuld_2 * (ranta_2 / 100)) / 12) * 0.70

skuld_3 = 236598
ranta_3 = 1.70
tot_lan_3 = ((skuld_3 * (ranta_3 / 100)) / 12) * 0.70 + int((skuld_3 * 0.02) / 12)

summa_huslan = tot_lan_1 + tot_lan_2 + tot_lan_3

# Fasta utgifter
pellets = 2000
transport = 1500
billan = 4100
el_tibber = 0
el_ellevio = 0
bredband = 0
tv = 0
mobil = 0
vatten_sopor = 0
forskola = 0
ovriga_fasta = 0
a_kassa_fack_david = 400
a_kassa_fack_elin = 400
csn_david = 1250
csn_elin = 1250

summa_fasta = (summa_huslan + pellets + transport + billan + el_tibber + el_ellevio + 
               bredband + tv + mobil + vatten_sopor + forskola + ovriga_fasta + 
               a_kassa_fack_david + a_kassa_fack_elin + csn_david + csn_elin)

# Rörliga utgifter (inkl. Spotify, Xbox, Podme)
mat = 7000
fickpeng_d = 5000
fickpeng_e = 5000
spotify = 129
xbox = 149
podme = 99

summa_rorliga = mat + fickpeng_d + fickpeng_e + spotify + xbox + podme

# Sparande (Buffert, ISK, Gemensamt, Bil)
buffert_manad = 500
isk_manad = 1300
gemensamt_manad = 3000
bil_manad = 1000

summa_sparande = buffert_manad + isk_manad + gemensamt_manad + bil_manad

# Resultat
totalt_ut = summa_fasta + summa_rorliga
netto_kvar = totalt_inkomster - totalt_ut - summa_sparande


# ==========================================
# 2. RESULTAT & ÖVERSIKT (FÖRSTA SIDESÄTTNING)
# ==========================================
st.title("🏡 Hushållsekonomi & Bolånekalkyl")
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

# Buffertmål beräkning
buffert_mal = 120000
# (Hämtas från inmatningen längre ner, sätts som standard här för beräkning)
buffert_nuv_temp = 50000 
if buffert_manad > 0 and buffert_nuv_temp < buffert_mal:
    kvar_att_spara = buffert_mal - buffert_nuv_temp
    manader_kvar = kvar_att_spara / buffert_manad
    dagar_kvar = int(manader_kvar * 30.44)
    mal_datum = datetime.now() + timedelta(days=dagar_kvar)
    st.info(f"🎯 **Buffertmål (120 000 kr):** Beräknat nås den **{mal_datum.strftime('%Y-%m-%d')}** (~{manader_kvar:.1f} månader kvar med nuvarande sparande).")

st.divider()


# ==========================================
# 3. INMATNING & JUSTERINGAR
# ==========================================

# --- INKOMSTER ---
st.header("1. Inkomster (Netto)")
col1, col2 = st.columns(2)
with col1:
    brutto_david_in = st.number_input("Bruttolön David (kr)", value=47500, step=500)
    skatt_pct_in = st.slider("Beräknad skatt (%)", min_value=20.0, max_value=50.0, value=34.0, step=0.5)
with col2:
    brutto_elin_in = st.number_input("Bruttolön Elin (kr)", value=41500, step=500)

ovrig_inkomst_in = st.number_input("Övriga inkomster netto (kr)", value=0, step=500)


# --- HUSLÅN ---
st.header("2. Huslån & Bolån")
rant_extra = st.slider("Simulera ränteändring alla lån (%-enheter)", min_value=-2.0, max_value=5.0, value=0.0, step=0.25)

col_l1, col_l2, col_l3 = st.columns(3)
with col_l1:
    st.number_input("Skuld Lån 1 (Större)", value=1162500, step=10000, key="s1")
    st.number_input("Ränta Lån 1 (%)", value=2.25, step=0.05, key="r1")
with col_l2:
    st.number_input("Skuld Lån 2 (Större)", value=1162500, step=10000, key="s2")
    st.number_input("Ränta Lån 2 (%)", value=2.25, step=0.05, key="r2")
with col_l3:
    st.number_input("Skuld Lån 3 (Mindre)", value=236598, step=5000, key="s3")
    st.number_input("Ränta Lån 3 (%)", value=1.70, step=0.05, key="r3")


# --- FASTA UTGIFTER ---
st.header("3. Fasta Utgifter")
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.markdown("### Boende & Drift")
    st.number_input("Pellets", value=2000, step=100, key="pel")
    st.number_input("Transport", value=1500, step=100, key="tra")
    st.number_input("Billån", value=4100, step=100, key="bil_lan")
    st.number_input("El (Tibber)", value=0, step=100, key="tib")
    st.number_input("Elnät (Ellevio)", value=0, step=100, key="ell")
    st.number_input("Bredband", value=0, step=50, key="bred")
    st.number_input("TV", value=0, step=50, key="tvs")
    st.number_input("Mobilabonnemang", value=0, step=50, key="mob")
    st.number_input("Vatten / Sopor", value=0, step=50, key="vat")
    st.number_input("Förskola", value=0, step=100, key="fors")
    st.number_input("Övrigt fast", value=0, step=100, key="ovr_f")

with col_f2:
    st.markdown("### Personliga Fasta")
    st.number_input("A-kassa & Fack David", value=400, step=50, key="ak_d")
    st.number_input("A-kassa & Fack Elin", value=400, step=50, key="ak_e")
    st.number_input("CSN David", value=1250, step=50, key="csn_d")
    st.number_input("CSN Elin", value=1250, step=50, key="csn_e")


# --- RÖRLIGA UTGIFTER ---
st.header("4. Rörliga Utgifter")
col_r1, col_r2 = st.columns(2)
with col_r1:
    st.number_input("Mat & livsmedel", value=7000, step=100, key="mat_in")
    st.number_input("Fickpeng David", value=5000, step=100, key="fick_d")
    st.number_input("Fickpeng Elin", value=5000, step=100, key="fick_e")
with col_r2:
    st.number_input("Spotify", value=129, step=10, key="spo_in")
    st.number_input("Xbox", value=149, step=10, key="xbox_in")
    st.number_input("Podme", value=99, step=10, key="pod_in")


# --- SPARANDE & NUVARANDE SALDON ---
st.header("5. Sparande & Nuvarande Saldon")
col_s1, col_s2, col_s3, col_s4 = st.columns(4)

with col_s1:
    st.markdown("### 🛡️ Buffert")
    st.number_input("Nuvarande saldo", value=50000, step=1000, key="buf_nuv")
    st.number_input("Sparande/mån", value=500, step=100, key="buf_man")

with col_s2:
    st.markdown("### 📈 ISK")
    st.number_input("Nuvarande saldo", value=75000, step=1000, key="isk_nuv")
    st.number_input("Sparande/mån", value=1300, step=100, key="isk_man")

with col_s3:
    st.markdown("### 🤝 Gemensamt")
    st.number_input("Nuvarande saldo", value=15000, step=1000, key="gem_nuv")
    st.number_input("Sparande/mån", value=3000, step=100, key="gem_man")

with col_s4:
    st.markdown("### 🚗 Bilen")
    st.number_input("Nuvarande saldo", value=10000, step=1000, key="bil_nuv")
    st.number_input("Sparande/mån", value=1000, step=100, key="bil_man")
