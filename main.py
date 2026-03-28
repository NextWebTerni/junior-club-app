import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
from fpdf import FPDF

# --- 1. CONFIGURAZIONE PAGINA E FONT ---
st.set_page_config(page_title="Junior Club Terni", layout="wide", initial_sidebar_state="expanded")
NOME_DATABASE = "dati_circolo.db" 

# --- BLOCCO ANTI-TRADUTTORE GLOBALE ---
st.components.v1.html("""
    <script>
        window.parent.document.documentElement.lang = 'it';
        window.parent.document.documentElement.setAttribute('translate', 'no');
        window.parent.document.documentElement.className += ' notranslate';
    </script>
""", height=0, width=0)

# --- 2. IL DESIGN "PREMIUM SOFTWARE" CORRETTO ---
st.markdown("""
<style>
/* Pulizia Globale */
#MainMenu {visibility: hidden;} footer {visibility: hidden;} .stAppDeployButton {display: none;}

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* Sfondo Globale */
.stApp { 
    background-color: #F3F6F9 !important; 
    font-family: 'Inter', -apple-system, sans-serif !important; 
}

/* === LARGHEZZA PERFETTA DELLO SCHERMO === */
[data-testid="block-container"] {
    max-width: 1200px !important;
    padding-top: 3rem !important;
    padding-bottom: 5rem !important;
}

/* === SIDEBAR PREMIUM === */
[data-testid="stSidebar"] { 
    background: linear-gradient(180deg, #FF6501 0%, #E65A00 100%) !important; 
    border-right: none !important; 
    box-shadow: 5px 0 40px rgba(0, 0, 0, 0.08);
}

.sidebar-title {
    color: #FFFFFF; font-weight: 900; font-size: 28px; text-align: center; 
    letter-spacing: -1px; margin-top: 20px; margin-bottom: 50px; text-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* === FIX MENU A PILLOLE SIDEBAR === */
[data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] { 
    flex-direction: column !important; background-color: transparent !important; gap: 8px; padding: 0 10px; display: flex !important;
}
[data-testid="stSidebar"] .stRadio label {
    background-color: rgba(255, 255, 255, 0.08) !important; border: 1px solid rgba(255, 255, 255, 0.05) !important; border-radius: 14px !important; padding: 16px 20px !important; cursor: pointer; transition: all 0.3s ease;
}
[data-testid="stSidebar"] .stRadio label:hover { background-color: rgba(255, 255, 255, 0.15) !important; transform: translateY(-2px); }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label > div:first-child { display: none !important; }
[data-testid="stSidebar"] .stRadio label:has(input:checked) { background-color: #FFFFFF !important; box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important; transform: translateX(4px); }
[data-testid="stSidebar"] .stRadio label p { color: #FFFFFF !important; font-size: 16px !important; font-weight: 600 !important; margin: 0 !important; }
[data-testid="stSidebar"] .stRadio label:has(input:checked) p { color: #FF6501 !important; font-weight: 800 !important; }

/* === INTERRUTTORE CENTRALE === */
.main div[data-testid="stRadio"] > div[role="radiogroup"] {
    flex-direction: row !important;
    background-color: #E2E8F0 !important;
    padding: 6px !important;
    border-radius: 16px !important;
    display: inline-flex !important;
    margin-bottom: 30px !important;
}
.main div[data-testid="stRadio"] label {
    background-color: transparent !important;
    padding: 12px 24px !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    border: none !important;
}
.main div[data-testid="stRadio"] label:has(input:checked) {
    background-color: #FFFFFF !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08) !important;
}
.main div[data-testid="stRadio"] label p { color: #64748B !important; font-weight: 700 !important; font-size: 15px !important; }
.main div[data-testid="stRadio"] label:has(input:checked) p { color: #1E293B !important; font-weight: 800 !important; }
.main div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child { display: none !important; }

/* === HEADER APP === */
.titolo-app { color: #1E293B; font-size: 42px; font-weight: 900; letter-spacing: -1.5px; margin-bottom: 0px; }
.sottotitolo { color: #64748B; font-size: 18px; font-weight: 500; margin-bottom: 30px; margin-top: 5px; }

/* === CONTAINER E CARD === */
[data-testid="stForm"] {
    background-color: #FFFFFF !important; border-radius: 24px !important; border: 1px solid rgba(226, 232, 240, 0.8) !important;
    box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.05), 0 0 10px rgba(15, 23, 42, 0.01) !important; padding: 50px !important; margin-bottom: 2rem !important;
}

/* === CAMPI DI TESTO EFFETTO SCAVATO === */
.stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox div[data-baseweb="select"] { 
    background-color: #F8FAFC !important; border: 1px solid #E2E8F0 !important; border-radius: 12px !important; padding: 16px 20px !important; font-size: 16px !important; font-weight: 600 !important; color: #1E293B !important; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important; transition: all 0.25s ease !important;
}
.stSelectbox div[data-baseweb="select"] * { color: #1E293B !important; font-weight: 600 !important; font-size: 16px !important; }
.stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, .stSelectbox div[data-baseweb="select"]:focus-within { 
    border-color: #FF6501 !important; background-color: #FFFFFF !important; box-shadow: 0 0 0 4px rgba(255, 101, 1, 0.1), 0 4px 10px rgba(0,0,0,0.05) !important; transform: translateY(-1px);
}

.stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #64748B !important; font-size: 12px !important; font-weight: 800 !important; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px !important;
}

.header-sezione { color: #0F172A; font-weight: 800; font-size: 18px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 40px; margin-bottom: 25px; display: flex; align-items: center; border-bottom: 2px solid #F1F5F9; padding-bottom: 12px; }
.header-sezione span { background: rgba(255, 101, 1, 0.1); color: #FF6501; padding: 8px 12px; border-radius: 10px; margin-right: 15px; font-size: 20px; }

/* === BOTTONE GLOW === */
button[kind="primary"] { background: linear-gradient(135deg, #FF6501 0%, #F97316 100%) !important; color: white !important; border: none !important; border-radius: 16px !important; padding: 1.4rem 2rem !important; font-size: 18px !important; font-weight: 900 !important; letter-spacing: 1.5px !important; box-shadow: 0 10px 30px -5px rgba(255, 101, 1, 0.5), 0 0 15px rgba(255, 101, 1, 0.3) !important; transition: all 0.3s ease !important; width: 100% !important; text-transform: uppercase; }
button[kind="primary"]:hover { transform: translateY(-4px) scale(1.01) !important; box-shadow: 0 20px 40px -10px rgba(255, 101, 1, 0.6), 0 0 20px rgba(255, 101, 1, 0.4) !important; }

/* Stampa */
@media print {
    body * { visibility: hidden; background: white; }
    .ricevuta-stampabile, .ricevuta-stampabile * { visibility: visible; }
    .ricevuta-stampabile { position: absolute; left: 0; top: 0; margin: 0 !important; width: 100%; border: none !important;}
    .stButton, .stAlert, iframe, .stDownloadButton { display: none !important; }
}
</style>
""", unsafe_allow_html=True)

