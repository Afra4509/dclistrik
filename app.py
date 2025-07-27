import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import math

# Konfigurasi halaman
st.set_page_config(
    page_title="Rangkaian Listrik Arus Searah",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    st.markdown("""
    <style>
    /* Import dari file CSS terpisah */
    @import url('physics_listrik.css');
    
    /* Style utama aplikasi */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .calc-container {
        background: linear-gradient(145deg, #f8f9ff 0%, #e8f0fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e1e8ed;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    
    .result-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        font-weight: 600;
        color: #2d3748;
    }
    
    .formula-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        color: #2d3748;
        text-align: center;
    }
    
    .illustration-box {
        background: linear-gradient(145deg, #f0f8ff 0%, #e6f3ff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px dashed #87ceeb;
        text-align: center;
        margin: 1rem 0;
    }
    
    .comparison-table {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .footer-watermark {
        position: fixed;
        bottom: 10px;
        right: 20px;
        font-size: 12px;
        color: #8a9ba8;
        font-weight: 500;
        z-index: 999;
    }
    
    /* Styling untuk sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
    }
    
    /* Styling untuk input widgets */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.5rem;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
    }
    
    /* Hover effects */
    .calc-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Header utama
st.markdown("""
<div class="main-header">
    <h1>⚡ BAB 02: Rangkaian Listrik Arus Searah</h1>
    <p>Kalkulator Interaktif & Visualisasi Konsep Listrik DC</p>
</div>
""", unsafe_allow_html=True)

# Sidebar untuk input
st.sidebar.markdown("### 🔧 Panel Kontrol")

# Pilihan kalkulator
calc_option = st.sidebar.selectbox(
    "Pilih Kalkulator:",
    ["Hukum Ohm", "Hambatan Seri-Paralel", "Daya Listrik", "Energi Listrik", "GGL & Tegangan Jepit"]
)

# Fungsi untuk membuat grafik dengan style konsisten
def create_plotly_graph(fig, title):
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16, color='#2d3748')),
        plot_bgcolor='rgba(248, 249, 255, 0.8)',
        paper_bgcolor='rgba(255, 255, 255, 0.9)',
        font=dict(color='#2d3748'),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#e2e8f0',
            borderwidth=1
        ),
        margin=dict(t=60, l=60, r=30, b=60)
    )
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(135, 206, 235, 0.3)',
        showline=True,
        linewidth=2,
        linecolor='#cbd5e0'
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(135, 206, 235, 0.3)',
        showline=True,
        linewidth=2,
        linecolor='#cbd5e0'
    )
    return fig

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Kalkulator Hukum Ohm
    if calc_option == "Hukum Ohm":
        st.markdown('<div class="calc-container">', unsafe_allow_html=True)
        st.markdown("### ⚡ Kalkulator Hukum Ohm")
        
        ohm_calc = st.sidebar.selectbox("Hitung:", ["Tegangan (V)", "Arus (I)", "Hambatan (R)"])
        
        if ohm_calc == "Tegangan (V)":
            I = st.sidebar.number_input("Arus (I) dalam Ampere:", value=1.0, step=0.1)
            R = st.sidebar.number_input("Hambatan (R) dalam Ohm:", value=10.0, step=0.1)
            V = I * R
            
            st.markdown(f'<div class="formula-box">V = I × R = {I} × {R} = {V:.2f} Volt</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">🔋 Tegangan = {V:.2f} Volt</div>', unsafe_allow_html=True)
            
            # Grafik V vs I
            I_range = np.linspace(0.1, 5, 100)
            V_range = I_range * R
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=I_range, y=V_range, mode='lines', 
                                   name=f'R = {R}Ω', line=dict(color='#667eea', width=3)))
            fig.add_trace(go.Scatter(x=[I], y=[V], mode='markers', 
                                   name='Titik Aktual', marker=dict(color='#ff6b6b', size=10)))
            
            fig.update_xaxes(title='Arus (A)')
            fig.update_yaxes(title='Tegangan (V)')
            fig = create_plotly_graph(fig, 'Grafik Tegangan vs Arus (Hukum Ohm)')
            st.plotly_chart(fig, use_container_width=True)
            
        elif ohm_calc == "Arus (I)":
            V = st.sidebar.number_input("Tegangan (V) dalam Volt:", value=12.0, step=0.1)
            R = st.sidebar.number_input("Hambatan (R) dalam Ohm:", value=10.0, step=0.1)
            I = V / R if R != 0 else 0
            
            st.markdown(f'<div class="formula-box">I = V / R = {V} / {R} = {I:.2f} Ampere</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">⚡ Arus = {I:.2f} Ampere</div>', unsafe_allow_html=True)
            
            # Grafik I vs R
            R_range = np.linspace(1, 50, 100)
            I_range = V / R_range
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=R_range, y=I_range, mode='lines', 
                                   name=f'V = {V}V', line=dict(color='#4ecdc4', width=3)))
            fig.add_trace(go.Scatter(x=[R], y=[I], mode='markers', 
                                   name='Titik Aktual', marker=dict(color='#ff6b6b', size=10)))
            
            fig.update_xaxes(title='Hambatan (Ω)')
            fig.update_yaxes(title='Arus (A)')
            fig = create_plotly_graph(fig, 'Grafik Arus vs Hambatan')
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Hambatan (R)
            V = st.sidebar.number_input("Tegangan (V) dalam Volt:", value=12.0, step=0.1)
            I = st.sidebar.number_input("Arus (I) dalam Ampere:", value=1.0, step=0.1)
            R = V / I if I != 0 else 0
            
            st.markdown(f'<div class="formula-box">R = V / I = {V} / {I} = {R:.2f} Ohm</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">🔧 Hambatan = {R:.2f} Ohm</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Kalkulator Hambatan Seri-Paralel
    elif calc_option == "Hambatan Seri-Paralel":
        st.markdown('<div class="calc-container">', unsafe_allow_html=True)
        st.markdown("### 🔗 Kalkulator Hambatan Seri-Paralel")
        
        arrangement = st.sidebar.selectbox("Susunan:", ["Seri", "Paralel"])
        num_resistors = st.sidebar.slider("Jumlah Hambatan:", 2, 5, 3)
        
        resistors = []
        for i in range(num_resistors):
            r = st.sidebar.number_input(f"R{i+1} (Ohm):", value=10.0*(i+1), step=0.1, key=f"r{i}")
            resistors.append(r)
        
        if arrangement == "Seri":
            R_total = sum(resistors)
            formula = " + ".join([f"R{i+1}" for i in range(num_resistors)])
            calculation = " + ".join([f"{r}" for r in resistors])
            
            st.markdown(f'<div class="formula-box">R_total = {formula} = {calculation} = {R_total:.2f} Ω</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">🔗 Hambatan Total (Seri) = {R_total:.2f} Ohm</div>', unsafe_allow_html=True)
            
        else:  # Paralel
            R_inv_total = sum([1/r for r in resistors if r != 0])
            R_total = 1/R_inv_total if R_inv_total != 0 else 0
            formula = " + ".join([f"1/R{i+1}" for i in range(num_resistors)])
            calculation = " + ".join([f"1/{r}" for r in resistors])
            
            st.markdown(f'<div class="formula-box">1/R_total = {formula} = {calculation} = {R_inv_total:.4f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="formula-box">R_total = 1/{R_inv_total:.4f} = {R_total:.2f} Ω</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">🔀 Hambatan Total (Paralel) = {R_total:.2f} Ohm</div>', unsafe_allow_html=True)
        
        # Grafik perbandingan
        fig = go.Figure()
        
        # Hitung untuk berbagai konfigurasi
        test_values = np.linspace(1, 20, 50)
        seri_values = [sum([r*x/10 for r in resistors]) for x in test_values]
        paralel_values = [1/sum([1/(r*x/10) for r in resistors]) for x in test_values]
        
        fig.add_trace(go.Scatter(x=test_values, y=seri_values, mode='lines', 
                               name='Susunan Seri', line=dict(color='#667eea', width=3)))
        fig.add_trace(go.Scatter(x=test_values, y=paralel_values, mode='lines', 
                               name='Susunan Paralel', line=dict(color='#4ecdc4', width=3)))
        
        fig.update_xaxes(title='Faktor Pengali')
        fig.update_yaxes(title='Hambatan Total (Ω)')
        fig = create_plotly_graph(fig, 'Perbandingan Hambatan Seri vs Paralel')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Kalkulator Daya Listrik  
    elif calc_option == "Daya Listrik":
        st.markdown('<div class="calc-container">', unsafe_allow_html=True)
        st.markdown("### ⚡ Kalkulator Daya Listrik")
        
        power_method = st.sidebar.selectbox("Metode Perhitungan:", ["P = V × I", "P = I² × R", "P = V² / R"])
        
        if power_method == "P = V × I":
            V = st.sidebar.number_input("Tegangan (V) dalam Volt:", value=12.0, step=0.1)
            I = st.sidebar.number_input("Arus (I) dalam Ampere:", value=2.0, step=0.1)
            P = V * I
            
            st.markdown(f'<div class="formula-box">P = V × I = {V} × {I} = {P:.2f} Watt</div>', unsafe_allow_html=True)
            
        elif power_method == "P = I² × R":
            I = st.sidebar.number_input("Arus (I) dalam Ampere:", value=2.0, step=0.1)
            R = st.sidebar.number_input("Hambatan (R) dalam Ohm:", value=10.0, step=0.1)
            P = I**2 * R
            
            st.markdown(f'<div class="formula-box">P = I² × R = {I}² × {R} = {P:.2f} Watt</div>', unsafe_allow_html=True)
            
        else:  # P = V² / R
            V = st.sidebar.number_input("Tegangan (V) dalam Volt:", value=12.0, step=0.1)
            R = st.sidebar.number_input("Hambatan (R) dalam Ohm:", value=10.0, step=0.1)
            P = V**2 / R if R != 0 else 0
            
            st.markdown(f'<div class="formula-box">P = V² / R = {V}² / {R} = {P:.2f} Watt</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="result-box">💡 Daya Listrik = {P:.2f} Watt</div>', unsafe_allow_html=True)
        
        # Grafik daya vs waktu
        time_range = np.linspace(0, 10, 100)
        power_constant = np.full_like(time_range, P)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_range, y=power_constant, mode='lines', 
                               name=f'Daya Konstan', line=dict(color='#ff6b6b', width=3)))
        
        fig.update_xaxes(title='Waktu (s)')
        fig.update_yaxes(title='Daya (W)')
        fig = create_plotly_graph(fig, 'Grafik Daya vs Waktu')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Kalkulator Energi Listrik
    elif calc_option == "Energi Listrik":
        st.markdown('<div class="calc-container">', unsafe_allow_html=True)
        st.markdown("### 🔋 Kalkulator Energi Listrik")
        
        P = st.sidebar.number_input("Daya (P) dalam Watt:", value=100.0, step=1.0)
        t = st.sidebar.number_input("Waktu (t) dalam jam:", value=2.0, step=0.1)
        
        W_joule = P * t * 3600  # dalam Joule
        W_kwh = P * t / 1000    # dalam kWh
        
        st.markdown(f'<div class="formula-box">W = P × t = {P} W × {t} jam = {W_joule:.0f} Joule</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="formula-box">W = {P} W × {t} jam = {W_kwh:.3f} kWh</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">⚡ Energi = {W_joule:.0f} Joule = {W_kwh:.3f} kWh</div>', unsafe_allow_html=True)
        
        # Grafik energi vs waktu
        time_range = np.linspace(0, 10, 100)
        energy_range = P * time_range * 3600
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_range, y=energy_range, mode='lines', 
                               name=f'P = {P} W', line=dict(color='#45b7d1', width=3)))
        fig.add_trace(go.Scatter(x=[t], y=[W_joule], mode='markers', 
                               name='Titik Aktual', marker=dict(color='#ff6b6b', size=10)))
        
        fig.update_xaxes(title='Waktu (jam)')
        fig.update_yaxes(title='Energi (Joule)')
        fig = create_plotly_graph(fig, 'Grafik Energi vs Waktu')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Kalkulator GGL & Tegangan Jepit
    elif calc_option == "GGL & Tegangan Jepit":
        st.markdown('<div class="calc-container">', unsafe_allow_html=True)
        st.markdown("### 🔋 Kalkulator GGL & Tegangan Jepit")
        
        calc_type = st.sidebar.selectbox("Hitung:", ["GGL (ε)", "Tegangan Jepit (V)", "Hambatan Dalam (r)"])
        
        if calc_type == "GGL (ε)":
            V = st.sidebar.number_input("Tegangan Jepit (V) dalam Volt:", value=9.0, step=0.1)
            I = st.sidebar.number_input("Arus (I) dalam Ampere:", value=1.0, step=0.1)
            r = st.sidebar.number_input("Hambatan Dalam (r) dalam Ohm:", value=1.0, step=0.1)
            
            epsilon = V + (I * r)
            st.markdown(f'<div class="formula-box">ε = V + I×r = {V} + {I}×{r} = {epsilon:.2f} Volt</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">🔋 GGL (ε) = {epsilon:.2f} Volt</div>', unsafe_allow_html=True)
            
        elif calc_type == "Tegangan Jepit (V)":
            epsilon = st.sidebar.number_input("GGL (ε) dalam Volt:", value=12.0, step=0.1)
            I = st.sidebar.number_input("Arus (I) dalam Ampere:", value=1.0, step=0.1)
            r = st.sidebar.number_input("Hambatan Dalam (r) dalam Ohm:", value=1.0, step=0.1)
            
            V = epsilon - (I * r)
            st.markdown(f'<div class="formula-box">V = ε - I×r = {epsilon} - {I}×{r} = {V:.2f} Volt</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">⚡ Tegangan Jepit (V) = {V:.2f} Volt</div>', unsafe_allow_html=True)
            
        else:  # Hambatan Dalam (r)
            epsilon = st.sidebar.number_input("GGL (ε) dalam Volt:", value=12.0, step=0.1)
            V = st.sidebar.number_input("Tegangan Jepit (V) dalam Volt:", value=9.0, step=0.1)
            I = st.sidebar.number_input("Arus (I) dalam Ampere:", value=1.0, step=0.1)
            
            r = (epsilon - V) / I if I != 0 else 0
            st.markdown(f'<div class="formula-box">r = (ε - V) / I = ({epsilon} - {V}) / {I} = {r:.2f} Ohm</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">🔧 Hambatan Dalam (r) = {r:.2f} Ohm</div>', unsafe_allow_html=True)
        
        # Grafik tegangan jepit vs arus
        I_range = np.linspace(0.1, 5, 100)
        if calc_type != "Hambatan Dalam (r)":
            if calc_type == "GGL (ε)":
                V_jepit_range = epsilon - I_range * r
                epsilon_line = np.full_like(I_range, epsilon)
            else:
                V_jepit_range = epsilon - I_range * r
                epsilon_line = np.full_like(I_range, epsilon)
        else:
            V_jepit_range = epsilon - I_range * r
            epsilon_line = np.full_like(I_range, epsilon)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=I_range, y=V_jepit_range, mode='lines', 
                               name='Tegangan Jepit', line=dict(color='#4ecdc4', width=3)))
        fig.add_trace(go.Scatter(x=I_range, y=epsilon_line, mode='lines', 
                               name='GGL', line=dict(color='#ff6b6b', width=2, dash='dash')))
        
        fig.update_xaxes(title='Arus (A)')
        fig.update_yaxes(title='Tegangan (V)')
        fig = create_plotly_graph(fig, 'Grafik GGL vs Tegangan Jepit')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Kolom kanan untuk ilustrasi dan perbandingan
with col2:
    st.markdown("### 📚 Ilustrasi & Konsep")
    
    # Ilustrasi rangkaian
    st.markdown('<div class="illustration-box">', unsafe_allow_html=True)
    st.markdown("#### 🔗 Rangkaian Seri")
    st.markdown("""
    ```
    ——[R1]——[R2]——[R3]——
    +                    -
    ```
    **Karakteristik:**
    - Arus sama di semua titik
    - Tegangan terbagi
    - R_total = R1 + R2 + R3
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="illustration-box">', unsafe_allow_html=True)
    st.markdown("#### 🔀 Rangkaian Paralel")
    st.markdown("""
    ```
    +——[R1]——+
    |        |
    +——[R2]——+
    |        |
    +——[R3]——+
    ```
    **Karakteristik:**
    - Tegangan sama di semua cabang
    - Arus terbagi
    - 1/R_total = 1/R1 + 1/R2 + 1/R3
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Perbandingan DC vs AC
    st.markdown("#### ⚡ Perbandingan DC vs AC")
    
    # Grafik gelombang DC vs AC
    t = np.linspace(0, 4*np.pi, 400)
    dc_wave = np.ones_like(t) * 5
    ac_wave = 5 * np.sin(t)
    
    fig = make_subplots(rows=2, cols=1, 
                       subplot_titles=('Arus Searah (DC)', 'Arus Bolak-balik (AC)'),
                       vertical_spacing=0.1)
    
    fig.add_trace(go.Scatter(x=t, y=dc_wave, mode='lines', name='DC', 
                           line=dict(color='#667eea', width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=ac_wave, mode='lines', name='AC', 
                           line=dict(color='#4ecdc4', width=3)), row=2, col=1)
    
    fig.update_xaxes(title_text="Waktu", row=2, col=1)
    fig.update_yaxes(title_text="Tegangan (V)")
    
    fig = create_plotly_graph(fig, 'Kurva Gelombang DC vs AC')
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabel perbandingan
    st.markdown('<div class="comparison-table">', unsafe_allow_html=True)
    comparison_data = {
        'Aspek': ['Arah Arus', 'Bentuk Gelombang', 'Frekuensi', 'Sumber', 'Kegunaan'],
        'DC': ['Satu arah', 'Konstan', '0 Hz', 'Baterai, Aki', 'Elektronik'],
        'AC': ['Bolak-balik', 'Sinusoidal', '50/60 Hz', 'PLN, Generator', 'Rumah tangga']
    }
    st.table(comparison_data)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer watermark
st.markdown("""
<div class="footer-watermark">
    afrafdhma • SMADA
</div>
""", unsafe_allow_html=True)

# Informasi tambahan
st.markdown("---")
st.markdown("### 📖 Rumus-rumus Penting")

col_formula1, col_formula2, col_formula3 = st.columns(3)

with col_formula1:
    st.markdown("""
    **Hukum Ohm:**
    - V = I × R
    - I = V / R  
    - R = V / I
    """)

with col_formula2:
    st.markdown("""
    **Daya Listrik:**
    - P = V × I
    - P = I² × R
    - P = V² / R
    """)

with col_formula3:
    st.markdown("""
    **Energi & GGL:**
    - W = P × t
    - ε = V + I×r
    - V = ε - I×r
    """)
