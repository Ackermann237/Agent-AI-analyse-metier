import streamlit as st
import json
import os
from dotenv import load_dotenv
from groq import Groq
import pandas as pd
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================
load_dotenv()

st.set_page_config(
    page_title="Assistant IA Consulting Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# STYLES CSS PROFESSIONNELS
# =====================================================
st.markdown("""
<style>
    /* Fond dégradé élégant */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Carte principale */
    .main-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        margin: 2rem auto;
        max-width: 1400px;
    }
    
    /* Titre principal */
    .main-title {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        text-align: center;
        color: white;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.95;
    }
    
    /* Masquer les labels Streamlit */
    .stTextArea label, .stTextArea > div > div > label {
        display: none !important;
    }
    
    /* Zone de texte */
    .stTextArea textarea {
        font-size: 1.1rem !important;
        border: 2px solid #cbd5e0 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    /* Bouton avec dégradé harmonieux */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1.2rem 3rem !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.4) !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        transform: translateY(-5px) scale(1.03) !important;
        box-shadow: 0 15px 40px rgba(79, 172, 254, 0.6) !important;
    }
    
    /* Section header */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 2rem 0 1rem 0;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Cartes KPI */
    .kpi-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-left: 5px solid #667eea;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .kpi-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        color: #1e293b;
        font-size: 1.8rem;
        font-weight: 800;
    }
    
    /* Insight box */
    .insight-box {
        background: #fff7ed;
        border-left: 5px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .insight-box h4 {
        color: #d97706;
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    
    .insight-box p {
        color: #92400e;
        margin: 0;
        line-height: 1.6;
    }
    
    /* Risk box */
    .risk-box {
        background: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .risk-box h4 {
        color: #dc2626;
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    
    /* Action box */
    .action-box {
        background: #ecfdf5;
        border-left: 5px solid #10b981;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .action-box h4 {
        color: #059669;
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    
    /* Timeline */
    .timeline-item {
        background: white;
        border-left: 4px solid #667eea;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Success message */
    .success-banner {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    /* DataFrames */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Masquer éléments Streamlit inutiles */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# API CONFIGURATION
# =====================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ **Clé API GROQ manquante**. Ajoute `GROQ_API_KEY=ta_clé` dans ton fichier `.env`")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# =====================================================
# PROMPT ENGINEERING AVANCÉ
# =====================================================
def build_advanced_prompt(user_input: str) -> str:
    return f"""Tu es un consultant senior expert en stratégie et analyse business pour un cabinet de conseil de prestige.

Analyse la demande client suivante de manière approfondie et professionnelle :

**DEMANDE CLIENT :**
{user_input}

**LIVRABLES ATTENDUS (format JSON strict) :**
{{
  "resume_executif": "Synthèse en 2-3 phrases de la problématique client",
  "type_demande": "Catégorie parmi: Analyse Stratégique, Reporting & BI, IA/ML, Benchmark Marché, Transformation Digitale, Due Diligence",
  "service_responsable": "Département: Strategy, Data & Analytics, Operations, Marketing & Growth, Technology",
  "priorite": "Haute/Moyenne/Basse",
  "complexite": "Faible/Moyenne/Élevée",
  "duree_estimee": "Durée en jours ou semaines",
  "budget_estime": "Fourchette budgétaire approximative en K€",
  
  "analyse_approfondie": {{
    "enjeux_business": ["Liste des 3-4 enjeux métier clés"],
    "opportunites": ["2-3 opportunités identifiées"],
    "risques": ["2-3 risques potentiels"],
    "parties_prenantes": ["Acteurs clés à impliquer"]
  }},
  
  "recommandations": {{
    "actions_immediates": ["3-4 actions à lancer sous 1 semaine"],
    "plan_moyen_terme": ["2-3 initiatives sur 1-3 mois"],
    "indicateurs_succes": ["KPIs pour mesurer le succès"]
  }},
  
  "ressources_requises": {{
    "competences": ["Expertises nécessaires"],
    "outils": ["Technologies/outils recommandés"],
    "partenaires": ["Partenaires externes éventuels"]
  }},
  
  "roadmap": [
    {{"phase": "Phase 1", "duree": "X jours", "livrables": ["Livrable 1", "Livrable 2"]}},
    {{"phase": "Phase 2", "duree": "X jours", "livrables": ["Livrable 1", "Livrable 2"]}}
  ],
  
  "points_vigilance": ["2-3 points d'attention critiques"],
  "valeur_ajoutee": "Impact business attendu et ROI potentiel"
}}

Réponds UNIQUEMENT avec le JSON, sois précis, concret et actionnable."""

# =====================================================
# HEADER
# =====================================================
st.markdown("<h1 class='main-title'>🤖 Assistant IA Consulting Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>🎯 Analyse stratégique automatisée • Intelligence artificielle avancée</p>", unsafe_allow_html=True)

# =====================================================
# INPUT SECTION
# =====================================================

st.markdown("### 📋 Description de la demande client")
st.markdown("---")

demande = st.text_area(
    "input_demande",
    placeholder="Exemple : Notre client, un groupe bancaire européen, souhaite développer une solution d'IA pour automatiser l'analyse de risque crédit et améliorer son taux d'acceptation de 15% tout en réduisant le taux de défaut. Budget prévu : 500K€, délai : 6 mois.",
    height=150,
    help="💡 Incluez : contexte, objectifs chiffrés, contraintes, budget et délais si disponibles",
    key="demande_input"
)

st.markdown("<br>", unsafe_allow_html=True)

analyze = st.button("🚀 Lancer l'analyse stratégique")

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ANALYSIS LOGIC
# =====================================================
if analyze and demande.strip():
    
    with st.spinner("🔍 Analyse approfondie en cours..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Tu es un consultant McKinsey senior expert en stratégie. Tu réponds toujours en JSON structuré et actionnable."},
                    {"role": "user", "content": build_advanced_prompt(demande)}
                ],
                temperature=0.3,
                max_tokens=2000
            )

            raw_result = response.choices[0].message.content.strip()
            
            # Nettoyage JSON
            if "```json" in raw_result:
                raw_result = raw_result.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_result:
                raw_result = raw_result.split("```")[1].split("```")[0].strip()
            
            data = json.loads(raw_result)

        except json.JSONDecodeError as e:
            st.error("❌ **Erreur de parsing JSON**")
            with st.expander("Voir la réponse brute"):
                st.code(raw_result, language="text")
            st.stop()

        except Exception as e:
            st.error("❌ **Erreur API Groq**")
            st.exception(e)
            st.stop()

    # =================================================
    # RESULTS DISPLAY - FORMAT PROFESSIONNEL
    # =================================================
    
    st.markdown("<div class='success-banner'>✅ Analyse stratégique terminée avec succès</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    # ==================== SECTION 1: RÉSUMÉ EXÉCUTIF ====================
    st.markdown("<div class='section-header'>📊 RÉSUMÉ EXÉCUTIF</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: #f8fafc; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #667eea; margin: 1rem 0;'>
        <p style='font-size: 1.2rem; color: #1e293b; line-height: 1.8; margin: 0;'>
            {data['resume_executif']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ==================== SECTION 2: KPIs CLÉS ====================
    st.markdown("<div class='section-header'>🎯 INDICATEURS CLÉS</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>📌 Type de mission</div>
            <div class='kpi-value' style='font-size: 1.3rem;'>{data['type_demande']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>🏢 Service</div>
            <div class='kpi-value' style='font-size: 1.3rem;'>{data['service_responsable']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        priorite_colors = {"Haute": "#dc2626", "Moyenne": "#f59e0b", "Basse": "#10b981"}
        color = priorite_colors.get(data['priorite'], "#64748b")
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>🚦 Priorité</div>
            <div class='kpi-value' style='color: {color}; font-size: 1.3rem;'>{data['priorite']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>⚙️ Complexité</div>
            <div class='kpi-value' style='font-size: 1.3rem;'>{data['complexite']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>⏱️ Durée estimée</div>
            <div class='kpi-value' style='font-size: 1.5rem;'>{data['duree_estimee']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>💰 Budget estimé</div>
            <div class='kpi-value' style='font-size: 1.5rem;'>{data['budget_estime']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== SECTION 3: ANALYSE APPROFONDIE ====================
    st.markdown("<div class='section-header'>🔍 ANALYSE APPROFONDIE</div>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("""
        <div class='insight-box'>
            <h4>🎯 Enjeux Business</h4>
        </div>
        """, unsafe_allow_html=True)
        for enjeu in data['analyse_approfondie']['enjeux_business']:
            st.markdown(f"• {enjeu}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='insight-box'>
            <h4>💡 Opportunités</h4>
        </div>
        """, unsafe_allow_html=True)
        for opp in data['analyse_approfondie']['opportunites']:
            st.markdown(f"• {opp}")
    
    with col_right:
        st.markdown("""
        <div class='risk-box'>
            <h4>⚠️ Risques Identifiés</h4>
        </div>
        """, unsafe_allow_html=True)
        for risque in data['analyse_approfondie']['risques']:
            st.markdown(f"• {risque}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: #eff6ff; border-left: 5px solid #3b82f6; padding: 1.5rem; border-radius: 10px;'>
            <h4 style='color: #1e40af; margin: 0 0 0.5rem 0;'>👥 Parties Prenantes</h4>
        </div>
        """, unsafe_allow_html=True)
        for partie in data['analyse_approfondie']['parties_prenantes']:
            st.markdown(f"• {partie}")
    
    # ==================== SECTION 4: RECOMMANDATIONS ====================
    st.markdown("<div class='section-header'>✨ PLAN D'ACTION RECOMMANDÉ</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='action-box'>
        <h4>🚀 Actions Immédiates (Semaine 1)</h4>
    </div>
    """, unsafe_allow_html=True)
    
    for i, action in enumerate(data['recommandations']['actions_immediates'], 1):
        st.markdown(f"""
        <div class='timeline-item'>
            <strong>Action {i}:</strong> {action}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #0000; border-left: 5px solid #f59e0b; padding: 1.5rem; border-radius: 10px;'>
        <h4 style='color: #d97706; margin: 0 0 0.5rem 0;'>📅 Plan Moyen Terme (1-3 mois)</h4>
    </div>
    """, unsafe_allow_html=True)
    
    for initiative in data['recommandations']['plan_moyen_terme']:
        st.markdown(f"• {initiative}")
    
    # ==================== SECTION 5: ROADMAP ====================
    st.markdown("<div class='section-header'>🗺️ ROADMAP DÉTAILLÉE</div>", unsafe_allow_html=True)
    
    roadmap_data = []
    for phase in data['roadmap']:
        roadmap_data.append({
            "Phase": phase['phase'],
            "Durée": phase['duree'],
            "Livrables": ", ".join(phase['livrables'])
        })
    
    df_roadmap = pd.DataFrame(roadmap_data)
    st.dataframe(df_roadmap, use_container_width=True, hide_index=True)
    
    # ==================== SECTION 6: RESSOURCES ====================
    st.markdown("<div class='section-header'>🛠️ RESSOURCES REQUISES</div>", unsafe_allow_html=True)
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.markdown("**👨‍💼 Compétences**")
        for comp in data['ressources_requises']['competences']:
            st.markdown(f"• {comp}")
    
    with col_res2:
        st.markdown("**🔧 Outils**")
        for outil in data['ressources_requises']['outils']:
            st.markdown(f"• {outil}")
    
    with col_res3:
        st.markdown("**🤝 Partenaires**")
        for partenaire in data['ressources_requises']['partenaires']:
            st.markdown(f"• {partenaire}")
    
    # ==================== SECTION 7: KPIs & VALEUR ====================
    st.markdown("<div class='section-header'>📈 INDICATEURS DE SUCCÈS & ROI</div>", unsafe_allow_html=True)
    
    col_kpi1, col_kpi2 = st.columns(2)
    
    with col_kpi1:
        st.markdown("**🎯 KPIs de succès**")
        for kpi in data['recommandations']['indicateurs_succes']:
            st.markdown(f"• {kpi}")
    
    with col_kpi2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                    padding: 1.5rem; border-radius: 12px; border-left: 5px solid #10b981;'>
            <h4 style='color: #059669; margin: 0 0 0.5rem 0;'>💎 Valeur Ajoutée</h4>
            <p style='color: #065f46; margin: 0; line-height: 1.6;'>{data['valeur_ajoutee']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== SECTION 8: POINTS DE VIGILANCE ====================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='risk-box'>
        <h4>🔔 Points de Vigilance</h4>
    </div>
    """, unsafe_allow_html=True)
    
    for point in data['points_vigilance']:
        st.markdown(f"• {point}")
    
    # ==================== EXPORT OPTIONS ====================
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📤 Export des données")
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Télécharger le rapport JSON",
            data=json_str,
            file_name=f"analyse_consulting_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col_export2:
        # Créer un résumé textuel
        rapport_text = f"""RAPPORT D'ANALYSE STRATÉGIQUE
{'='*60}

RÉSUMÉ EXÉCUTIF:
{data['resume_executif']}

TYPE DE MISSION: {data['type_demande']}
SERVICE: {data['service_responsable']}
PRIORITÉ: {data['priorite']}
DURÉE: {data['duree_estimee']}
BUDGET: {data['budget_estime']}

ENJEUX BUSINESS:
{chr(10).join(['• ' + e for e in data['analyse_approfondie']['enjeux_business']])}

ACTIONS IMMÉDIATES:
{chr(10).join(['• ' + a for a in data['recommandations']['actions_immediates']])}

VALEUR AJOUTÉE:
{data['valeur_ajoutee']}
"""
        st.download_button(
            label="📄 Télécharger le rapport TXT",
            data=rapport_text,
            file_name=f"rapport_consulting_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

elif analyze:
    st.warning("⚠️ Veuillez saisir une demande avant de lancer l'analyse.")

# =====================================================
# FOOTER
# =====================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: white; padding: 2rem; background: rgba(0,0,0,0.2); 
            border-radius: 15px; margin-top: 3rem;'>
    <p style='font-size: 1.1rem; margin: 0;'>
        ⚡ Powered by <strong>Groq AI</strong> & <strong>Streamlit</strong>
    </p>
    <p style='font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;'>
        Développé par AMOUGOU André Désiré Junior • © 2026 Tous droits réservés
    </p>
</div>
""", unsafe_allow_html=True)