# --- 3. DATABASE ---
def init_db():
    conn = sqlite3.connect(NOME_DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS soci (nome_atleta TEXT, luogo_data_nascita TEXT, indirizzo TEXT, nome_genitore TEXT, codice_fiscale_genitore TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS contatori_v2 (tipo TEXT PRIMARY KEY, numero INTEGER)''')
    c.execute("INSERT OR IGNORE INTO contatori_v2 (tipo, numero) VALUES ('POS', 0)")
    c.execute("INSERT OR IGNORE INTO contatori_v2 (tipo, numero) VALUES ('CONTANTI', 0)")
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

def get_prossimo_numero(tipo_ricevuta):
    conn = sqlite3.connect(NOME_DATABASE)
    c = conn.cursor()
    c.execute("SELECT numero FROM contatori_v2 WHERE tipo=?", (tipo_ricevuta,))
    res = c.fetchone()
    conn.close()
    if res:
        return res[0] + 1
    return 1

def salva_numero_ricevuta(tipo_ricevuta, numero):
    conn = sqlite3.connect(NOME_DATABASE)
    c = conn.cursor()
    c.execute("UPDATE contatori_v2 SET numero=? WHERE tipo=?", (numero, tipo_ricevuta))
    conn.commit()
    conn.close()

def aggiungi_socio_singolo(nome, nascita, indirizzo, genitore, cf):
    try:
        conn = sqlite3.connect(NOME_DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO soci VALUES (?, ?, ?, ?, ?)", (nome.upper(), nascita.upper(), indirizzo.upper(), genitore.upper(), cf.upper()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Errore: {e}")
        return False

df_soci = get_soci()

# --- 4. MENU LATERALE ---
st.sidebar.markdown("<div translate='no' class='notranslate sidebar-title'>JUNIOR CLUB TERNI</div>", unsafe_allow_html=True)
menu = st.sidebar.radio("Navigazione", ["📝 Emissione Ricevuta", "👥 Anagrafica Clienti", "📊 Storico Pagamenti"], label_visibility="collapsed")

# --- 5. SEZIONE EMISSIONE RICEVUTA ---
if menu == "📝 Emissione Ricevuta":
    st.markdown("<div translate='no' class='titolo-app notranslate'>Emissione Ricevuta</div><div translate='no' class='sottotitolo notranslate'>Modulo Ufficiale Gestionale Junior Club.</div>", unsafe_allow_html=True)
    
    tipo_ricevuta = st.radio("Seleziona Modello", ["💳 RICEVUTA SPORTIVA (POS)", "💵 RICEVUTA GENERICA (CONTANTI)"], horizontal=True, label_visibility="collapsed")
    
    # =========================================================================
    # A) MODELLO: RICEVUTA SPORTIVA (POS)
    # =========================================================================
    if tipo_ricevuta == "💳 RICEVUTA SPORTIVA (POS)":
        tipo_contatore = "POS"
        if df_soci.empty:
            st.warning("L'archivio è vuoto. Vai in 'Anagrafica Clienti' per aggiungere un iscritto.")
        else:
            col_nome = 'nome_atleta' if 'nome_atleta' in df_soci.columns else df_soci.columns[0]
            
            st.markdown("<div translate='no' class='notranslate' style='margin-bottom: 8px;'><span style='font-size: 14px; font-weight: 800; color: #475569; text-transform: uppercase; letter-spacing: 0.5px;'>🔍 Cerca Allievo in Archivio</span></div>", unsafe_allow_html=True)
            lista_allievi = ["-- SELEZIONA UN ALLIEVO --"] + df_soci[col_nome].tolist()
            atleta_selezionato = st.selectbox("", lista_allievi, label_visibility="collapsed")
            st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
            
            if atleta_selezionato == "-- SELEZIONA UN ALLIEVO --":
                nome_form, genitore, cf_gen, nascita, indirizzo, default_pagante = "", "", "", "", "", ""
            else:
                dati_atleta = df_soci[df_soci[col_nome] == atleta_selezionato].iloc[0]
                nome_form = dati_atleta[col_nome]
                genitore = dati_atleta.get('nome_genitore', '')
                cf_gen = dati_atleta.get('codice_fiscale_genitore', '')
                nascita = dati_atleta.get('luogo_data_nascita', '')
                indirizzo = dati_atleta.get('indirizzo', '')
                default_pagante = genitore if pd.notna(genitore) and str(genitore).strip() != "" else nome_form

            with st.form("form_compilazione_sportiva"):
                st.markdown("<div translate='no' class='header-sezione notranslate' style='margin-top: 10px;'><span>💶</span> Dettagli Importi</div>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                prossimo_num = get_prossimo_numero(tipo_contatore)
                num_ric = c1.number_input("Numero Ricevuta (POS)", min_value=1, value=prossimo_num, step=1)
                num_ric_str = f"{num_ric:02d}"
                data_ric = c2.text_input("Data Emissione", datetime.now().strftime('%d/%m/%Y'))
                importo = c3.number_input("Importo Cifre (€)", min_value=0.0, step=5.0, value=50.0)
                
                c4, c5 = st.columns([1, 1])
                importo_lettere = c4.text_input("Importo in Lettere", "CINQUANTA/00")
                causale = c5.text_input("Causale", "Scuola tennis")
                
                st.markdown("<div translate='no' class='header-sezione notranslate'><span>👤</span> Intestatario (Pagante)</div>", unsafe_allow_html=True)
                c6, c7 = st.columns(2)
                chi_paga = c6.text_input("Nome Pagante", value=default_pagante)
                cf_pagante = c7.text_input("Codice Fiscale Pagante", value=cf_gen)
                
                st.markdown("<div translate='no' class='header-sezione notranslate'><span>🏃</span> Dati Allievo</div>", unsafe_allow_html=True)
                c8, c9, c10 = st.columns(3)
                nome_allievo = c8.text_input("Nome Atleta", value=nome_form)
                nascita_allievo = c9.text_input("Luogo/Data Nascita", value=nascita)
                indirizzo_allievo = c10.text_input("Indirizzo Residenza", value=indirizzo)
                
                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                incaricato_firma = st.selectbox("Firma Autorizzata", ["Nessuno", "Sara Cesaroni", "Elisa Tradardi", "Valerio Cesaroni", "Federico Sciaboletta", "Eleonora Bartoli"])
                
                st.markdown("<br><br>", unsafe_allow_html=True)
                submit = st.form_submit_button("✨ GENERA RICEVUTA SPORTIVA PDF", type="primary")

            if submit:
                if not nome_allievo.strip():
                    st.error("⚠️ Attenzione: Seleziona il nome dell'atleta prima di generare la ricevuta.")
                else:
                    salva_numero_ricevuta(tipo_contatore, num_ric)
                    testo_firma = "" if incaricato_firma == "Nessuno" else incaricato_firma
                    
                    # PDF CREATION
                    pdf = FPDF(orientation='P', unit='mm', format='A4')
                    pdf.add_page()
                    pdf.rect(10, 10, 190, 140)
                    
                    pdf.set_xy(15, 15)
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(90, 6, "JUNIOR CLUB TERNI S.S.D. A R.L.", ln=1)
                    pdf.set_x(15)
                    pdf.set_font("Arial", '', 10)
                    pdf.cell(90, 5, "Via Arturo Toscanini n.49", ln=1)
                    pdf.set_x(15)
                    pdf.cell(90, 5, "05100 Terni (TR) ITA", ln=1)
                    pdf.set_x(15)
                    pdf.cell(90, 5, "C.F.: 01550520553", ln=1)
                    
                    pdf.set_xy(120, 15)
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(40, 8, "RICEVUTA n.")
                    pdf.set_font("Courier", 'B', 16)
                    pdf.cell(30, 8, num_ric_str, border='B', align='C')
                    pdf.set_xy(125, 30)
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(15, 10, "Euro", align='R')
                    pdf.set_font("Courier", 'B', 16)
                    pdf.cell(50, 10, f"{importo:.2f}", border=1, align='C')
                    
                    pdf.set_xy(15, 50)
                    pdf.set_font("Arial", 'B', 14)
                    pdf.cell(50, 8, "RICEVIAMO")
                    pdf.set_xy(15, 60)
                    pdf.set_font("Arial", '', 10)
                    pdf.cell(8, 6, "da")
                    pdf.set_font("Courier", 'B', 11)
                    pdf.cell(92, 6, chi_paga, border='B')
                    pdf.set_font("Arial", '', 10)
                    pdf.cell(35, 6, "(CODICE FISCALE)")
                    pdf.set_font("Courier", 'B', 11)
                    pdf.cell(40, 6, cf_pagante, border='B')
                    pdf.set_xy(15, 70)
                    pdf.set_font("Arial", '', 10)
                    pdf.cell(32, 6, "la somma di Euro")
                    pdf.set_font("Courier", 'B', 11)
                    pdf.cell(93, 6, importo_lettere, border=1)
                    pdf.set_font("Arial", '', 10)
                    pdf.cell(25, 6, "(IN LETTERE)")
                    pdf.set_xy(15, 80)
                    pdf.set_font("Arial", '', 10)
                    pdf.cell(38, 6, "per l'attività sportiva")
                    pdf.set_font("Courier", 'B', 11)
                    pdf.cell(137, 6, causale, border='B')
                    
                    pdf.rect(15, 95, 175, 35)
                    pdf.set_xy(15, 95)
                    pdf.set_font("Arial", '', 9)
                    pdf.cell(40, 11, " COGNOME E NOME", border='B')
                    pdf.set_font("Courier", 'B', 11)
                    pdf.cell(135, 11, nome_allievo, border='B', align='R')
                    pdf.set_xy(15, 106)
                    pdf.set_font("Arial", '', 9)
                    pdf.cell(40, 11, " LUOGO/DATA NASCITA", border='B')
                    pdf.set_font("Courier", 'B', 11)
                    pdf.cell(135, 11, nascita_allievo, border='B', align='R')
                    pdf.set_xy(15, 117)
                    pdf.set_font("Arial", '', 9)
                    pdf.cell(40, 11, " INDIRIZZO")
                    pdf.set_font("Courier", 'B', 11)
                    pdf.cell(135, 11, indirizzo_allievo, align='R')
                    
                    pdf.set_xy(15, 135)
                    pdf.set_font("Arial", 'B', 10)
                    pdf.cell(12, 6, "Data")
                    pdf.set_font("Courier", 'B', 10)
                    pdf.cell(40, 6, data_ric, border='B')
                    
                    pdf.set_xy(120, 131)
                    pdf.set_font("Arial", '', 10)
                    pdf.cell(70, 6, "Firma dell'incaricato", align='C')
                    pdf.set_xy(120, 137)
                    pdf.set_font("Courier", 'B', 10)
                    pdf.cell(70, 6, testo_firma, border='T', align='C')
                    
                    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
                    nome_file_pdf = f"Ricevuta_POS_JuniorClub_n{num_ric_str}.pdf"

                    # HTML PREVIEW (Senza spazi vuoti all'inizio delle righe!)
                    html_ricevuta = f"""
<div class="ricevuta-stampabile notranslate" translate="no" style="background: white; border: 1px solid #E2E8F0; padding: 40px; max-width: 900px; margin: 30px auto; font-family: Arial, sans-serif; color: #0F172A; box-sizing: border-box; box-shadow: 0 10px 30px rgba(0,0,0,0.06); border-radius: 12px;">
<div style="display: flex; justify-content: space-between; align-items: flex-start;">
<div style="width: 55%; font-size: 12px; line-height: 1.5; color: #0F172A;">
<span style="font-size: 18px; font-weight: 900; display: block; margin-bottom: 4px;">JUNIOR CLUB TERNI S.S.D. A R.L.</span>
<span style="font-weight: 600;">Via Arturo Toscanini n.49<br>05100 Terni (TR) ITA<br>C.F.: 01550520553</span>
</div>
<div style="width: 40%; text-align: right;">
<div style="font-size: 24px; font-weight: 900;">RICEVUTA <span style="font-size: 14px;">n.</span> <span style="font-family: 'Courier New', monospace; border-bottom: 2px solid #0F172A; padding: 0 20px;">{num_ric_str}</span></div>
<div style="display: flex; align-items: center; justify-content: flex-end; margin-top: 15px;">
<div style="font-size: 32px; font-weight: bold; margin-right: 15px;">€</div>
<div style="border: 2px solid #0F172A; width: 220px; height: 45px; display: flex; background: white;">
<div style="flex-grow: 1; text-align: center; font-size: 22px; font-family: 'Courier New', monospace; font-weight: bold; line-height: 41px;">{importo:.2f}</div>
<div style="width: 45px; background-color: #F8FAFC; border-left: 2px solid #0F172A;"></div>
</div></div></div></div>
<div style="font-size: 22px; font-weight: 900; margin-top: 40px; margin-bottom: 15px;">RICEVIAMO</div>
<div style="display: flex; align-items: flex-end; border-bottom: 1px solid #0F172A; margin-bottom: 20px; padding-bottom: 4px;">
<span style="font-weight: bold; font-size: 15px; margin-right: 10px;">da</span>
<span style="flex-grow: 1; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px;">{chi_paga}</span>
<span style="font-weight: bold; font-size: 15px; margin-left: 10px; margin-right: 10px;">(CODICE FISCALE)</span>
<span style="font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px;">{cf_pagante}</span>
</div>
<div style="display: flex; align-items: center; border-bottom: 1px solid #0F172A; margin-bottom: 20px; padding-bottom: 4px;">
<span style="font-weight: bold; font-size: 15px; margin-right: 10px;">la somma* di €</span>
<div style="flex-grow: 1; background: #F8FAFC; border: 1px solid #0F172A; height: 32px; line-height: 32px; padding-left: 10px; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px; margin-right: 10px;">{importo_lettere}</div>
<span style="font-weight: bold; font-size: 15px;">(IN LETTERE)</span>
</div>
<div style="display: flex; align-items: flex-end; border-bottom: 1px solid #0F172A; margin-bottom: 30px; padding-bottom: 4px;">
<span style="font-weight: bold; font-size: 15px; margin-right: 10px;">per l'attività sportiva</span>
<span style="flex-grow: 1; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px;">{causale}</span>
</div>
<div style="display: flex; justify-content: space-between; align-items: stretch; margin-bottom: 60px;">
<div style="width: 100%; border: 1px solid #0F172A; display: flex; background: white;">
<div style="width: 20px; background: #F8FAFC; border-right: 1px solid #0F172A; flex-shrink: 0;"></div>
<div style="flex-grow: 1; padding: 15px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="display: flex; justify-content: space-between; border-bottom: 1px solid #E2E8F0; padding-bottom: 4px;">
<span style="font-size: 12px; font-weight: bold;">COGNOME E NOME</span>
<span style="font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{nome_allievo}</span>
</div>
<div style="display: flex; justify-content: space-between; border-bottom: 1px solid #E2E8F0; padding-bottom: 4px; padding-top: 4px;">
<span style="font-size: 12px; font-weight: bold;">LUOGO/DATA DI NASCITA</span>
<span style="font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{nascita_allievo}</span>
</div>
<div style="display: flex; justify-content: space-between; padding-top: 4px;">
<span style="font-size: 12px; font-weight: bold;">INDIRIZZO</span>
<span style="font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{indirizzo_allievo}</span>
</div></div></div>
</div>
<div style="display: flex; justify-content: space-between; align-items: flex-end;">
<div style="font-weight: bold; font-size: 15px;">Data <span style="font-family: 'Courier New', monospace; border-bottom: 1px solid #0F172A; padding: 0 20px;">{data_ric}</span></div>
<div style="text-align: center; font-weight: bold; font-size: 15px; width: 250px;">
Firma dell'incaricato
<div style="border-bottom: 1px solid #0F172A; width: 100%; margin-top: 5px; margin-bottom: 5px;"></div>
<span style="font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{testo_firma}</span>
</div>
</div></div>
"""
                    st.markdown(html_ricevuta, unsafe_allow_html=True)
                    
                    # PULSANTIERA EMAIL UNIVERSALE
                    st.markdown("<hr style='margin-top: 30px; margin-bottom: 20px; border-color: #E2E8F0;'>", unsafe_allow_html=True)
                    st.download_button(label="📥 1. SCARICA IL FILE PDF", data=pdf_bytes, file_name=nome_file_pdf, mime="application/pdf", use_container_width=True)
                    st.components.v1.html(f"""
                        <script>
                            function lanciaStampa() {{ window.parent.print(); }}
                            function apriGmail() {{ var s=encodeURIComponent("Ricevuta Junior Club Terni n. {num_ric_str}"); var b=encodeURIComponent("Gentile cliente,\\n\\nIn allegato trova la ricevuta n. {num_ric_str}.\\n\\nCordiali saluti,\\nJunior Club Terni S.S.D. A R.L."); window.open("https://mail.google.com/mail/?view=cm&fs=1&su="+s+"&body="+b, '_blank'); }}
                            function apriOutlook() {{ var s=encodeURIComponent("Ricevuta Junior Club Terni n. {num_ric_str}"); var b=encodeURIComponent("Gentile cliente,\\n\\nIn allegato trova la ricevuta n. {num_ric_str}.\\n\\nCordiali saluti,\\nJunior Club Terni S.S.D. A R.L."); window.open("https://outlook.live.com/mail/0/deeplink/compose?subject="+s+"&body="+b, '_blank'); }}
                            function apriMailApp() {{ var s=encodeURIComponent("Ricevuta Junior Club Terni n. {num_ric_str}"); var b=encodeURIComponent("Gentile cliente,\\n\\nIn allegato trova la ricevuta n. {num_ric_str}.\\n\\nCordiali saluti,\\nJunior Club Terni S.S.D. A R.L."); window.parent.location.href = "mailto:?subject="+s+"&body="+b; }}
                        </script>
                        <div style="font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; color: #475569; margin-bottom: 8px;">2. SCEGLI L'APP E TRASCINA IL PDF:</div>
                        <div style="display: flex; gap: 10px;">
                            <button onclick="lanciaStampa()" style="flex: 1; background-color: #0F172A; color: white; border: none; padding: 14px; font-size: 13px; border-radius: 12px; cursor: pointer; font-weight: 800; transition: 0.2s;">🖨️ STAMPA PDF</button>
                            <button onclick="apriGmail()" style="flex: 1; background-color: #EA4335; color: white; border: none; padding: 14px; font-size: 13px; border-radius: 12px; cursor: pointer; font-weight: 800; transition: 0.2s;">🔴 APRI GMAIL</button>
                            <button onclick="apriOutlook()" style="flex: 1; background-color: #0078D4; color: white; border: none; padding: 14px; font-size: 13px; border-radius: 12px; cursor: pointer; font-weight: 800; transition: 0.2s;">🔵 APRI OUTLOOK</button>
                            <button onclick="apriMailApp()" style="flex: 1; background-color: #64748B; color: white; border: none; padding: 14px; font-size: 13px; border-radius: 12px; cursor: pointer; font-weight: 800; transition: 0.2s;">✉️ ALTRA APP</button>
                        </div>
                    """, height=100)

    # =========================================================================
    # B) MODELLO: RICEVUTA GENERICA (CONTANTI)
    # =========================================================================
    else:
        tipo_contatore = "CONTANTI"
        with st.form("form_compilazione_generica"):
            st.markdown("<div translate='no' class='header-sezione notranslate' style='margin-top: 0px;'><span>📄</span> Dati Ricevuta Generica</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            prossimo_num = get_prossimo_numero(tipo_contatore)
            num_ric = c1.number_input("Numero Ricevuta (CONTANTI)", min_value=1, value=prossimo_num, step=1)
            num_ric_str = f"{num_ric:02d}"
            data_ric = c2.text_input("Data Emissione", datetime.now().strftime('%d/%m/%Y'))
            importo = c3.number_input("Importo Cifre (€)", min_value=0.0, step=5.0, value=50.0)
            
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            chi_paga = st.text_input("Ricevuti da (Nome/Ente)", placeholder="Es. Rossi Mario / Comune di Terni")
            
            c4, c5 = st.columns([1, 1])
            importo_lettere = c4.text_input("Importo in Lettere", "CINQUANTA/00")
            causale = c5.text_input("Per (Causale)", placeholder="Es. Affitto campi")
            
            incaricato_firma = st.selectbox("Firma Autorizzata", ["Nessuno", "Sara Cesaroni", "Elisa Tradardi", "Valerio Cesaroni", "Federico Sciaboletta", "Eleonora Bartoli"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_gen = st.form_submit_button("✨ GENERA RICEVUTA GENERICA PDF", type="primary")

        if submit_gen:
            if not chi_paga.strip():
                st.error("⚠️ Attenzione: Inserisci da chi hai ricevuto i soldi.")
            else:
                salva_numero_ricevuta(tipo_contatore, num_ric)
                testo_firma = "" if incaricato_firma == "Nessuno" else incaricato_firma
                
                # PDF CREATION
                pdf = FPDF(orientation='P', unit='mm', format='A4')
                pdf.add_page()
                pdf.rect(10, 10, 190, 100)
                
                pdf.set_xy(15, 15)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(90, 6, "JUNIOR CLUB TERNI S.S.D. A R.L.", ln=1)
                pdf.set_x(15)
                pdf.set_font("Arial", '', 10)
                pdf.cell(90, 5, "Via Arturo Toscanini n.49", ln=1)
                pdf.set_x(15)
                pdf.cell(90, 5, "05100 Terni (TR) ITA", ln=1)
                pdf.set_x(15)
                pdf.cell(90, 5, "C.F.: 01550520553", ln=1)
                
                pdf.set_xy(120, 15)
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(40, 8, "RICEVUTA n.", align='R')
                pdf.set_font("Courier", 'B', 16)
                pdf.cell(30, 8, num_ric_str, border='B', align='C')
                
                pdf.set_xy(120, 25)
                pdf.set_font("Arial", '', 12)
                pdf.cell(40, 8, "data", align='R')
                pdf.set_font("Courier", 'B', 12)
                pdf.cell(30, 8, data_ric, border='B', align='C')
                
                pdf.set_xy(15, 45)
                pdf.set_font("Arial", '', 12)
                pdf.cell(25, 8, "Ricevuti da")
                pdf.set_font("Courier", 'B', 14)
                pdf.cell(150, 8, chi_paga, border='B')
                
                pdf.set_xy(15, 60)
                pdf.set_font("Arial", 'B', 22)
                pdf.cell(10, 12, "€")
                pdf.rect(25, 60, 165, 12, style='D')
                pdf.set_xy(25, 60)
                pdf.set_fill_color(240, 244, 248) 
                pdf.rect(25, 60, 165, 12, style='FD')
                pdf.set_font("Courier", 'B', 14)
                pdf.cell(165, 12, f"  {importo_lettere}", align='L')
                
                pdf.set_xy(15, 80)
                pdf.set_font("Arial", '', 12)
                pdf.cell(10, 8, "Per")
                pdf.set_font("Courier", 'B', 12)
                pdf.cell(125, 8, causale, border='B')
                
                pdf.set_xy(15, 95)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(25, 10, "TOTALE €")
                pdf.set_fill_color(240, 244, 248)
                pdf.rect(40, 95, 40, 10, style='FD')
                pdf.set_xy(40, 95)
                pdf.set_font("Courier", 'B', 14)
                pdf.cell(40, 10, f"{importo:.2f}", align='C')
                
                pdf.rect(155, 78, 35, 30)
                pdf.set_xy(155, 82)
                pdf.set_font("Arial", '', 8)
                pdf.multi_cell(35, 5, "Soggetta\nad Imposta\nvigente\n\nAPPLICARE\nMARCA", align='C')
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
                nome_file_pdf = f"Ricevuta_CONTANTI_JuniorClub_n{num_ric_str}.pdf"

                # HTML PREVIEW (Senza spazi vuoti all'inizio delle righe)
                html_ricevuta = f"""
<div class="ricevuta-stampabile notranslate" translate="no" style="background: white; border: 1px solid #E2E8F0; padding: 40px; max-width: 900px; margin: 30px auto; font-family: Arial, sans-serif; color: #0F172A; box-sizing: border-box; box-shadow: 0 10px 30px rgba(0,0,0,0.06); border-radius: 12px;">
<div style="display: flex; justify-content: space-between; align-items: flex-start;">
<div style="width: 50%; font-size: 12px; line-height: 1.5; color: #0F172A;">
<span style="font-size: 18px; font-weight: 900; display: block; margin-bottom: 4px;">JUNIOR CLUB TERNI S.S.D. A R.L.</span>
<span style="font-weight: 600;">Via Arturo Toscanini n.49<br>05100 Terni (TR) ITA<br>C.F.: 01550520553</span>
</div>
<div style="width: 45%; text-align: right;">
<div style="font-size: 24px; font-weight: 900; margin-bottom: 10px;">RICEVUTA n. <span style="font-family: 'Courier New', monospace; border-bottom: 2px solid #0F172A; padding: 0 20px; font-weight: bold;">{num_ric_str}</span></div>
<div style="font-size: 16px;">data <span style="font-family: 'Courier New', monospace; border-bottom: 1px solid #0F172A; padding: 0 20px; font-weight: bold;">{data_ric}</span></div>
</div>
</div>
<div style="margin-top: 40px; font-size: 16px; display: flex; align-items: flex-end;">
<span style="margin-right: 15px;">Ricevuti da</span>
<span style="flex-grow: 1; border-bottom: 1px solid #0F172A; font-family: 'Courier New', monospace; font-weight: bold; font-size: 18px; padding-bottom: 2px;">{chi_paga}</span>
</div>
<div style="display: flex; align-items: center; margin-top: 30px;">
<div style="font-size: 38px; font-weight: bold; margin-right: 15px;">€</div>
<div style="flex-grow: 1; background-color: #EEF2F6; border: 2px solid #CBD5E1; height: 50px; line-height: 46px; padding-left: 20px; font-family: 'Courier New', monospace; font-weight: bold; font-size: 20px;">{importo_lettere}</div>
</div>
<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 30px;">
<div style="width: 70%; display: flex; align-items: flex-end;">
<span style="margin-right: 15px;">Per</span>
<span style="flex-grow: 1; border-bottom: 1px solid #0F172A; font-family: 'Courier New', monospace; font-weight: bold; font-size: 16px; padding-bottom: 2px;">{causale}</span>
</div>
<div style="width: 120px; border: 1px solid #0F172A; text-align: center; padding: 15px 5px; font-size: 11px; font-weight: bold; background: white; margin-bottom: -50px;">
Soggetta<br>ad Imposta<br>vigente<br><br><span style="font-size: 9px;">APPLICARE LA<br>MARCA SUL RETRO</span>
</div>
</div>
<div style="display: flex; align-items: center; margin-top: 40px;">
<div style="font-size: 20px; font-weight: bold; margin-right: 15px;">TOTALE €</div>
<div style="width: 150px; background-color: #EEF2F6; border: 2px solid #CBD5E1; height: 40px; line-height: 36px; text-align: center; font-family: 'Courier New', monospace; font-weight: bold; font-size: 20px;">{importo:.2f}</div>
</div>
<div style="text-align: right; margin-top: 30px; font-weight: bold; font-size: 15px;">
Firma
<div style="border-bottom: 1px solid #0F172A; width: 250px; margin-left: auto; margin-top: 5px; margin-bottom: 5px;"></div>
<span style="font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{testo_firma}</span>
</div>
</div>
"""
                st.markdown(html_ricevuta, unsafe_allow_html=True)
                
                # PULSANTIERA EMAIL UNIVERSALE
                st.markdown("<hr style='margin-top: 30px; margin-bottom: 20px; border-color: #E2E8F0;'>", unsafe_allow_html=True)
                st.download_button(label="📥 1. SCARICA IL FILE PDF", data=pdf_bytes, file_name=nome_file_pdf, mime="application/pdf", use_container_width=True)
                st.components.v1.html(f"""
                    <script>
                        function lanciaStampa() {{ window.parent.print(); }}
                        function apriGmail() {{ var s=encodeURIComponent("Ricevuta Generica Junior Club Terni n. {num_ric_str}"); var b=encodeURIComponent("Gentile cliente,\\n\\nIn allegato trova la ricevuta n. {num_ric_str}.\\n\\nCordiali saluti,\\nJunior Club Terni S.S.D. A R.L."); window.open("https://mail.google.com/mail/?view=cm&fs=1&su="+s+"&body="+b, '_blank'); }}
                        function apriOutlook() {{ var s=encodeURIComponent("Ricevuta Generica Junior Club Terni n. {num_ric_str}"); var b=encodeURIComponent("Gentile cliente,\\n\\nIn allegato trova la ricevuta n. {num_ric_str}.\\n\\nCordiali saluti,\\nJunior Club Terni S.S.D. A R.L."); window.open("https://outlook.live.com/mail/0/deeplink/compose?subject="+s+"&body="+b, '_blank'); }}
                        function apriMailApp() {{ var s=encodeURIComponent("Ricevuta Generica Junior Club Terni n. {num_ric_str}"); var b=encodeURIComponent("Gentile cliente,\\n\\nIn allegato trova la ricevuta n. {num_ric_str}.\\n\\nCordiali saluti,\\nJunior Club Terni S.S.D. A R.L."); window.parent.location.href = "mailto:?subject="+s+"&body="+b; }}
                    </script>
                    <div style="font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; color: #475569; margin-bottom: 8px;">2. SCEGLI L'APP E TRASCINA IL PDF:</div>
                    <div style="display: flex; gap: 10px;">
                        <button onclick="lanciaStampa()" style="flex: 1; background-color: #0F172A; color: white; border: none; padding: 14px; font-size: 13px; border-radius: 12px; cursor: pointer; font-weight: 800; transition: 0.2s;">🖨️ STAMPA PDF</button>
                        <button onclick="apriGmail()" style="flex: 1; background-color: #EA4335; color: white; border: none; padding: 14px; font-size: 13px; border-radius: 12px; cursor: pointer; font-weight: 800; transition: 0.2s;">🔴 APRI GMAIL</button>
                        <button onclick="apriOutlook()" style="flex: 1; background-color: #0078D4; color: white; border: none; padding: 14px; font-size: 13px; border-radius: 12px; cursor: pointer; font-weight: 800; transition: 0.2s;">🔵 APRI OUTLOOK</button>
                        <button onclick="apriMailApp()" style="flex: 1; background-color: #64748B; color: white; border: none; padding: 14px; font-size: 13px; border-radius: 12px; cursor: pointer; font-weight: 800; transition: 0.2s;">✉️ ALTRA APP</button>
                    </div>
                """, height=100)

# --- 6. ANAGRAFICA E STORICO ---
elif menu == "👥 Anagrafica Clienti":
    st.markdown("<div translate='no' class='titolo-app notranslate'>Anagrafica Clienti</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ NUOVO ALLIEVO", "📋 ELENCO ISCRITTI"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("aggiungi_singolo"):
            st.markdown("<div translate='no' class='header-sezione notranslate'><span>📋</span> Dati Anagrafici</div>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            nuovo_nome = col_a.text_input("Nome e Cognome Allievo")
            nuovo_nascita = col_b.text_input("Luogo e Data di Nascita")
            nuovo_indirizzo = st.text_input("Indirizzo di Residenza")
            
            st.markdown("<div translate='no' class='header-sezione notranslate'><span>👤</span> Dati Genitore (Per Detrazione)</div>", unsafe_allow_html=True)
            col_c, col_d = st.columns(2)
            nuovo_genitore = col_c.text_input("Nome Genitore / Pagante")
            nuovo_cf = col_d.text_input("Codice Fiscale")
            
            st.markdown("<br>", unsafe_allow_html=True)
            salva_nuovo = st.form_submit_button("SALVA NEL DATABASE", type="primary")
            
            if salva_nuovo:
                if nuovo_nome.strip() == "":
                    st.error("Il nome dell'allievo è obbligatorio.")
                else:
                    if aggiungi_socio_singolo(nuovo_nome, nuovo_nascita, nuovo_indirizzo, nuovo_genitore, nuovo_cf):
                        st.success("Allievo aggiunto con successo!")
                        st.rerun()

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_soci, use_container_width=True, height=600, hide_index=True)

else:
    st.markdown("<div translate='no' class='titolo-app notranslate'>Storico Pagamenti</div>", unsafe_allow_html=True)
    st.info("Funzione in fase di sviluppo.")