import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Hushållsekonomi", page_icon="💰", layout="wide")

st.title("🏡 Hushållsekonomi & Bolånekalkyl")

# ==========================================
# 1. INMATNING & BERÄKNINGAR (Körs i bakgrunden för resultat)
# ==========================================

# Inkomster
brutto_david = st.number_input("Bruttolön David (kr)", value=47500, step=500, key="b_dav")
skatt_pct = st.slider("Beräknad skatt (%)", min_value=20.0, max_value=50.0, value=34.0, step=0.5, key="sk_pct")
netto_david = brutto_david * (1 - (skatt_pct / 100))

brutto_elin = st.number_input("Bruttolön Elin (kr)", value=41500, step=500, key="b_el")
netto_elin = brutto_elin * (1 - (skatt_pct / 100))

ovrig_inkomst = st.number_input("Övriga inkomster netto (kr)", value=0, step=500, key="ovr_ink")
totalt_inkomster = netto_david + netto_elin + ovrig_inkomst

# Huslån
rant_extra = st.slider("Simulera ränteändring alla lån (%-enheter)", min_value=-2.0, max_value=5.0, value=0.0, step=0.25, key="r_ext")

skuld_1 = st.number_input("Skuld Lån 1 (Större)", value=1162500, step=10000, key="s1")
ranta_1 = st.number_input("Ränta Lån 1 (%)", value=2.25, step=0.05, key="ra1") + rant_extra
tot_lan_1 = ((skuld_1 * (ranta_1 / 100)) / 12) * 0.70

skuld_2 = st.number_input("Skuld Lån 2 (Större)", value=1162500, step=10000, key="s2")
ranta_2 = st.number_input("Ränta Lån 2 (%)", value=2.25, step=0.05, key="ra2") + rant_extra
tot_lan_2 = ((skuld_2 * (ranta_2 / 100)) / 12) * 0.70

skuld_3 = st.number_input("Skuld Lån 3 (Mindre)", value=236598, step=5000, key="s3")
ranta_3 = st.number_input("Ränta Lån 3 (%)", value=1.70, step=0.05, key="ra3") + rant_extra
amortering_3 = st.number_input("Amortering Lån 3 (kr/mån)", value=int((skuld_3 * 0.02) / 12), step=100, key="amor3")
tot_lan_3 = ((skuld_3 * (ranta_3 / 100)) / 12) * 0.70 + amortering_3

summa_huslan = tot_lan_1 + tot_lan_2 + tot_lan_3

# Fasta utgifter
pellets = st.number_input("Pellets", value=2000, step=100, key="pel")
transport = st.number_input("Transport", value=1500, step=100, key="tra")
billan = st.number_input("Billån", value=4100, step=100, key="bil_lan")
el_tibber = st.number_input("El (Tibber)", value=0, step=100, key="tib")
el_ellevio = st.number_input("Elnät (Ellevio)", value=0, step=100, key="ell")
bredband = st.number_input("Bredband", value=0, step=50, key="bred")
tv = st.number_input("TV", value=0, step=50, key="tvs")
mobil = st.number_input("Mobilabonnemang", value=0, step=50, key="mob")
vatten_sopor = st.number_input("Vatten / Sopor", value=0, step=50, key="vat")
forskola = st.number_input("Förskola", value=0, step=100, key="fors")
ovriga_fasta = st.number_input("Övrigt fast", value=0, step=100, key="ovr_f")

a_kassa_fack_david = st.number_input("A-kassa & Fack David", value=400, step=50, key="ak_d")
a_kassa_fack_elin = st.number_input("A-kassa & Fack Elin", value=400, step=50, key="ak_e")
csn_david = st.number_input("CSN David", value=1250, step=50, key="csn_d")
csn_elin = st.number_input("CSN Elin", value=1250, step=50, key="csn_e")

summa_fasta = (summa_huslan + pellets + transport + billan + el_tibber + el_ellevio + 
               bredband + tv + mobil + vatten_sopor + forskola + ovriga_fasta + 
               a_kassa_fack_david + a_kassa_fack_elin + csn_david + csn_elin)

# Rörliga utgifter
mat = st.number_input("Mat & livsmedel", value=7000, step=100, key="mat_in")
fickpeng_d = st.number_input("Fickpeng David", value=5000, step=100, key="fick_d")
fickpeng_e = st.number_input("Fickpeng Elin", value=5000, step=100, key="fick_e")
spotify = st.number_input("Spotify", value=129, step=10, key="spo_in")
xbox = st.number_input("Xbox", value=149, step=10, key="xbox_in")
podme = st.number_input("Podme", value=99, step=10, key="pod_in")

