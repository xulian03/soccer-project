import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Profesional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar el diseño
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f2937;
        font-weight: 700;
    }
    h2 {
        color: #374151;
        font-weight: 600;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar estado de sesión
if 'theme' not in st.session_state:
    st.session_state.theme = 'Claro'
if 'notifications' not in st.session_state:
    st.session_state.notifications = True

# Datos simulados
@st.cache_data
def generar_datos_ventas():
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    ventas = np.random.randint(50000, 150000, 12)
    return pd.DataFrame({'Mes': meses, 'Ventas': ventas})

@st.cache_data
def generar_datos_usuarios():
    nombres = ['Ana García', 'Carlos López', 'María Rodríguez', 'Juan Martínez', 'Laura Sánchez',
               'Pedro González', 'Sofia Fernández', 'Diego Torres', 'Carmen Ruiz', 'Javier Díaz']
    paises = ['España', 'México', 'Argentina', 'Colombia', 'Chile']
    estados = ['Activo', 'Inactivo', 'Pendiente']
    
    data = {
        'Nombre': nombres,
        'Edad': np.random.randint(22, 65, 10),
        'País': np.random.choice(paises, 10),
        'Estado': np.random.choice(estados, 10),
        'Registro': [(datetime.now() - timedelta(days=np.random.randint(1, 365))).strftime('%Y-%m-%d') for _ in range(10)]
    }
    return pd.DataFrame(data)

@st.cache_data
def generar_datos_productos():
    productos = ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E']
    ventas = np.random.randint(100, 500, 5)
    return pd.DataFrame({'Producto': productos, 'Unidades Vendidas': ventas})

@st.cache_data
def generar_datos_categorias():
    categorias = ['Electrónica', 'Ropa', 'Alimentos', 'Hogar', 'Deportes']
    valores = np.random.randint(15000, 50000, 5)
    return pd.DataFrame({'Categoría': categorias, 'Ventas': valores})

# Sidebar - Menú de navegación
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/667eea/ffffff?text=DASHBOARD", use_container_width=True)
    st.title("📊 Panel de Control")
    st.markdown("---")
    
    seccion = st.radio(
        "Navegación",
        ["🏠 Inicio", "📈 Estadísticas", "👥 Usuarios", "💰 Ventas", "⚙️ Configuración"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Información")
    st.info(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    st.success(f"👤 Usuario: Admin")

# Contenido principal según la sección seleccionada
if seccion == "🏠 Inicio":
    st.title("🏠 Panel de Inicio")
    st.markdown("### Resumen General del Sistema")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💵 Ingresos Totales",
            value="$1,245,890",
            delta="12.5%"
        )
    
    with col2:
        st.metric(
            label="👥 Usuarios Activos",
            value="8,542",
            delta="3.2%"
        )
    
    with col3:
        st.metric(
            label="📊 Tasa de Conversión",
            value="24.8%",
            delta="-1.2%"
        )
    
    with col4:
        st.metric(
            label="🛒 Ventas del Mes",
            value="3,456",
            delta="8.7%"
        )
    
    st.markdown("---")
    
    # Gráficos de resumen
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Tendencia de Ventas")
        df_ventas = generar_datos_ventas()
        fig = px.line(df_ventas, x='Mes', y='Ventas', markers=True)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Actividad Reciente")
        actividades = pd.DataFrame({
            'Actividad': ['Nueva venta registrada', 'Usuario nuevo registrado', 'Producto actualizado', 'Pago procesado', 'Comentario recibido'],
            'Tiempo': ['Hace 5 min', 'Hace 15 min', 'Hace 1 hora', 'Hace 2 horas', 'Hace 3 horas']
        })
        st.dataframe(actividades, hide_index=True, use_container_width=True)

elif seccion == "📈 Estadísticas":
    st.title("📈 Estadísticas Detalladas")
    
    tab1, tab2, tab3 = st.tabs(["📊 Ventas Mensuales", "🎯 Por Categoría", "📉 Comparativas"])
    
    with tab1:
        st.subheader("Ventas Mensuales del Año")
        df_ventas = generar_datos_ventas()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(df_ventas, x='Mes', y='Ventas', color='Ventas',
                        color_continuous_scale='blues')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.metric("Total Anual", f"${df_ventas['Ventas'].sum():,}")
            st.metric("Promedio Mensual", f"${df_ventas['Ventas'].mean():,.0f}")
            st.metric("Mejor Mes", df_ventas.loc[df_ventas['Ventas'].idxmax(), 'Mes'])
    
    with tab2:
        st.subheader("Distribución por Categoría")
        df_cat = generar_datos_categorias()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(df_cat, values='Ventas', names='Categoría', hole=0.4)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(df_cat, x='Categoría', y='Ventas', color='Categoría')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Análisis Comparativo")
        
        # Datos de comparación
        trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
        año_actual = np.random.randint(200000, 400000, 4)
        año_anterior = np.random.randint(180000, 350000, 4)
        
        df_comp = pd.DataFrame({
            'Trimestre': trimestres,
            '2024': año_actual,
            '2023': año_anterior
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_comp['Trimestre'], y=df_comp['2024'], name='2024'))
        fig.add_trace(go.Bar(x=df_comp['Trimestre'], y=df_comp['2023'], name='2023'))
        fig.update_layout(barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)

elif seccion == "👥 Usuarios":
    st.title("👥 Gestión de Usuarios")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Usuarios", "10,234")
    with col2:
        st.metric("Activos", "8,542")
    with col3:
        st.metric("Nuevos (mes)", "234")
    
    st.markdown("---")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_estado = st.selectbox("Filtrar por Estado", ["Todos", "Activo", "Inactivo", "Pendiente"])
    with col2:
        filtro_pais = st.selectbox("Filtrar por País", ["Todos", "España", "México", "Argentina", "Colombia", "Chile"])
    with col3:
        buscar = st.text_input("🔍 Buscar usuario", "")
    
    # Tabla de usuarios
    df_usuarios = generar_datos_usuarios()
    
    # Aplicar filtros
    if filtro_estado != "Todos":
        df_usuarios = df_usuarios[df_usuarios['Estado'] == filtro_estado]
    if filtro_pais != "Todos":
        df_usuarios = df_usuarios[df_usuarios['País'] == filtro_pais]
    if buscar:
        df_usuarios = df_usuarios[df_usuarios['Nombre'].str.contains(buscar, case=False)]
    
    st.dataframe(
        df_usuarios,
        use_container_width=True,
        height=400,
        column_config={
            "Estado": st.column_config.SelectboxColumn(
                "Estado",
                options=["Activo", "Inactivo", "Pendiente"]
            )
        }
    )
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Agregar Usuario", use_container_width=True):
            st.success("Función de agregar usuario")
    with col2:
        if st.button("📧 Enviar Email Masivo", use_container_width=True):
            st.info("Función de email masivo")
    with col3:
        if st.button("📥 Exportar CSV", use_container_width=True):
            st.success("Función de exportar")

elif seccion == "💰 Ventas":
    st.title("💰 Panel de Ventas")
    
    # Métricas de ventas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Ventas Hoy", "$45,230", "5.2%")
    with col2:
        st.metric("Ventas Semana", "$312,450", "12.3%")
    with col3:
        st.metric("Ventas Mes", "$1,245,890", "8.7%")
    with col4:
        st.metric("Ticket Promedio", "$142", "2.1%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Productos Más Vendidos")
        df_productos = generar_datos_productos()
        fig = px.bar(df_productos, x='Unidades Vendidas', y='Producto', 
                     orientation='h', color='Unidades Vendidas',
                     color_continuous_scale='greens')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💳 Métodos de Pago")
        metodos = pd.DataFrame({
            'Método': ['Tarjeta de Crédito', 'Transferencia', 'PayPal', 'Efectivo'],
            'Porcentaje': [45, 30, 15, 10]
        })
        fig = px.pie(metodos, values='Porcentaje', names='Método', hole=0.4)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📋 Últimas Transacciones")
    transacciones = pd.DataFrame({
        'ID': [f'TXN{i:04d}' for i in range(1001, 1011)],
        'Cliente': ['Cliente ' + str(i) for i in range(1, 11)],
        'Producto': np.random.choice(['Producto A', 'Producto B', 'Producto C', 'Producto D'], 10),
        'Monto': np.random.randint(50, 500, 10),
        'Estado': np.random.choice(['Completado', 'Pendiente', 'Cancelado'], 10)
    })
    st.dataframe(transacciones, use_container_width=True, hide_index=True)

elif seccion == "⚙️ Configuración":
    st.title("⚙️ Configuración del Sistema")
    
    tab1, tab2, tab3 = st.tabs(["🎨 Apariencia", "🔔 Notificaciones", "👤 Perfil"])
    
    with tab1:
        st.subheader("Personalización de Apariencia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tema = st.selectbox(
                "Seleccionar Tema",
                ["Claro", "Oscuro", "Auto"],
                index=["Claro", "Oscuro", "Auto"].index(st.session_state.theme)
            )
            st.session_state.theme = tema
            
            idioma = st.selectbox("Idioma", ["Español", "English", "Français", "Deutsch"])
            
            densidad = st.select_slider(
                "Densidad de Información",
                options=["Compacta", "Normal", "Espaciosa"],
                value="Normal"
            )
        
        with col2:
            st.info(f"**Tema actual:** {st.session_state.theme}")
            st.info(f"**Idioma:** {idioma}")
            st.info(f"**Densidad:** {densidad}")
        
        if st.button("💾 Guardar Cambios de Apariencia", use_container_width=True):
            st.success("✅ Configuración de apariencia guardada correctamente")
    
    with tab2:
        st.subheader("Configuración de Notificaciones")
        
        col1, col2 = st.columns(2)
        
        with col1:
            notif_email = st.checkbox("Notificaciones por Email", value=True)
            notif_push = st.checkbox("Notificaciones Push", value=st.session_state.notifications)
            notif_ventas = st.checkbox("Alertas de Ventas", value=True)
            notif_usuarios = st.checkbox("Alertas de Usuarios Nuevos", value=False)
        
        with col2:
            frecuencia = st.radio(
                "Frecuencia de Resumen",
                ["Diario", "Semanal", "Mensual"]
            )
            
            hora_resumen = st.time_input("Hora del Resumen Diario", datetime.now().time())
        
        st.session_state.notifications = notif_push
        
        if st.button("💾 Guardar Configuración de Notificaciones", use_container_width=True):
            st.success("✅ Configuración de notificaciones guardada correctamente")
    
    with tab3:
        st.subheader("Información del Perfil")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre Completo", "Administrador")
            email = st.text_input("Email", "admin@dashboard.com")
            telefono = st.text_input("Teléfono", "+34 600 000 000")
        
        with col2:
            cargo = st.text_input("Cargo", "Administrador del Sistema")
            departamento = st.selectbox("Departamento", ["TI", "Ventas", "Marketing", "Recursos Humanos"])
            zona_horaria = st.selectbox("Zona Horaria", ["GMT+1 (Madrid)", "GMT-5 (Ciudad de México)", "GMT-3 (Buenos Aires)"])
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Guardar Perfil", use_container_width=True):
                st.success("✅ Perfil actualizado correctamente")
        
        with col2:
            if st.button("🔑 Cambiar Contraseña", use_container_width=True):
                st.info("Redirigiendo a cambio de contraseña...")
        
        with col3:
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                st.warning("Sesión cerrada")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Dashboard Profesional v1.0 | © 2024 Todos los derechos reservados</div>",
    unsafe_allow_html=True
)