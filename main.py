import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
from fpdf import FPDF

# --- 1. CONFIGURAZIONE PAGINA E FONT ---
st.set_page_config(page_title="Junior Club Terni", layout="wide", initial_sidebar_state="expanded")
NOME_DATABASE = "dati_circolo.db" 

st.markdown("""
    <style>
    /* Rimozione degli elementi di default di Streamlit per un look pulito */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} .stAppDeployButton {display: none;}
    
    /* Configurazione del Font moderno */
    .stApp { background-color: #f1f5f9; font-family: 'Inter', sans-serif; }
    
    /* SIDEBAR ARANCIONE JUNIOR CLUB */
    [data-testid="stSidebar"] { 
        background-color: #FF6501 !important; 
        border-right: none; 
        box-shadow: 4px 0 20px rgba(0,0,0,0.08);
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; font-weight: 600; }
    
    /* Titoli Principali Ultra-Definiti */
    .titolo-app { color: #0f172a; font-size: 42px; font-weight: 900; margin-bottom: 0px; text-transform: uppercase;}
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
        transition: all 0.2s ease;
    }
    .stTextInput input:focus, .stNumberInput input:focus { 
        border-color: #FF6501 !important; 
        background-color: #ffffff !important; 
        box-shadow: 0 0 0 3px rgba(255, 101, 1, 0.1) !important; 
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
    }
    button[kind="primary"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 25px -5px rgba(15, 23, 42, 0.6) !important;
        background-color: #FF6501 !important;
    }

    /* TRUCCO PER STAMPARE SOLO L'ANTEPRIMA A PAGINA 1 */
    @media print {
        body * { visibility: hidden; }
        .ricevuta-stampabile, .ricevuta-stampabile * { visibility: visible; }
        .ricevuta-stampabile { position: absolute; left: 0; top: 0; margin: 0 !important; width: 100%; }
        .stButton, .stAlert, iframe, .stDownloadButton { display: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE E CONTATORE RICEVUTE ---
def init_db():
    conn = sqlite3.connect(NOME_DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS soci (nome_atleta TEXT, luogo_data_nascita TEXT, indirizzo TEXT, nome_genitore TEXT, codice_fiscale_genitore TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS contatore_ricevute (numero INTEGER)''')
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

def get_prossimo_numero():
    conn = sqlite3.connect(NOME_DATABASE)
    c = conn.cursor()
    c.execute("SELECT MAX(numero) FROM contatore_ricevute")
    max_num = c.fetchone()[0]
    conn.close()
    return (max_num + 1) if max_num else 1

def salva_numero_ricevuta(numero):
    conn = sqlite3.connect(NOME_DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO contatore_ricevute VALUES (?)", (numero,))
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

# --- 4. MENU ---
st.sidebar.markdown("<h2 style='font-weight: 900; font-size: 28px; text-align: center; margin-bottom: 40px; letter-spacing: -1px;'>JUNIOR CLUB TERNI</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("SEZIONI:", ["📝 Emissione Ricevuta", "👥 Anagrafica Clienti", "📊 Storico Pagamenti"])

# --- 5. RICEVUTA ---
if menu == "📝 Emissione Ricevuta":
    st.markdown("<div class='titolo-app'>EMISSIONE RICEVUTA</div><div class='sottotitolo'>Modulo ufficiale JUNIOR CLUB TERNI.</div>", unsafe_allow_html=True)
    
    if df_soci.empty:
        st.warning("L'archivio è vuoto. Vai in 'Anagrafica Clienti' per aggiungere un iscritto.")
    else:
        col_nome = 'nome_atleta' if 'nome_atleta' in df_soci.columns else df_soci.columns[0]
        
        st.markdown("<div style='background-color: #fff; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 25px; box-shadow: 0 4px 15px -1px rgba(0,0,0,0.05);'><div style='font-size: 12px; font-weight: 900; color: #475569; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px;'>🔍 CERCA ALLIEVO IN ARCHIVIO</div>", unsafe_allow_html=True)
        atleta_selezionato = st.selectbox("", df_soci[col_nome].tolist(), label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
        dati_atleta = df_soci[df_soci[col_nome] == atleta_selezionato].iloc[0]
        genitore = dati_atleta.get('nome_genitore', '')
        cf_gen = dati_atleta.get('codice_fiscale_genitore', '')
        nascita = dati_atleta.get('luogo_data_nascita', '')
        indirizzo = dati_atleta.get('indirizzo', '')
        default_pagante = genitore if pd.notna(genitore) and str(genitore).strip() != "" else dati_atleta[col_nome]

        with st.form("form_compilazione"):
            
            st.markdown("<div class='header-sezione'><span>💶</span> DETTAGLI RICEVUTA E IMPORTI</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            prossimo_num = get_prossimo_numero()
            num_ric = c1.number_input("Numero Ricevuta *", min_value=1, value=prossimo_num, step=1)
            num_ric_str = f"{num_ric:02d}"
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
            nome_allievo = c8.text_input("Nome Atleta *", value=dati_atleta[col_nome])
            nascita_allievo = c9.text_input("Luogo/Data di Nascita *", value=nascita)
            indirizzo_allievo = c10.text_input("Indirizzo di Residenza *", value=indirizzo)
            
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            incaricato_firma = st.selectbox("Firma Autorizzata", ["Nessuno", "Sara Cesaroni", "Elisa Tradardi", "Valerio Cesaroni", "Federico Sciaboletta", "Eleonora Bartoli"])
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            submit = st.form_submit_button("✨ GENERA RICEVUTA", type="primary")

        if submit:
            salva_numero_ricevuta(num_ric)
            testo_firma = "" if incaricato_firma == "Nessuno" else incaricato_firma
            
            # --- 1. CREAZIONE DEL FILE PDF (PER IL DOWNLOAD DIRETTO) ---
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            pdf.rect(10, 10, 190, 140)
            pdf.set_xy(15, 15)
            pdf.set_font("Arial", '', 9)
            pdf.multi_cell(90, 4, "DENOMINAZIONE o RAGIONE SOCIALE e SEDE LEGALE\ndella ditta ovvero COGNOME e NOME,\nRESIDENZA, C.F. se persona fisica")
            pdf.set_xy(15, 30)
            pdf.set_font("Arial", 'B', 12)
            pdf.multi_cell(90, 5, "JUNIOR CLUB TERNI - Terni\nC.F. 1234567890")
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
            pdf.rect(15, 95, 140, 35)
            pdf.set_xy(15, 95)
            pdf.set_font("Arial", '', 9)
            pdf.cell(40, 11, " COGNOME E NOME", border='B')
            pdf.set_font("Courier", 'B', 11)
            pdf.cell(100, 11, nome_allievo, border='B', align='R')
            pdf.set_xy(15, 106)
            pdf.set_font("Arial", '', 9)
            pdf.cell(40, 11, " LUOGO/DATA NASCITA", border='B')
            pdf.set_font("Courier", 'B', 11)
            pdf.cell(100, 11, nascita_allievo, border='B', align='R')
            pdf.set_xy(15, 117)
            pdf.set_font("Arial", '', 9)
            pdf.cell(40, 11, " INDIRIZZO")
            pdf.set_font("Courier", 'B', 11)
            pdf.cell(100, 11, indirizzo_allievo, align='R')
            pdf.rect(160, 95, 30, 35)
            pdf.set_xy(160, 100)
            pdf.set_font("Arial", '', 8)
            pdf.multi_cell(30, 5, "Soggetta\nad Imposta\nvigente\n\nAPPLICARE\nMARCA", align='C')
            pdf.set_xy(15, 135)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(12, 6, "Data")
            pdf.set_font("Courier", 'B', 10)
            pdf.cell(40, 6, data_ric, border='B')
            pdf.set_xy(120, 130)
            pdf.set_font("Arial", '', 10)
            pdf.cell(70, 6, "Firma dell'incaricato", align='C')
            pdf.set_xy(120, 140)
            pdf.set_font("Courier", 'B', 10)
            pdf.cell(70, 6, testo_firma, border='T', align='C')
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')

            # --- 2. ANTEPRIMA VISIVA A SCHERMO (BIANCO E NERO) ---
            html_ricevuta = f"""
            <div class="ricevuta-stampabile" style="background: white; border: 2px solid black; padding: 40px; max-width: 900px; margin: 30px auto; font-family: Arial, sans-serif; color: black; box-sizing: border-box; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="width: 55%; font-size: 10px; font-weight: bold; color: black; line-height: 1.4;">
            DENOMINAZIONE o RAGIONE SOCIALE e SEDE LEGALE della ditta ovvero COGNOME e NOME,<br>RESIDENZA, C.F. se persona fisica<br>
            <span style="color: black; font-size: 17px; font-weight: 900; display: block; margin-top: 8px;">JUNIOR CLUB TERNI - Terni - C.F. 1234567890</span>
            </div>
            <div style="width: 40%; text-align: right;">
            <div style="font-size: 24px; font-weight: 900;">RICEVUTA <span style="font-size: 14px;">n.</span> <span style="color: black; font-family: 'Courier New', monospace; border-bottom: 2px solid black; padding: 0 20px;">{num_ric_str}</span></div>
            <div style="display: flex; align-items: center; justify-content: flex-end; margin-top: 15px;">
            <div style="font-size: 32px; font-weight: bold; margin-right: 15px;">€</div>
            <div style="border: 2px solid black; width: 220px; height: 45px; display: flex; background: white;">
            <div style="flex-grow: 1; text-align: center; font-size: 22px; color: black; font-family: 'Courier New', monospace; font-weight: bold; line-height: 41px;">{importo:.2f}</div>
            <div style="width: 45px; background-color: #e5e5e5; border-left: 2px solid black;"></div>
            </div></div></div></div>
            <div style="font-size: 22px; font-weight: 900; margin-top: 40px; margin-bottom: 15px;">RICEVIAMO</div>
            <div style="display: flex; align-items: flex-end; border-bottom: 1.5px solid black; margin-bottom: 20px; padding-bottom: 4px;">
            <span style="font-weight: bold; font-size: 15px; margin-right: 10px;">da</span>
            <span style="flex-grow: 1; color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px;">{chi_paga}</span>
            <span style="font-weight: bold; font-size: 15px; margin-left: 10px; margin-right: 10px;">(CODICE FISCALE)</span>
            <span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px;">{cf_pagante}</span>
            </div>
            <div style="display: flex; align-items: center; border-bottom: 1.5px solid black; margin-bottom: 20px; padding-bottom: 4px;">
            <span style="font-weight: bold; font-size: 15px; margin-right: 10px;">la somma* di €</span>
            <div style="flex-grow: 1; background: #e5e5e5; border: 1px solid black; height: 32px; line-height: 32px; padding-left: 10px; color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px; margin-right: 10px;">{importo_lettere}</div>
            <span style="font-weight: bold; font-size: 15px;">(IN LETTERE)</span>
            </div>
            <div style="display: flex; align-items: flex-end; border-bottom: 1.5px solid black; margin-bottom: 30px; padding-bottom: 4px;">
            <span style="font-weight: bold; font-size: 15px; margin-right: 10px;">per l'attività sportiva</span>
            <span style="flex-grow: 1; color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 17px;">{causale}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: stretch; margin-bottom: 60px;">
            <div style="width: 70%; border: 1.5px solid black; display: flex; background: white;">
            <div style="width: 20px; background: #e5e5e5; border-right: 1.5px solid black; flex-shrink: 0;"></div>
            <div style="flex-grow: 1; padding: 15px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid black; padding-bottom: 4px;">
            <span style="font-size: 12px; font-weight: bold;">COGNOME E NOME</span>
            <span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{nome_allievo}</span>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid black; padding-bottom: 4px; padding-top: 4px;">
            <span style="font-size: 12px; font-weight: bold;">LUOGO/DATA DI NASCITA</span>
            <span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{nascita_allievo}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding-top: 4px;">
            <span style="font-size: 12px; font-weight: bold;">INDIRIZZO</span>
            <span style="color: black; font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px;">{indirizzo_allievo}</span>
            </div></div></div>
            <div style="width: 120px; border: 1.5px solid black; text-align: center; padding: 15px 5px; font-size: 11px; font-weight: bold; display: flex; flex-direction: column; justify-content: center; background: white;">
            Soggetta<br>ad Imposta<br>vigente<br><br><span style="font-size: 9px;">APPLICARE LA<br>MARCA SUL RETRO</span>
            </div></div>
            <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div style="font-weight: bold; font-size: 15px;">Data <span style="color: black; font-family: 'Courier New', monospace; border-bottom: 1.5px solid black; padding: 0 20px;">{data_ric}</span></div>
            <div style="text-align: center; font-weight: bold; font-size: 15px; width: 250px;">
            Firma dell'incaricato<br><br><div style="border-bottom: 1px solid black; width: 100%; margin: 5px 0;"></div>
            <span style="color: black; font-size: 15px;">{testo_firma}</span>
            </div></div></div>
            """
            st.markdown(html_ricevuta, unsafe_allow_html=True)

            # --- 3. I TASTI DI GESTIONE ---
            st.markdown("<hr style='margin-top: 30px; margin-bottom: 20px; border-color: #e2e8f0;'>", unsafe_allow_html=True)
            
            # Tasto DOWNLOAD (Pulsante nativo di Streamlit, modernizzato via CSS)
            st.download_button(
                label="📥 SCARICA IL FILE PDF",
                data=pdf_bytes,
                file_name=f"Ricevuta_JuniorClub_n{num_ric_str}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            # Tasti STAMPA E INVIA
            st.components.v1.html("""
                <script>
                    function lanciaStampa() { window.parent.print(); }
                    function lanciaInvia() { alert("La funzione per inviare via WhatsApp sarà collegata presto!"); }
                </script>
                <div style="display: flex; gap: 15px; margin-top: 5px;">
                    <button onclick="lanciaStampa()" style="flex: 1; background-color: #FF6501; color: white; border: none; padding: 12px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.2s;">🖨️ STAMPA SUBITO</button>
                    <button onclick="lanciaInvia()" style="flex: 1; background-color: #10b981; color: white; border: none; padding: 12px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.2s;">✉️ INVIA RICEVUTA</button>
                </div>
            """, height=70)

# --- 6. ANAGRAFICA E STORICO ---
elif menu == "👥 Anagrafica Clienti":
    st.markdown("<div class='titolo-app'>ANAGRAFICA CLIENTI</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ NUOVO ALLIEVO", "📋 ELENCO ISCRITTI"])
    
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
                    if aggiungi_socio_singolo(nuovo_nome, nuovo_nascita, nuovo_indirizzo, nuovo_genitore, nuovo_cf):
                        st.success("Allievo aggiunto con successo!")
                        st.rerun()

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_soci, use_container_width=True, height=600, hide_index=True)

else:
    st.markdown("<div class='titolo-app'>STORICO PAGAMENTI</div>", unsafe_allow_html=True)
    st.info("Funzione in fase di sviluppo.")

st.markdown('</div>', unsafe_allow_html=True)