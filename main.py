import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Junior Club Terni", layout="wide", initial_sidebar_state="expanded")

# --- NOME DEL TUO DATABASE (Qui ho messo quello che avevi selezionato nello screenshot) ---
NOME_DATABASE = "dati_circolo.db"

# --- 2. OPZIONE NUCLEARE ANTI-TRADUTTORE E CSS ---
st.components.v1.html("""
    <script>
        window.parent.document.documentElement.lang = 'it';
        window.parent.document.documentElement.setAttribute('translate', 'no');
    </script>
""", height=0, width=0)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} 
    .stAppDeployButton {display: none;}
    .stApp { background-color: #f1f5f9; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #FF6501 !important; border-right: none; box-shadow: 4px 0 20px rgba(0,0,0,0.08); }
    [data-testid="stSidebar"] * { color: #ffffff !important; font-weight: 600; }
    .titolo-app { color: #0f172a; font-size: 42px; font-weight: 900; margin-bottom: 0px; text-transform: uppercase;}
    .sottotitolo { color: #64748b; font-size: 16px; font-weight: 500; margin-bottom: 30px; margin-top: 5px; }
    [data-testid="stForm"] { background-color: #ffffff; border-radius: 20px; border: 1px solid #e2e8f0; padding: 40px; margin-bottom: 2rem;}
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] { border-radius: 8px !important; border: 1px solid #cbd5e1 !important; background-color: #f8fafc !important; font-size: 16px !important; font-weight: 600 !important; }
    .stTextInput label, .stNumberInput label, .stSelectbox label { font-weight: 800 !important; color: #475569 !important; font-size: 12px !important; text-transform: uppercase !important; }
    .header-sezione { color: #0f172a; font-weight: 900; font-size: 18px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; margin-top: 25px; margin-bottom: 25px; display: flex; align-items: center; }
    .header-sezione span { color: #FF6501; margin-right: 10px; font-size: 22px; }
    button[kind="primary"] { background-color: #0f172a !important; color: white !important; border-radius: 12px !important; padding: 1.2rem 2rem !important; font-size: 18px !important; font-weight: 900 !important; width: 100% !important; }
    @media print {
        body * { visibility: hidden; }
        .ricevuta-stampabile, .ricevuta-stampabile * { visibility: visible; }
        .ricevuta-stampabile { position: absolute; left: 0; top: 0; margin: 0 !important; width: 100%; }
        .stButton, .stAlert { display: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE: LOCALE (SQLITE ORIGINALE) ---
def init_db():
    conn = sqlite3.connect(NOME_DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS soci
                 (nome_atleta TEXT, luogo_data_nascita TEXT, indirizzo TEXT, 
                  nome_genitore TEXT, codice_fiscale_genitore TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_soci():
    conn = sqlite3.connect(NOME_DATABASE)
    try:
        df = pd.read_sql_query("SELECT * FROM soci", conn)
    except:
        df = pd.DataFrame(columns=['nome_atleta', 'luogo_data_nascita', 'indirizzo', 'nome_genitore', 'codice_fiscale_genitore'])
    conn.close()
    return df

df_soci = get_soci()

def aggiungi_socio_singolo(nome, nascita, indirizzo, genitore, cf):
    try:
        conn = sqlite3.connect(NOME_DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO soci (nome_atleta, luogo_data_nascita, indirizzo, nome_genitore, codice_fiscale_genitore) VALUES (?, ?, ?, ?, ?)", 
                  (nome.upper(), nascita.upper(), indirizzo.upper(), genitore.upper(), cf.upper()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Errore di salvataggio: {e}")
        return False

# --- 4. MENU LATERALE ---
st.sidebar.markdown("<h2 style='font-weight: 900; font-size: 28px; text-align: center; margin-bottom: 40px;'>JUNIOR CLUB TERNI</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("SEZIONI:", ["📝 Emissione Ricevuta", "👥 Anagrafica Clienti", "📊 Storico Pagamenti"])

# --- 5. SEZIONE EMISSIONE RICEVUTA ---
if menu == "📝 Emissione Ricevuta":
    st.markdown("<div class='titolo-app'>EMISSIONE RICEVUTA</div>", unsafe_allow_html=True)
    st.markdown("<div class='sottotitolo'>Modulo ufficiale JUNIOR CLUB TERNI.</div>", unsafe_allow_html=True)
    
    if df_soci.empty:
        st.warning("L'archivio è vuoto. Vai in 'Anagrafica Clienti' per aggiungere un iscritto.")
    else:
        # Trova la colonna giusta qualsiasi nome abbia
        col_nome = 'nome_atleta' if 'nome_atleta' in df_soci.columns else df_soci.columns[0]
        
        st.markdown("<div style='background-color: #fff; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 25px;'><div style='font-weight: 900; margin-bottom: 12px;'>🔍 CERCA ALLIEVO IN ARCHIVIO</div>", unsafe_allow_html=True)
        atleta_selezionato = st.selectbox("", df_soci[col_nome].tolist(), label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
        dati_atleta = df_soci[df_soci[col_nome] == atleta_selezionato].iloc[0]
        
        # Estrazione sicura dei dati
        genitore = dati_atleta.get('nome_genitore', '')
        cf_gen = dati_atleta.get('codice_fiscale_genitore', '')
        nascita = dati_atleta.get('luogo_data_nascita', '')
        indirizzo = dati_atleta.get('indirizzo', '')
        
        # IL FIX È QUI: Usa col_nome invece di ['nome_atleta']
        default_pagante = genitore if pd.notna(genitore) and str(genitore).strip() != "" else dati_atleta[col_nome]

        with st.form("form_compilazione"):
            st.markdown("<div class='header-sezione'><span>💶</span> DETTAGLI RICEVUTA E IMPORTI</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            num_ric = c1.text_input("Numero Ricevuta *", "01")
            data_ric = c2.text_input("Data Emissione *", datetime.now().strftime('%d/%m/%Y'))
            importo = c3.number_input("Importo Cifre (€) *", min_value=0.0, step=5.0, value=50.0)
            
            c4, c5 = st.columns([1, 1])
            importo_lettere = c4.text_input("Importo in Lettere *", "CINQUANTA/00")
            causale = c5.text_input("Causale *", "GINNASTICA / Mese in corso")
            
            st.markdown("<div class='header-sezione'><span>👤</span> INTESTATARIO RICEVUTA (GENITORE/PAGANTE)</div>", unsafe_allow_html=True)
            c6, c7 = st.columns(2)
            chi_paga = c6.text_input("Nome Pagante *", value=default_pagante)
            cf_pagante = c7.text_input("Codice Fiscale Pagante *", value=cf_gen)
            
            st.markdown("<div class='header-sezione'><span>🏃</span> DATI ALLIEVO E FIRMA</div>", unsafe_allow_html=True)
            c8, c9, c10 = st.columns(3)
            
            # IL FIX È QUI: Usa col_nome
            nome_allievo = c8.text_input("Nome Atleta *", value=dati_atleta[col_nome])
            
            nascita_allievo = c9.text_input("Luogo/Data di Nascita *", value=nascita)
            indirizzo_allievo = c10.text_input("Indirizzo di Residenza *", value=indirizzo)
            
            incaricato_firma = st.selectbox("Firma Autorizzata", ["Nessuno", "Sara Cesaroni", "Elisa Tradardi", "Valerio Cesaroni", "Federico Sciaboletta", "Eleonora Bartoli"])
            submit = st.form_submit_button("✨ GENERA MODULO RICEVUTA", type="primary")

        if submit:
            st.success("✅ Documento generato con successo. Scorri in basso e clicca il bottone scuro per stampare.")
            testo_firma = "" if incaricato_firma == "Nessuno" else incaricato_firma
            
            html_ricevuta = f"""
<div class="ricevuta-stampabile" style="background: white; border: 2px solid #FF6501; padding: 40px; max-width: 900px; margin: 30px auto; font-family: Arial, sans-serif; color: #FF6501;">
<div style="display: flex; justify-content: space-between; align-items: flex-start;">
<div style="width: 55%; font-size: 10px; font-weight: bold; color: black; line-height: 1.4;">
DENOMINAZIONE o RAGIONE SOCIALE e SEDE LEGALE della ditta ovvero COGNOME e NOME,<br>
RESIDENZA, C.F. se persona fisica<br>
<span style="color: #FF6501; font-size: 17px; font-weight: 900; display: block; margin-top: 8px;">JUNIOR CLUB TERNI - Terni - C.F. 1234567890</span>
</div>
<div style="width: 40%; text-align: right;">
<div style="font-size: 24px; font-weight: 900;">RICEVUTA <span style="font-size: 14px;">n.</span> <span style="color: black; font-family: 'Courier New', monospace; border-bottom: 2px solid #FF6501; padding: 0 20px;">{num_ric}</span></div>
<div style="display: flex; align-items: center; justify-content: flex-end; margin-top: 15px;">
<div style="font-size: 32px; font-weight: bold; margin-right: 15px;">€</div>
<div style="border: 2px solid #FF6501; width: 220px; height: 45px; display: flex; background: white;">
<div style="flex-grow: 1; text-align: center; font-size: 22px; color: black; font-family: 'Courier New', monospace; font-weight: bold; line-height: 41px;">{importo:.2f}</div>
<div style="width: 45px; background-color: #fff4ed; border-left: 2px solid #FF6501;"></div>
</div>
</div>
</div>
</div>
<div style="font-size: 22px; font-weight: 900; margin-top: 40px; margin-bottom: 15px;">RICEVIAMO</div>
<div style="display: flex; align-items: flex-end; border-bottom: 1.5px solid #FF6501; margin-bottom: 20px; padding-bottom: 4px;">
<span style="font-weight: bold; font-size: 15px; margin-right: 10px;">da</span>
<span style="flex-grow: 1; color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px;">{chi_paga}</span>
<span style="font-weight: bold; font-size: 15px; margin-left: 10px; margin-right: 10px;">(CODICE FISCALE)</span>
<span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px;">{cf_pagante}</span>
</div>
<div style="display: flex; align-items: center; border-bottom: 1.5px solid #FF6501; margin-bottom: 20px; padding-bottom: 4px;">
<span style="font-weight: bold; font-size: 15px; margin-right: 10px;">la somma* di €</span>
<div style="flex-grow: 1; background: #fff4ed; border: 1px solid #FF6501; height: 32px; line-height: 32px; padding-left: 10px; color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px; margin-right: 10px;">{importo_lettere}</div>
<span style="font-weight: bold; font-size: 15px;">(IN LETTERE)</span>
</div>
<div style="display: flex; align-items: flex-end; border-bottom: 1.5px solid #FF6501; margin-bottom: 30px; padding-bottom: 4px;">
<span style="font-weight: bold; font-size: 15px; margin-right: 10px;">per l'attività sportiva</span>
<span style="flex-grow: 1; color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px;">{causale}</span>
</div>
<div style="display: flex; justify-content: space-between; align-items: stretch; margin-bottom: 60px;">
<div style="width: 70%; border: 1.5px solid #FF6501; display: flex; background: white;">
<div style="width: 20px; background: #fff4ed; border-right: 1.5px solid #FF6501; flex-shrink: 0;"></div>
<div style="flex-grow: 1; padding: 15px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="display: flex; justify-content: space-between; border-bottom: 1px solid #FF6501; padding-bottom: 4px;">
<span style="font-size: 12px; font-weight: bold;">COGNOME E NOME</span>
<span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{nome_allievo}</span>
</div>
<div style="display: flex; justify-content: space-between; border-bottom: 1px solid #FF6501; padding-bottom: 4px; padding-top: 4px;">
<span style="font-size: 12px; font-weight: bold;">LUOGO/DATA DI NASCITA</span>
<span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{nascita_allievo}</span>
</div>
<div style="display: flex; justify-content: space-between; padding-top: 4px;">
<span style="font-size: 12px; font-weight: bold;">INDIRIZZO</span>
<span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{indirizzo_allievo}</span>
</div>
</div>
</div>
<div style="width: 120px; border: 1.5px solid #FF6501; text-align: center; padding: 15px 5px; font-size: 11px; font-weight: bold; display: flex; flex-direction: column; justify-content: center; background: white;">
Soggetta<br>ad Imposta<br>vigente<br><br><span style="font-size: 9px;">APPLICARE LA<br>MARCA SUL RETRO</span>
</div>
</div>
<div style="display: flex; justify-content: space-between; align-items: flex-end;">
<div style="font-weight: bold; font-size: 15px;">Data <span style="color: black; font-family: 'Courier New', monospace; border-bottom: 1.5px solid #FF6501; padding: 0 20px;">{data_ric}</span></div>
<div style="text-align: center; font-weight: bold; font-size: 15px; width: 250px;">
Firma dell'incaricato<br><br>
<div style="border-bottom: 1px solid #FF6501; width: 100%; margin: 5px 0;"></div>
<span style="color: black; font-size: 15px;">{testo_firma}</span>
</div>
</div>
</div>
"""
            st.markdown(html_ricevuta, unsafe_allow_html=True)
            st.components.v1.html("""<script> function lanciaStampa() { window.parent.print(); } </script><div style="text-align: center; margin-top: 30px;"><button onclick="lanciaStampa()" style="background-color: #0f172a; color: white; border: none; padding: 18px 50px; font-size: 20px; border-radius: 12px; cursor: pointer; font-weight: 900; box-shadow: 0 10px 20px -5px rgba(15, 23, 42, 0.4);">🖨️ STAMPA / SALVA PDF</button></div>""", height=120)

# --- 6. SEZIONE ANAGRAFICA ---
elif menu == "👥 Anagrafica Clienti":
    st.markdown("<div class='titolo-app'>ANAGRAFICA CLIENTI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["➕ NUOVO ALLIEVO", "📋 ELENCO ISCRITTI"])
    
    with tab1:
        with st.form("aggiungi_singolo"):
            st.markdown("<div class='header-sezione'><span>📋</span> DATI ANAGRAFICI</div>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            nuovo_nome = col_a.text_input("Nome e Cognome Allievo *")
            nuovo_nascita = col_b.text_input("Luogo e Data di Nascita")
            nuovo_indirizzo = st.text_input("Indirizzo di Residenza")
            
            st.markdown("<div class='header-sezione'><span>👤</span> DATI GENITORE</div>", unsafe_allow_html=True)
            col_c, col_d = st.columns(2)
            nuovo_genitore = col_c.text_input("Nome Genitore / Pagante")
            nuovo_cf = col_d.text_input("Codice Fiscale")
            
            salva_nuovo = st.form_submit_button("SALVA NEL DATABASE", type="primary")
            
            if salva_nuovo:
                if nuovo_nome.strip() == "":
                    st.error("Il nome dell'allievo è obbligatorio.")
                else:
                    if aggiungi_socio_singolo(nuovo_nome, nuovo_nascita, nuovo_indirizzo, nuovo_genitore, nuovo_cf):
                        st.success("Allievo aggiunto con successo!")
                        st.rerun()

    with tab2:
        st.dataframe(df_soci, use_container_width=True, height=600, hide_index=True)

else:
    st.markdown("<div class='titolo-app'>STORICO PAGAMENTI</div>", unsafe_allow_html=True)
    st.info("Funzione in fase di sviluppo. Arriverà presto!")

st.markdown('</div>', unsafe_allow_html=True)