import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Hushållsekonomi", page_icon="💰", layout="wide")

st.title("🏡 Hushållsekonomi & Bolånekalkyl")

# ==========================================
# 1. HJÄLPFUNKTION FÖR INMATNINGAR & SESSION STATE
# ==========================================
# Hämtar inskrivna värden från formulären nedan för att räkna ut resultatet överst

brutto_david = st.session_state.get("b_dav", 0.0)
brutto_elin = st.session_state.get("b_el", 0.0)
skatt_pct = st.session_state.get("sk_pct", 30.0)
ovrig_inkomst = st.session_state.get("ovr_ink", 0.0)

netto_david = brutto_david * (1 - (skatt_pct / 100))
netto_elin = brutto_elin * (1 - (skatt_pct / 100))
totalt_inkomster = netto_david + netto_elin + ovrig_inkomst

# Lån
rant_extra = st.session_state.get("r_ext", 0.0)
skuld_1 = st.session_state.get("s1", 0.0)
ranta_1 = st.session_state.get("ra1", 0.0) + rant_extra
tot_lan_1 = ((skuld_1 * (ranta_1 / 100)) / 12) * 0.70 if skuld_1 > 0 else 0.0

skuld_2 = st.session_state.get("s2", 0.0)
ranta_2 = st.session_state.get("ra2", 0.0) + rant_extra
tot_lan_2 = ((skuld_2 * (ranta_2 / 100)) / 12) * 0.70 if skuld_2 > 0 else 0.0

skuld_3 = st.session_state.get("s3", 0.0)
ranta_3 = st.session_state.get("ra3", 0.0) + rant_extra
amortering_3 = st.session_state.get("amor3", 0.0)
tot_lan_3 = (((skuld_3 * (ranta_3 / 100)) / 12) * 0.70 + amortering_3) if skuld_3 > 0 else 0.0

summa_huslan = tot_lan_1 + tot_lan_2 + tot_lan_3

# Fasta Utgifter
pellets = st.session_state.get("pel", 0.0)
transport = st.session_state.get("tra", 0.0)
billan = st.session_state.get("bil_lan", 0.0)
el_tibber = st.session_state.get("tib", 0.0)
el_ellevio = st.session_state.get("ell", 0.0)
bredband = st.session_state.get("bred", 0.0)
tv = st.session_state.get("tvs", 0.0)
mobil = st.session_state.get("mob", 0.0)
vatten_sopor = st.session_state.get("vat", 0.0)
forskola = st.session_state.get("fors", 0.0)
ovriga_fasta = st.session_state.get("ovr_f", 0.0)

a_kassa_fack_david = st.session_state.get("ak_d", 0.0)
a_kassa_fack_elin = st.session_state.get("ak_e", 0.0)
csn_david = st.session_state.get("csn_d", 0.0)
csn_elin = st.session_state.get("csn_e", 0.0)

summa_fasta = (summa_huslan + pellets + transport + billan + el_tibber + el_ellevio + 
               bredband + tv + mobil + vatten_sopor + forskola + ovriga_fasta + 
               a_kassa_fack_david + a_kassa_fack_elin + csn_david + csn_elin)

# Rörliga Utgifter
mat = st.session_state.get("mat_in", 0.0)
fickpeng_d = st.session_state.get("fick_d", 0.0)
fickpeng_e = st.session_state.get("fick_e", 0.0)
spotify = st.session_state.get("spo_in", 0.0)
xbox = st.session_state.get("xbox_in", 0.0)
podme = st.session_state.get("pod_in", 0.0)

summa_rorliga = mat + fickpeng_d + fickpeng_e + spotify + xbox + podme

# Sparande
buffert_nuv = st.session_state.get("buf_nuv", 0.0)
buffert_manad = st.session_state.get("buf_man", 0.0)

isk_d_nuv = st.session_state.get("isk_d_nuv", 0.0)
isk_d_man = st.session_state.get("isk_d_man", 0.0)

isk_e_nuv = st.session_state.get("isk_e_nuv", 0.0)
isk_e_man = st.session_state.get("isk_e_man", 0.0)

gemensamt_nuv = st.session_state.get("gem_nuv", 0.0)
gemensamt_manad = st.session_state.get("gem_man", 0.0)

bil_nuv = st.session_state.get("bil_nuv", 0.0)
bil_manad = st.session_state.get("bil_man", 0.0)

renov_nuv = st.session_state.get("ren_nuv", 0.0)
renov_manad = st.session_state.get("ren_man", 0.0)

pension_d_manad = st.session_state.get("p_d_man", 0.0)
pension_e_manad = st.session_state.get("p_e_man", 0.0)

