import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection # Nuovo motore

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Junior Club Terni", layout="wide", initial_sidebar_state="expanded")

# --- 2. OPZIONE NUCLEARE ANTI-TRADUTTORE E CSS (Invariato) ---
st.components.v1.html("""
    <script>
        window.parent.document.documentElement.lang = 'it';
        window.parent.document.documentElement.setAttribute('translate', 'no');
        var meta = window.parent.document.createElement('meta');
        meta.name = "google";
        meta.content = "notranslate";
        window.parent.document.getElementsByTagName('head')[0].appendChild(meta);
    </script>
""", height=0, width=0)

st.markdown("""
    <style>
    /* Pulizia Interfaccia */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} 
    .stAppDeployButton {display: none;}
    
    /* Sfondo principale neutro elegante */
    .stApp { background-color: #f1f5f9; font-family: 'Inter', 'Helvetica Neue', sans-serif; }
    
    /* SIDEBAR ARANCIONE JUNIOR CLUB */
    [data-testid="stSidebar"] { 
        background-color: #FF6501 !important; 
        border-right: none; 
        box-shadow: 4px 0 20px rgba(0,0,0,0.08);
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; font-weight: 600; }
    .stRadio div[role="radiogroup"] label span { background-color: transparent !important; }
    
    /* Titoli Principali Ultra-Definiti */
    .titolo-app { color: #0f172a; font-size: 42px; font-weight: 900; margin-bottom: 0px; letter-spacing: -1px; text-transform: uppercase;}
    .sottotitolo { color: #64748b; font-size: 16px; font-weight: 500; margin-bottom: 30px; margin-top: 5px; }
    
    /* LA CARD DEL FORM */
    [data-testid="stForm"] {
        background-color: #ffffff;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.08);
        padding: 40px 50px;
        margin-bottom: 2rem;
    }
    
    /* Campi di testo: altissima leggibilità */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] { 
        border-radius: 8px !important; 
        border: 1px solid #cbd5e1 !important; 
        padding: 12px 16px !important; 
        background-color: #f8fafc !important; 
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #0f172a !important; 
        transition: all 0.2s ease;
    }
    .stTextInput input:focus, .stNumberInput input:focus { 
        border-color: #FF6501 !important; 
        background-color: #ffffff !important; 
        box-shadow: 0 0 0 3px rgba(255, 101, 1, 0.15) !important; 
    }
    
    /* Etichette (Labels) Minimal e Chiare */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-weight: 800 !important;
        color: #475569 !important;
        font-size: 12px !important;
        margin-bottom: 6px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Intestazioni di sezione SUPER ELEGANTI */
    .header-sezione {
        color: #0f172a;
        font-weight: 900;
        font-size: 18px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 10px;
        margin-top: 25px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
    }
    .header-sezione span { color: #FF6501; margin-right: 10px; font-size: 22px; }
    
    /* BOTTONE GIGANTE SCURO (Effetto Lusso) */
    button[kind="primary"] {
        background-color: #0f172a !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.2rem 2rem !important;
        font-size: 18px !important;
        font-weight: 900 !important;
        letter-spacing: 1.5px !important;
        box-shadow: 0 10px 20px -5px rgba(15, 23, 42, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        text-transform: uppercase;
    }
    button[kind="primary"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 25px -5px rgba(15, 23, 42, 0.6) !important;
        background-color: #FF6501 !important;
    }

    /* MAGIA STAMPA */
    @media print {
        body * { visibility: hidden; }
        .ricevuta-stampabile, .ricevuta-stampabile * { visibility: visible; }
        .ricevuta-stampabile { position: absolute; left: 0; top: 0; margin: 0 !important; box-shadow: none !important; width: 100%; }
        .stButton, .stAlert { display: none !important; }
    }
    
    /* Anagrafica Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 30px; border-bottom: 2px solid #e2e8f0; }
    .stTabs [data-baseweb="tab"] { height: 50px; font-size: 16px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;}
    .stTabs [aria-selected="true"] { color: #FF6501 !important; border-bottom: 4px solid #FF6501 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div translate="no" class="notranslate">', unsafe_allow_html=True)

# --- 3. DATABASE (ORA GOOGLE SHEETS) ---
# Creiamo la connessione
conn_gs = st.connection("gsheets", type=GSheetsConnection)

def get_soci():
    # Legge i dati dal foglio "soci". ttl=0 serve per avere i dati sempre aggiornati
    return conn_gs.read(worksheet="soci", ttl=0)

def aggiungi_socio_singolo(nome, nascita, indirizzo, genitore, cf):
    df_attuale = get_soci()
    nuova_riga = pd.DataFrame([{
        "nome_atleta": nome.upper(),
        "luogo_data_nascita": nascita.upper(),
        "indirizzo": indirizzo.upper(),
        "nome_genitore": genitore.upper(),
        "codice_fiscale_genitore": cf.upper()
    }])
    # Unisce il vecchio database con il nuovo nome
    df_finale = pd.concat([df_attuale, nuova_riga], ignore_index=True)
    # Aggiorna il foglio Google
    conn_gs.update(worksheet="soci", data=df_finale)

# Carichiamo i dati iniziali
df_soci = get_soci()

# --- 4. MENU LATERALE ---
st.sidebar.markdown("<h2 translate='no' class='notranslate' style='font-weight: 900; font-size: 28px; text-align: center; margin-bottom: 40px; letter-spacing: -1px; color: #ffffff;'>JUNIOR CLUB TERNI</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("SEZIONI:", ["📝 Emissione Ricevuta", "👥 Anagrafica Clienti", "📊 Storico Pagamenti"])

# --- 5. SEZIONE EMISSIONE RICEVUTA ---
if menu == "📝 Emissione Ricevuta":
    st.markdown("<div class='titolo-app'>EMISSIONE RICEVUTA</div>", unsafe_allow_html=True)
    st.markdown("<div class='sottotitolo'>Modulo ufficiale <span translate='no' class='notranslate'>JUNIOR CLUB TERNI</span>.</div>", unsafe_allow_html=True)
    
    if df_soci.empty:
        st.warning("L'archivio è vuoto. Vai in 'Anagrafica Clienti' per aggiungere un iscritto.")
    else:
        col_nome = 'nome_atleta' if 'nome_atleta' in df_soci.columns else df_soci.columns[0]
        
        st.markdown("""
            <div style='background-color: #ffffff; border-radius: 12px; padding: 25px; box-shadow: 0 4px 15px -1px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 25px;'>
                <div style='font-size: 13px; font-weight: 900; color: #475569; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px;'>🔍 CERCA ALLIEVO IN ARCHIVIO</div>
        """, unsafe_allow_html=True)
        
        atleta_selezionato = st.selectbox("", df_soci[col_nome].tolist(), label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
        dati_atleta = df_soci[df_soci[col_nome] == atleta_selezionato].iloc[0]
        genitore = dati_atleta.get('nome_genitore', '')
        cf_gen = dati_atleta.get('codice_fiscale_genitore', '')
        nascita = dati_atleta.get('luogo_data_nascita', '')
        indirizzo = dati_atleta.get('indirizzo', '')
        default_pagante = genitore if pd.notna(genitore) and str(genitore).strip() != "" else dati_atleta['nome_atleta']

        with st.form("form_compilazione"):
            
            st.markdown("<div class='header-sezione'><span>💶</span> DETTAGLI RICEVUTA E IMPORTI</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            num_ric = c1.text_input("Numero Ricevuta *", placeholder="es. 01")
            data_ric = c2.text_input("Data Emissione *", value=datetime.now().strftime('%d/%m/%Y'))
            importo = c3.number_input("Importo Cifre (€) *", min_value=0.0, step=5.0, value=50.0)
            
            c4, c5 = st.columns([1, 1])
            importo_lettere = c4.text_input("Importo in Lettere *", placeholder="es. CINQUANTA/00")
            causale = c5.text_input("Causale *", value="GINNASTICA / Mese in corso")
            
            st.markdown("<div class='header-sezione'><span>👤</span> INTESTATARIO RICEVUTA (GENITORE/PAGANTE)</div>", unsafe_allow_html=True)
            c6, c7 = st.columns(2)
            chi_paga = c6.text_input("Nome Pagante *", value=default_pagante)
            cf_pagante = c7.text_input("Codice Fiscale Pagante *", value=cf_gen)
            
            st.markdown("<div class='header-sezione'><span>🏃</span> DATI ALLIEVO E FIRMA</div>", unsafe_allow_html=True)
            c8, c9, c10 = st.columns(3)
            nome_allievo = c8.text_input("Nome Atleta *", value=dati_atleta['nome_atleta'])
            nascita_allievo = c9.text_input("Luogo/Data di Nascita *", value=nascita)
            indirizzo_allievo = c10.text_input("Indirizzo di Residenza *", value=indirizzo)
            
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            incaricato_firma = st.selectbox("Firma Autorizzata", [
                "Nessuno (Lascia spazio vuoto per la penna)", 
                "Sara Cesaroni", 
                "Elisa Tradardi", 
                "Valerio Cesaroni", 
                "Federico Sciaboletta", 
                "Eleonora Bartoli"
            ])
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            submit = st.form_submit_button("✨ GENERA MODULO RICEVUTA", type="primary")

        if submit:
            campi_mancanti = []
            if not str(num_ric).strip(): campi_mancanti.append("Numero Ricevuta")
            if not str(data_ric).strip(): campi_mancanti.append("Data Emissione")
            if importo <= 0: campi_mancanti.append("Importo in Cifre")
            if not str(importo_lettere).strip(): campi_mancanti.append("Importo in Lettere")
            if not str(causale).strip(): campi_mancanti.append("Causale")
            if not str(chi_paga).strip(): campi_mancanti.append("Nome Pagante")
            if not str(cf_pagante).strip(): campi_mancanti.append("Codice Fiscale Pagante")
            if not str(nome_allievo).strip(): campi_mancanti.append("Nome Atleta")
            if not str(nascita_allievo).strip(): campi_mancanti.append("Luogo/Data di Nascita")
            if not str(indirizzo_allievo).strip(): campi_mancanti.append("Indirizzo di Residenza")
            
            if campi_mancanti:
                st.error(f"🚫 **ATTENZIONE: Modulo Incompleto!** Compila i seguenti campi: **{', '.join(campi_mancanti)}**.")
            else:
                testo_firma = "" if incaricato_firma.startswith("Nessuno") else incaricato_firma
                
                st.success("✅ Documento generato con successo. Scorri in basso e clicca il bottone scuro per stampare.")
                
                html_ricevuta = f"""
<div class="ricevuta-stampabile" style="background: white; border: 2px solid #FF6501; padding: 40px; max-width: 900px; margin: 30px auto; font-family: Arial, sans-serif; color: #FF6501; box-sizing: border-box; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
<div style="display: flex; justify-content: space-between; align-items: flex-start;">
<div style="width: 55%; font-size: 10px; font-weight: bold; color: black; line-height: 1.4;">
DENOMINAZIONE o RAGIONE SOCIALE e SEDE LEGALE della ditta ovvero COGNOME e NOME,<br>
RESIDENZA, C.F. se persona fisica<br>
<span translate="no" class="notranslate" style="color: #FF6501; font-size: 17px; font-weight: 900; display: block; margin-top: 8px;">JUNIOR CLUB TERNI - Terni - C.F. 1234567890</span>
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
<span style="flex-grow: 1; color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{chi_paga}</span>
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
<span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px; text-align: right;">{nome_allievo}</span>
</div>
<div style="display: flex; justify-content: space-between; border-bottom: 1px solid #FF6501; padding-bottom: 4px; padding-top: 4px;">
<span style="font-size: 12px; font-weight: bold;">LUOGO/DATA DI NASCITA</span>
<span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px; text-align: right;">{nascita_allievo}</span>
</div>
<div style="display: flex; justify-content: space-between; padding-top: 4px;">
<span style="font-size: 12px; font-weight: bold;">INDIRIZZO</span>
<span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px; text-align: right;">{indirizzo_allievo}</span>
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
<div style="font-size: 10px; font-weight: bold; color: black; margin-top: 40px; border-top: 1.5px solid #FF6501; padding-top: 8px;">
* Somma non soggetta ad IVA ai sensi del quarto comma dell'Art. 4 del D.P.R. 633/72 e successive modifiche.
</div>
</div>
"""
                st.markdown(html_ricevuta, unsafe_allow_html=True)
                
                # Tasto Stampa
                st.components.v1.html("""
                    <script> function lanciaStampa() { window.parent.print(); } </script>
                    <div style="text-align: center; margin-top: 30px;">
                        <button onclick="lanciaStampa()" style="background-color: #0f172a; color: white; border: none; padding: 18px 50px; font-size: 20px; border-radius: 12px; cursor: pointer; font-weight: 900; box-shadow: 0 10px 20px -5px rgba(15, 23, 42, 0.4); text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;">
                            🖨️ STAMPA / SALVA PDF
                        </button>
                    </div>
                """, height=120)

# --- 6. SEZIONE ANAGRAFICA ---
elif menu == "👥 Anagrafica Clienti":
    st.markdown("<div class='titolo-app'>ANAGRAFICA CLIENTI</div>", unsafe_allow_html=True)
    st.markdown("<div class='sottotitolo'>Gestione del database atleti del <span translate='no' class='notranslate'>JUNIOR CLUB TERNI</span>.</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["➕ NUOVO ALLIEVO", "📋 ELENCO ISCRITTI", "📂 IMPORTA FILE CSV"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("aggiungi_singolo"):
            st.markdown("<div class='header-sezione'><span>📋</span> DATI ANAGRAFICI</div>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            nuovo_nome = col_a.text_input("Nome e Cognome Allievo *")
            nuovo_nascita = col_b.text_input("Luogo e Data di Nascita")
            nuovo_indirizzo = st.text_input("Indirizzo di Residenza")
            
            st.markdown("<div class='header-sezione'><span>👤</span> DATI GENITORE (PER DETRAZIONE)</div>", unsafe_allow_html=True)
            col_c, col_d = st.columns(2)
            nuovo_genitore = col_c.text_input("Nome Genitore / Pagante")
            nuovo_cf = col_d.text_input("Codice Fiscale")
            
            st.markdown("<br>", unsafe_allow_html=True)
            salva_nuovo = st.form_submit_button("SALVA NEL DATABASE", type="primary")
            
            if salva_nuovo:
                if nuovo_nome.strip() == "":
                    st.error("Il nome dell'allievo è obbligatorio.")
                else:
                    aggiungi_socio_singolo(nuovo_nome, nuovo_nascita, nuovo_indirizzo, nuovo_genitore, nuovo_cf)
                    st.success("Allievo aggiunto con successo su Google Sheets!")
                    st.rerun()

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_soci, use_container_width=True, height=600, hide_index=True)

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("Trascina qui il file CSV se devi fare un aggiornamento massivo del database.")
        file_caricato = st.file_uploader("", type="csv", label_visibility="collapsed")
        
        if file_caricato:
            df_nuovo = pd.read_csv(file_caricato, sep=';')
            df_nuovo.columns = df_nuovo.columns.astype(str).str.lower().str.strip()
            df_nuovo.rename(columns={'nome atleta': 'nome_atleta', 'luogo/data di nascita': 'luogo_data_nascita', 'nome genitore x detrazione': 'nome_genitore', 'cod. fiscale genitore': 'codice_fiscale_genitore'}, inplace=True)
            if st.button("SOVRASCRIVI DATABASE CON FILE CSV", type="primary"):
                # Aggiorna direttamente il foglio Google sovrascrivendo tutto
                conn_gs.update(worksheet="soci", data=df_nuovo)
                st.success("Database su Google Sheets aggiornato!")
                st.rerun()

# --- 7. SEZIONE STORICO ---
else:
    st.markdown("<div class='titolo-app'>STORICO PAGAMENTI</div>", unsafe_allow_html=True)
    st.info("Funzione in fase di sviluppo. Arriverà presto!")

st.markdown('</div>', unsafe_allow_html=True)