summa_rorliga = mat + fickpeng_d + fickpeng_e + spotify + xbox + podme

# Sparande & Saldon
buffert_nuv = st.number_input("Nuvarande saldo Buffert", value=50000, step=1000, key="buf_nuv")
buffert_manad = st.number_input("Spar/mån Buffert", value=500, step=100, key="buf_man")

isk_d_nuv = st.number_input("Nuvarande saldo ISK David", value=40000, step=1000, key="isk_d_nuv")
isk_d_man = st.number_input("Spar/mån ISK David", value=800, step=100, key="isk_d_man")

isk_e_nuv = st.number_input("Nuvarande saldo ISK Elin", value=35000, step=1000, key="isk_e_nuv")
isk_e_man = st.number_input("Spar/mån ISK Elin", value=500, step=100, key="isk_e_man")

gemensamt_nuv = st.number_input("Nuvarande saldo Gemensamt", value=15000, step=1000, key="gem_nuv")
gemensamt_manad = st.number_input("Spar/mån Gemensamt", value=3000, step=100, key="gem_man")

bil_nuv = st.number_input("Nuvarande saldo Bilen", value=10000, step=1000, key="bil_nuv")
bil_manad = st.number_input("Spar/mån Bilen", value=1000, step=100, key="bil_man")

renov_nuv = st.number_input("Nuvarande saldo Renovering", value=20000, step=1000, key="ren_nuv")
renov_manad = st.number_input("Spar/mån Renovering", value=1000, step=100, key="ren_man")

pension_d_manad = st.number_input("Pension David / mån", value=500, step=100, key="p_d_man")
pension_e_manad = st.number_input("Pension Elin / mån", value=500, step=100, key="p_e_man")

# Summeringar
totalt_isk_nuv = isk_d_nuv + isk_e_nuv
totalt_isk_manad = isk_d_man + isk_e_man
totalt_pension_manad = pension_d_manad + pension_e_manad

# Totalt sparande för Buffert, Gemensamt och ISK tillsammans
huvudsakligt_spar_manad = buffert_manad + gemensamt_manad + totalt_isk_manad

# Totalt sparande totalt sett
summa_sparande = huvudsakligt_spar_manad + bil_manad + renov_manad + totalt_pension_manad

totalt_ut = summa_fasta + summa_rorliga
netto_kvar = totalt_inkomster - totalt_ut - summa_sparande


# ==========================================
# 2. RESULTAT & ÖVERSIKT (LIGGER HÖGST UPP)
# ==========================================
st.markdown("---")
st.header("📊 Resultat & Överskott")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Netto Inkomster", f"{totalt_inkomster:,.0f} kr")
col_m2.metric("Utgifter (exkl. spar)", f"{totalt_ut:,.0f} kr")
col_m3.metric("Totalt Sparande", f"{summa_sparande:,.0f} kr/mån")
col_m4.metric("Kvar att leva på", f"{netto_kvar:,.0f} kr")

# Extra sparande-specifikation i resultatdelen
st.info(info=f"💡 **Specifikation sparande:** Buffert, Gemensamt & ISK totalt: **{huvudsakligt_spar_manad:,.0f} kr/mån** (ISK totalt: {totalt_isk_manad:,.0f} kr/mån).")

if netto_kvar < 0:
    st.error("⚠️ Utgifterna och sparandet överstiger inkomsterna!")
else:
    st.success("✅ Ekonomin går ihop med plus på sista raden.")

# Buffertmål beräkning
buffert_mal = 120000
if buffert_manad > 0 and buffert_nuv < buffert_mal:
    kvar_att_spara = buffert_mal - buffert_nuv
    manader_kvar = kvar_att_spara / buffert_manad
    dagar_kvar = int(manader_kvar * 30.44)
    mal_datum = datetime.now() + timedelta(days=dagar_kvar)
    st.markdown(f"🎯 **Buffertmål (120 000 kr):** Beräknat nås den **{mal_datum.strftime('%Y-%m-%d')}** (~{manader_kvar:.1f} månader kvar).")
elif buffert_nuv >= buffert_mal:
    st.markdown("🎉 Buffertmålet på 120 000 kr är nått!")

st.markdown("---")