# Summeringar Sparande
totalt_isk_nuv = isk_d_nuv + isk_e_nuv
totalt_isk_manad = isk_d_man + isk_e_man
totalt_pension_manad = pension_d_manad + pension_e_manad

huvudsakligt_spar_manad = buffert_manad + gemensamt_manad + totalt_isk_manad
summa_sparande = huvudsakligt_spar_manad + bil_manad + renov_manad + totalt_pension_manad

totalt_ut = summa_fasta + summa_rorliga
netto_kvar = totalt_inkomster - totalt_ut - summa_sparande


# ==========================================
# 2. RESULTAT & ÖVERSIKT (ÖVERST I APPEN)
# ==========================================
st.header("📊 Resultat & Överskott")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Netto Inkomster", f"{totalt_inkomster:,.0f} kr")
col_m2.metric("Utgifter (exkl. spar)", f"{totalt_ut:,.0f} kr")
col_m3.metric("Totalt Sparande", f"{summa_sparande:,.0f} kr/mån")
col_m4.metric("Kvar att leva på", f"{netto_kvar:,.0f} kr")

st.info(f"💡 **Specifikation sparande:** Buffert, Gemensamt & ISK totalt: **{huvudsakligt_spar_manad:,.0f} kr/mån** (Totalt ISK: {totalt_isk_manad:,.0f} kr/mån | Nuvarande totalt ISK-saldo: {totalt_isk_nuv:,.0f} kr).")

if netto_kvar < 0 and totalt_inkomster > 0:
    st.error("⚠️ Utgifterna och sparandet överstiger inkomsterna!")
elif totalt_inkomster > 0:
    st.success("✅ Ekonomin går ihop med plus på sista raden.")

# Buffertmål beräkning
buffert_mal = 120000.0
if buffert_manad > 0 and buffert_nuv < buffert_mal:
    kvar_att_spara = buffert_mal - buffert_nuv
    manader_kvar = kvar_att_spara / buffert_manad
    dagar_kvar = int(manader_kvar * 30.44)
    mal_datum = datetime.now() + timedelta(days=dagar_kvar)
    st.markdown(f"🎯 **Buffertmål (120 000 kr):** Beräknat nås den **{mal_datum.strftime('%Y-%m-%d')}** (~{manader_kvar:.1f} månader kvar).")
elif buffert_nuv >= buffert_mal and buffert_mal > 0:
    st.markdown("🎉 Buffertmålet på 120 000 kr är nått!")

st.markdown("---")


# ==========================================
# 3. FORMULÄR & INMATNINGSPOSTER (TOMMA VÄRDEN)
# ==========================================

# --- 1. INKOMSTER ---
st.header("1. Inkomster (Netto)")
col1, col2 = st.columns(2)
with col1:
    st.number_input("Bruttolön David (kr)", value=0.0, step=500.0, key="b_dav")
    st.slider("Beräknad skatt (%)", min_value=20.0, max_value=50.0, value=30.0, step=0.5, key="sk_pct")
with col2:
    st.number_input("Bruttolön Elin (kr)", value=0.0, step=500.0, key="b_el")

st.number_input("Övriga inkomster netto (kr)", value=0.0, step=500.0, key="ovr_ink")


# --- 2. HUSLÅN ---
st.header("2. Huslån & Bolån")
st.slider("Simulera ränteändring alla lån (%-enheter)", min_value=-2.0, max_value=5.0, value=0.0, step=0.25, key="r_ext")

col_l1, col_l2, col_l3 = st.columns(3)
with col_l1:
    st.subheader("Lån 1 (Större)")
    st.number_input("Skuld Lån 1 (kr)", value=0.0, step=10000.0, key="s1")
    st.number_input("Ränta Lån 1 (%)", value=0.0, step=0.05, key="ra1")
    st.write(f"Kostnad efter ränteavdrag: **{tot_lan_1:,.0f} kr/mån**")

with col_l2:
    st.subheader("Lån 2 (Större)")
    st.number_input("Skuld Lån 2 (kr)", value=0.0, step=10000.0, key="s2")
    st.number_input("Ränta Lån 2 (%)", value=0.0, step=0.05, key="ra2")
    st.write(f"Kostnad efter ränteavdrag: **{tot_lan_2:,.0f} kr/mån**")

with col_l3:
    st.subheader("Lån 3 (Mindre)")
    st.number_input("Skuld Lån 3 (kr)", value=0.0, step=5000.0, key="s3")
    st.number_input("Ränta Lån 3 (%)", value=0.0, step=0.05, key="ra3")
    st.number_input("Amortering Lån 3 (kr/mån)", value=0.0, step=100.0, key="amor3")
    st.write(f"Kostnad efter ränteavdrag: **{tot_lan_3:,.0f} kr/mån**")


# --- 3. FASTA UTGIFTER ---
st.header("3. Fasta Utgifter")
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.markdown("### Boende & Drift")
    st.number_input("Pellets", value=0.0, step=100.0, key="pel")
    st.number_input("Transport", value=0.0, step=100.0, key="tra")
    st.number_input("Billån", value=0.0, step=100.0, key="bil_lan")
    st.number_input("El (Tibber)", value=0.0, step=100.0, key="tib")
    st.number_input("Elnät (Ellevio)", value=0.0, step=100.0, key="ell")
    st.number_input("Bredband", value=0.0, step=50.0, key="bred")
    st.number_input("TV", value=0.0, step=50.0, key="tvs")
    st.number_input("Mobilabonnemang", value=0.0, step=50.0, key="mob")
    st.number_input("Vatten / Sopor", value=0.0, step=50.0, key="vat")
    st.number_input("Förskola", value=0.0, step=100.0, key="fors")
    st.number_input("Övrigt fast", value=0.0, step=100.0, key="ovr_f")

with col_f2:
    st.markdown("### Personliga Fasta")
    st.number_input("A-kassa & Fack David", value=0.0, step=50.0, key="ak_d")
    st.number_input("A-kassa & Fack Elin", value=0.0, step=50.0, key="ak_e")
    st.number_input("CSN David", value=0.0, step=50.0, key="csn_d")
    st.number_input("CSN Elin", value=0.0, step=50.0, key="csn_e")


# --- 4. RÖRLIGA UTGIFTER ---
st.header("4. Rörliga Utgifter")
col_r1, col_r2 = st.columns(2)
with col_r1:
    st.number_input("Mat & livsmedel", value=0.0, step=100.0, key="mat_in")
    st.number_input("Fickpeng David", value=0.0, step=100.0, key="fick_d")
    st.number_input("Fickpeng Elin", value=0.0, step=100.0, key="fick_e")
with col_r2:
    st.number_input("Spotify", value=0.0, step=10.0, key="spo_in")
    st.number_input("Xbox", value=0.0, step=10.0, key="xbox_in")
    st.number_input("Podme", value=0.0, step=10.0, key="pod_in")


# --- 5. SPARANDE & SALDON ---
st.header("5. Sparande & Nuvarande Saldon")

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown("### 🛡️ Buffert")
    st.number_input("Nuvarande saldo Buffert", value=0.0, step=1000.0, key="buf_nuv")
    st.number_input("Spar/mån Buffert", value=0.0, step=100.0, key="buf_man")

with col_s2:
    st.markdown("### 📈 ISK David")
    st.number_input("Nuvarande saldo ISK David", value=0.0, step=1000.0, key="isk_d_nuv")
    st.number_input("Spar/mån ISK David", value=0.0, step=100.0, key="isk_d_man")

with col_s3:
    st.markdown("### 📈 ISK Elin")
    st.number_input("Nuvarande saldo ISK Elin", value=0.0, step=1000.0, key="isk_e_nuv")
    st.number_input("Spar/mån ISK Elin", value=0.0, step=100.0, key="isk_e_man")

col_s4, col_s5, col_s6 = st.columns(3)
with col_s4:
    st.markdown("### 🤝 Gemensamt")
    st.number_input("Nuvarande saldo Gemensamt", value=0.0, step=1000.0, key="gem_nuv")
    st.number_input("Spar/mån Gemensamt", value=0.0, step=100.0, key="gem_man")

with col_s5:
    st.markdown("### 🚗 Bilen")
    st.number_input("Nuvarande saldo Bilen", value=0.0, step=1000.0, key="bil_nuv")
    st.number_input("Spar/mån Bilen", value=0.0, step=100.0, key="bil_man")

with col_s6:
    st.markdown("### 🛠️ Renovering")
    st.number_input("Nuvarande saldo Renovering", value=0.0, step=1000.0, key="ren_nuv")
    st.number_input("Spar/mån Renovering", value=0.0, step=100.0, key="ren_man")

st.markdown("### 👵 Pension (Månadssparande)")
col_p1, col_p2 = st.columns(2)
with col_p1:
    st.number_input("Pension David / mån", value=0.0, step=100.0, key="p_d_man")
with col_p2:
    st.number_input("Pension Elin / mån", value=0.0, step=100.0, key="p_e_man")
