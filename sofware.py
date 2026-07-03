import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import warnings

# Ocultar advertencias de fragmentación de DataFrames
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURACIÓN GENERAL Y PERSISTENCIA DE DATOS
# ============================================================

STUDENTS_CSV = 'becarios.csv'
FOLLOWUPS_CSV = 'seguimientos.csv'

class SistemaBecasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Sistema Integral de Monitoreo de Becarios")
        self.root.geometry("1280x750")
        self.root.minsize(1100, 650)

        # 1. Inicialización de los datos (Cargar archivo físico o Generar Demo)
        self.estudiantes, self.seguimientos = self.cargar_datos()
        
        # 2. Configuración del diseño visual moderno (Estilos globales)
        # PRIMERO cargamos los estilos para que los widgets los encuentren al crearse
        self.configurar_estilos_interfaz()
        
        # 3. Construcción del contenedor principal de pestañas
        self.notebook = ttk.Notebook(root)
      
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Creación física de las pestañas
        self.tab_dashboard = ttk.Frame(self.notebook, style='Card.TFrame')
        self.tab_registro = ttk.Frame(self.notebook, style='Card.TFrame')
        self.tab_consulta = ttk.Frame(self.notebook, style='Card.TFrame')
        self.tab_reporte = ttk.Frame(self.notebook, style='Card.TFrame')
        
        self.notebook.add(self.tab_dashboard, text="  📊 Dashboard General  ")
        self.notebook.add(self.tab_registro, text="  📝 Panel de Registro  ")
        self.notebook.add(self.tab_consulta, text="  🔍 Buscador Avanzado  ")
        self.notebook.add(self.tab_reporte, text="  📄 Reportes Ejecutivos  ")
        
        # 4. Renderizado e inicialización de componentes visuales por pestaña
        self.configurar_dashboard()
        self.configurar_registro()
        self.configurar_consulta()
        self.configurar_reporte()
        
        # Renderizar datos en el Dashboard al arrancar el programa
        self.actualizar_dashboard()
        
    def configurar_estilos_interfaz(self):
        """Define la paleta de colores y la tipografía moderna de la aplicación"""
        self.root.configure(bg='#f4f6f9') # Fondo limpio grisáceo
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores de la paleta corporativa
        self.color_primario = '#1e3a8a'   # Azul Oscuro Ejecutivo
        self.color_secundario = '#3b82f6' # Azul Brillante Informativo
        self.color_exito = '#10b981'      # Verde Esmeralda
        self.color_alerta = '#f59e0b'     # Ámbar / Naranja
        self.color_fondo = '#f4f6f9'      # Fondo general
        
        # Estilos aplicados a componentes ttk
        self.style.configure('Modern.Notebook', background=self.color_fondo, borderwidth=0)
        self.style.configure('Modern.Notebook.Tab', 
                        background='#e2e8f0', 
                        foreground='#334155', 
                        font=('Segoe UI', 10, 'bold'), 
                        padding=[15, 6], 
                        borderwidth=0)
        
        self.style.map('Modern.Notebook.Tab', 
                  background=[('selected', self.color_primario)], 
                  foreground=[('selected', 'white')])
        
        self.style.configure('Card.TFrame', background='white', borderwidth=0, relief='flat')
        self.style.configure('TLabel', background='white', font=('Segoe UI', 10), foreground='#334155')
        self.style.configure('TCheckbutton', background='white', font=('Segoe UI', 10))
        
    def cargar_datos(self):
        """Carga los CSVs existentes o autogenera una base inteligente de 1000 estudiantes"""
        if os.path.exists(STUDENTS_CSV) and os.path.exists(FOLLOWUPS_CSV):
            estudiantes = pd.read_csv(STUDENTS_CSV)
            seguimientos = pd.read_csv(FOLLOWUPS_CSV)
            seguimientos['fecha'] = pd.to_datetime(seguimientos['fecha'])
            return estudiantes, seguimientos
        
        # Modo Demo Automatizado si no existen archivos
        np.random.seed(42)
        carreras = ['Ing. en Sistemas', 'Medicina', 'Derecho', 'Administración', 'Arquitectura', 
                    'Psicología', 'Contaduría Pública', 'Diseño Gráfico', 'Comunicaciones', 'Ing. Civil']
        
        estudiantes = pd.DataFrame({
            'student_id': range(1, 1001),
            'nombre': [f'Estudiante Alumno_{i}' for i in range(1, 1001)],
            'carrera': np.random.choice(carreras, 1000),
            'anio': np.random.choice([1, 2, 3, 4, 5], 1000, p=[0.2, 0.25, 0.25, 0.2, 0.1])
        })
        
        fechas = [datetime.now() - timedelta(days=np.random.randint(1, 180)) for _ in range(5000)]
        seguimientos = pd.DataFrame({
            'student_id': np.random.choice(range(1, 1001), 5000),
            'fecha': [f.strftime('%Y-%m-%d') for f in fechas],
            'tipo': np.random.choice(['Llamada', 'Presencial', 'Virtual'], 5000, p=[0.4, 0.35, 0.25]),
            'asistio_clase': np.random.choice([True, False], 5000, p=[0.80, 0.20]),
            'entrego_tareas': np.random.choice([True, False], 5000, p=[0.75, 0.25]),
            'act_voluntariado': np.random.choice([True, False], 5000, p=[0.65, 0.35]),
            'aprobo_parcial': np.random.choice([True, False], 5000, p=[0.70, 0.30]),
            'comentario': [f'Monitoreo rutinario número {i}' for i in range(5000)]
        })
        
        estudiantes.to_csv(STUDENTS_CSV, index=False)
        seguimientos.to_csv(FOLLOWUPS_CSV, index=False)
        seguimientos['fecha'] = pd.to_datetime(seguimientos['fecha'])
        return estudiantes, seguimientos
    
    def guardar_datos(self):
        """Guarda los cambios de forma síncrona en el almacenamiento local"""
        self.estudiantes.to_csv(STUDENTS_CSV, index=False)
        self.seguimientos.to_csv(FOLLOWUPS_CSV, index=False)
    
    # ============================================================
    # 📊 PESTAÑA 1: DASHBOARD DINÁMICO
    # ============================================================
    
    def configurar_dashboard(self):
        frame_filtros = tk.Frame(self.tab_dashboard, bg='#f8fafc', height=55)
        frame_filtros.pack(fill='x', side='top', ipady=8)
        
        tk.Label(frame_filtros, text=" 🔍 Filtrar Datos:", font=('Segoe UI', 10, 'bold'), bg='#f8fafc').pack(side='left', padx=15)
        
        años_reales = sorted(self.seguimientos['fecha'].dt.year.unique())
        valores_anio = ['Todos'] + [str(a) for a in años_reales]
        
        tk.Label(frame_filtros, text="Año Fiscal:", bg='#f8fafc').pack(side='left', padx=5)
        self.filtro_anio = ttk.Combobox(frame_filtros, values=valores_anio, width=10, state="readonly")
        self.filtro_anio.set('Todos')
        self.filtro_anio.pack(side='left', padx=5)
        
        tk.Label(frame_filtros, text="Mes Académico:", bg='#f8fafc').pack(side='left', padx=5)
        self.filtro_mes = ttk.Combobox(frame_filtros, values=['Todos'] + list(range(1, 13)), width=8, state="readonly")
        self.filtro_mes.set('Todos')
        self.filtro_mes.pack(side='left', padx=5)
        
        btn_actualizar = tk.Button(frame_filtros, text="🔄 Actualizar Gráficos", 
                                   command=self.actualizar_dashboard, 
                                   bg=self.color_secundario, fg='white', font=('Segoe UI', 9, 'bold'),
                                   relief='flat', padx=15, cursor='hand2')
        btn_actualizar.pack(side='left', padx=20)
        
        self.frame_kpis = tk.Frame(self.tab_dashboard, bg='white')
        self.frame_kpis.pack(fill='x', side='top', pady=5)
        
        self.frame_graficos = tk.Frame(self.tab_dashboard, bg='white')
        self.frame_graficos.pack(fill='both', expand=True, padx=10, pady=5)
    
    def actualizar_dashboard(self):
        for widget in self.frame_graficos.winfo_children(): widget.destroy()
        for widget in self.frame_kpis.winfo_children(): widget.destroy()
        
        df = self.seguimientos.copy()
        anio = self.filtro_anio.get()
        mes = self.filtro_mes.get()
        
        if anio != 'Todos': df = df[df['fecha'].dt.year == int(anio)]
        if mes != 'Todos': df = df[df['fecha'].dt.month == int(mes)]
        
        if df.empty:
            tk.Label(self.frame_graficos, text="⚠️ No se encontraron registros para los filtros seleccionados.", 
                    font=('Segoe UI', 13, 'bold'), fg='#94a3b8', bg='white').pack(expand=True)
            return
        
        metricas = df.groupby('student_id').agg(
            tasa_asistencia=('asistio_clase', 'mean'),
            tasa_tareas=('entrego_tareas', 'mean'),
            tasa_voluntariado=('act_voluntariado', 'mean'),
            tasa_aprobacion=('aprobo_parcial', 'mean')
        ).reset_index()
        
        metricas = metricas.merge(self.estudiantes[['student_id', 'nombre']], on='student_id')
        for col in ['tasa_asistencia', 'tasa_tareas', 'tasa_voluntariado', 'tasa_aprobacion']:
            metricas[col] = (metricas[col] * 100).round(1)
        
        metricas['rendimiento'] = metricas[['tasa_asistencia', 'tasa_tareas', 'tasa_voluntariado', 'tasa_aprobacion']].mean(axis=1).round(1)
        metricas = metricas.sort_values('rendimiento', ascending=False)
        
        rend_general_promedio = metricas['rendimiento'].mean()
        self.crear_tarjeta_kpi(self.frame_kpis, "Estudiantes Monitoreados", f"{len(metricas)} alumnos", self.color_primario)
        self.crear_tarjeta_kpi(self.frame_kpis, "Intervenciones Totales", f"{len(df)} registros", self.color_secundario)
        self.crear_tarjeta_kpi(self.frame_kpis, "Rendimiento Global Promedio", f"{rend_general_promedio:.1f}%", self.color_exito)
        
        sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#f8fafc", "figure.facecolor": "white"})
        fig = Figure(figsize=(12, 7), dpi=85)
        
        ax1 = fig.add_subplot(221)
        top10 = metricas.head(10)
        sns.barplot(x='rendimiento', y='nombre', data=top10, ax=ax1, palette="Blues_r")
        ax1.set_title('Top 10 Rendimiento de Excelencia', fontsize=11, fontweight='bold', color=self.color_primario)
        ax1.set_xlabel('Porcentaje General (%)', fontsize=9)
        ax1.set_ylabel('')
        ax1.tick_params(labelsize=8)
        
        ax2 = fig.add_subplot(222)
        promedios = metricas[['tasa_asistencia', 'tasa_tareas', 'tasa_voluntariado', 'tasa_aprobacion']].mean()
        promedios.index = ['Asistencia', 'Tareas', 'Voluntariado', 'Aprobación']
        sns.barplot(x=promedios.index, y=promedios.values, ax=ax2, palette="viridis")
        ax2.set_ylim(0, 100)
        ax2.set_title('Cumplimiento por Eje Indicador', fontsize=11, fontweight='bold', color=self.color_primario)
        ax2.tick_params(labelsize=9)
        for i, val in enumerate(promedios.values):
            ax2.text(i, val + 1, f'{val:.1f}%', ha='center', fontweight='bold', fontsize=9, color='#1e293b')
            
        ax3 = fig.add_subplot(223)
        tipos = df['tipo'].value_counts()
        ax3.pie(tipos.values, labels=tipos.index, autopct='%1.1f%%', startangle=140, 
                colors=['#60a5fa', '#34d399', '#fbbf24'], textprops={'fontsize': 9, 'fontweight': 'bold'})
        ax3.set_title('Canalización de Seguimientos', fontsize=11, fontweight='bold', color=self.color_primario)
        
        ax4 = fig.add_subplot(224)
        sns.histplot(metricas['rendimiento'], bins=12, kde=True, color='#8b5cf6', ax=ax4, edgecolor='white')
        ax4.set_title('Curva de Densidad de Rendimiento', fontsize=11, fontweight='bold', color=self.color_primario)
        ax4.set_xlabel('Escala Rendimiento (%)', fontsize=9)
        ax4.set_ylabel('Frecuencia Alumnos', fontsize=9)
        ax4.tick_params(labelsize=9)
        ax4.axvline(rend_general_promedio, color='red', linestyle='--', linewidth=1.5, label=f'Media: {rend_general_promedio:.1f}%')
        ax4.legend(fontsize=8)
        
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, self.frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
    def crear_tarjeta_kpi(self, master, titulo, valor, color_borde):
        card = tk.Frame(master, bg='#f8fafc', bd=0)
        card.pack(side='left', expand=True, fill='x', padx=15, pady=8)
        
        borde_izquierdo = tk.Frame(card, bg=color_borde, width=5)
        borde_izquierdo.pack(side='left', fill='y')
        
        contenido = tk.Frame(card, bg='#f8fafc', padx=10, pady=10)
        contenido.pack(side='left', fill='both', expand=True)
        
        lbl_tit = tk.Label(contenido, text=titulo.upper(), font=('Segoe UI', 8, 'bold'), fg='#64748b', bg='#f8fafc')
        lbl_tit.pack(anchor='w')
        lbl_val = tk.Label(contenido, text=valor, font=('Segoe UI', 14, 'bold'), fg='#1e293b', bg='#f8fafc')
        lbl_val.pack(anchor='w', pady=(2, 0))

    # ============================================================
    # 📝 PESTAÑA 2: CONTROL DE REGISTROS (ALUMNOS Y MONITOREOS)
    # ============================================================
    
    def configurar_registro(self):
        canvas_scroll = tk.Canvas(self.tab_registro, borderwidth=0, highlightthickness=0, bg='white')
        scrollbar = ttk.Scrollbar(self.tab_registro, orient="vertical", command=canvas_scroll.yview)
        scroll_frame = tk.Frame(canvas_scroll, bg='white')
        
        scroll_frame.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
        canvas_scroll.create_window((0,0), window=scroll_frame, anchor="nw", width=1100)
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        canvas_scroll.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        f_becario = tk.LabelFrame(scroll_frame, text=" 👤 ALTA NUEVA DE ESTUDIANTE BECARIO ", font=('Segoe UI', 11, 'bold'), fg=self.color_primario, bg='white', bd=1, relief='solid', padx=15, pady=15)
        f_becario.pack(fill='x', pady=15, padx=20)
        
        tk.Label(f_becario, text="Nombre Completo:", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=10)
        self.entry_nombre = tk.Entry(f_becario, width=35, font=('Segoe UI', 10), bd=1, relief='solid')
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(f_becario, text="Carrera Universitaria:", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=0, column=2, sticky='w', pady=10)
        self.entry_carrera = tk.Entry(f_becario, width=25, font=('Segoe UI', 10), bd=1, relief='solid')
        self.entry_carrera.grid(row=0, column=3, padx=10, pady=10)
        
        tk.Label(f_becario, text="Año Académico:", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=0, column=4, sticky='w', pady=10)
        self.entry_anio = ttk.Combobox(f_becario, values=['1', '2', '3', '4', '5'], width=8, state="readonly")
        self.entry_anio.grid(row=0, column=5, padx=10, pady=10)
        
        btn_reg_becario = tk.Button(f_becario, text="➕ Guardar Estudiante", command=self.registrar_becario, 
                                    bg=self.color_exito, fg='white', font=('Segoe UI', 10, 'bold'), relief='flat', padx=15, cursor='hand2')
        btn_reg_becario.grid(row=0, column=6, padx=15, pady=10)
        
        f_seguimiento = tk.LabelFrame(scroll_frame, text=" 📝 HOJA DE SEGUIMIENTO Y MONITOREO PERIÓDICO ", font=('Segoe UI', 11, 'bold'), fg=self.color_primario, bg='white', bd=1, relief='solid', padx=15, pady=15)
        f_seguimiento.pack(fill='x', pady=15, padx=20)
        
        tk.Label(f_seguimiento, text="ID de Registro Becario:", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=8)
        self.entry_id = tk.Entry(f_seguimiento, width=12, font=('Segoe UI', 10), bd=1, relief='solid')
        self.entry_id.grid(row=0, column=1, sticky='w', padx=10, pady=8)
        
        tk.Label(f_seguimiento, text="Método / Canal:", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=0, column=2, sticky='w', pady=8)
        self.entry_tipo = ttk.Combobox(f_seguimiento, values=['Llamada', 'Presencial', 'Virtual'], width=15, state="readonly")
        self.entry_tipo.grid(row=0, column=3, sticky='w', padx=10, pady=8)
        
        lbl_eval = tk.Label(f_seguimiento, text="Métricas de Cumplimiento Evaluadas en la Sesión:", font=('Segoe UI', 10, 'bold', 'underline'), bg='white')
        lbl_eval.grid(row=1, column=0, columnspan=4, sticky='w', pady=(20, 10))
        
        self.var_asistio = tk.BooleanVar()
        self.var_tareas = tk.BooleanVar()
        self.var_voluntariado = tk.BooleanVar()
        self.var_aprobo = tk.BooleanVar()
        
        chk_1 = ttk.Checkbutton(f_seguimiento, text="Asistencia Regular a Clases", variable=self.var_asistio)
        chk_1.grid(row=2, column=0, sticky='w', padx=5, pady=6)
        chk_2 = ttk.Checkbutton(f_seguimiento, text="Entrega de Tareas al Día", variable=self.var_tareas)
        chk_2.grid(row=2, column=2, sticky='w', padx=5, pady=6)
        chk_3 = ttk.Checkbutton(f_seguimiento, text="Horas de Voluntariado Cubiertas", variable=self.var_voluntariado)
        chk_3.grid(row=3, column=0, sticky='w', padx=5, pady=6)
        chk_4 = ttk.Checkbutton(f_seguimiento, text="Aprobación de Evaluaciones Parciales", variable=self.var_aprobo)
        chk_4.grid(row=3, column=2, sticky='w', padx=5, pady=6)
        
        tk.Label(f_seguimiento, text="Notas / Observación:", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=4, column=0, sticky='nw', pady=(20, 5))
        self.entry_comentario = tk.Entry(f_seguimiento, width=65, font=('Segoe UI', 10), bd=1, relief='solid')
        self.entry_comentario.grid(row=4, column=1, columnspan=3, sticky='w', pady=(20, 5), padx=10)
        
        btn_reg_seguimiento = tk.Button(f_seguimiento, text="📝 Asentar Seguimiento", command=self.registrar_seguimiento, 
                                        bg=self.color_secundario, fg='white', font=('Segoe UI', 10, 'bold'), relief='flat', padx=20, pady=5, cursor='hand2')
        btn_reg_seguimiento.grid(row=5, column=3, sticky='e', pady=20, padx=10)
        
    def registrar_becario(self):
        nombre = self.entry_nombre.get().strip()
        carrera = self.entry_carrera.get().strip()
        anio = self.entry_anio.get()
        
        if not nombre or not carrera or not anio:
            messagebox.showerror("Campos Incompletos", "Por favor, llene toda la información requerida del estudiante.")
            return
        
        nuevo_id = int(self.estudiantes['student_id'].max() + 1)
        nuevo_df = pd.DataFrame({'student_id': [nuevo_id], 'nombre': [nombre], 'carrera': [carrera], 'anio': [int(anio)]})
        
        self.estudiantes = pd.concat([self.estudiantes, nuevo_df], ignore_index=True)
        self.guardar_datos()
        messagebox.showinfo("Operación Exitosa", f"Estudiante guardado.\nID Asignado Único: {nuevo_id}")
        
        self.entry_nombre.delete(0, tk.END)
        self.entry_carrera.delete(0, tk.END)
        self.entry_anio.set('')
        self.actualizar_dashboard()
        self.configurar_reporte()
        
    def registrar_seguimiento(self):
        try:
            raw_id = self.entry_id.get().strip()
            if not raw_id:
                messagebox.showerror("Error de Entrada", "El ID del becario no puede estar vacío.")
                return
                
            student_id = int(raw_id)
            if student_id not in self.estudiantes['student_id'].values:
                messagebox.showerror("Error de Búsqueda", "El ID ingresado no coincide con ningún becario registrado.")
                return
            
            tipo = self.entry_tipo.get()
            if not tipo:
                messagebox.showerror("Falta Parámetro", "Por favor seleccione el canal de comunicación (Tipo).")
                return
            
            nuevo_seg = pd.DataFrame({
                'student_id': [student_id],
                'fecha': [datetime.now()],
                'tipo': [tipo],
                'asistio_clase': [self.var_asistio.get()],
                'entrego_tareas': [self.var_tareas.get()],
                'act_voluntariado': [self.var_voluntariado.get()],
                'aprobo_parcial': [self.var_aprobo.get()],
                'comentario': [self.entry_comentario.get().strip() or 'Auditoría ordinaria sin anomalías']
            })
            
            self.seguimientos = pd.concat([self.seguimientos, nuevo_seg], ignore_index=True)
            self.guardar_datos()
            messagebox.showinfo("Proceso Completado", "El seguimiento técnico ha sido añadido al historial histórico.")
            
            self.entry_id.delete(0, tk.END)
            self.entry_tipo.set('')
            self.var_asistio.set(False)
            self.var_tareas.set(False)
            self.var_voluntariado.set(False)
            self.var_aprobo.set(False)
            self.entry_comentario.delete(0, tk.END)
            self.actualizar_dashboard()
            self.configurar_reporte()
            
        except ValueError:
            messagebox.showerror("Error Crítico", "El ID debe ser exclusivamente un valor numérico entero.")

    # ============================================================
    # 🔍 PESTAÑA 3: MOTOR DE CONSULTA AVANZADA
    # ============================================================
    
    def configurar_consulta(self):
        frame_consulta = tk.Frame(self.tab_consulta, bg='white')
        frame_consulta.pack(fill='both', expand=True, padx=20, pady=15)
        
        barra_herramientas = tk.Frame(frame_consulta, bg='#f8fafc', padx=10, pady=10)
        barra_herramientas.pack(fill='x', side='top', pady=(0, 15))
        
        tk.Label(barra_herramientas, text="Número ID de Alumno:", font=('Segoe UI', 10, 'bold'), bg='#f8fafc').pack(side='left', padx=10)
        self.entry_buscar = tk.Entry(barra_herramientas, width=15, font=('Segoe UI', 11), bd=1, relief='solid')
        self.entry_buscar.pack(side='left', padx=5)
        self.entry_buscar.bind('<Return>', lambda event: self.buscar_becario())
        
        btn_buscar = tk.Button(barra_herramientas, text="🔍 Ejecutar Búsqueda", command=self.buscar_becario, 
                               bg=self.color_secundario, fg='white', font=('Segoe UI', 9, 'bold'), relief='flat', padx=15, cursor='hand2')
        btn_buscar.pack(side='left', padx=10)
        
        btn_limpiar = tk.Button(barra_herramientas, text="🗑️ Limpiar Pantalla", command=self.limpiar_consulta, 
                               bg='#64748b', fg='white', font=('Segoe UI', 9, 'bold'), relief='flat', padx=15, cursor='hand2')
        btn_limpiar.pack(side='left', padx=5)
        
        self.text_consulta = scrolledtext.ScrolledText(frame_consulta, height=22, font=('Consolas', 11), 
                                                       bg='#1e293b', fg='#f8fafc', insertbackground='white', padx=15, pady=15)
        self.text_consulta.pack(fill='both', expand=True)
        self.text_consulta.insert(tk.END, "💡 Escriba el ID de un becario y presione 'Buscar' para auditar su expediente completo...")
    
    def buscar_becario(self):
        try:
            input_val = self.entry_buscar.get().strip()
            if not input_val: return
            
            student_id = int(input_val)
            estudiante = self.estudiantes[self.estudiantes['student_id'] == student_id]
            
            if estudiante.empty:
                self.text_consulta.delete(1.0, tk.END)
                self.text_consulta.insert(tk.END, f"❌ ERROR: El código de estudiante #{student_id} no está registrado en el sistema.")
                return
            
            self.text_consulta.delete(1.0, tk.END)
            
            self.text_consulta.insert(tk.END, f"╔══════════════════════════════════════════════════════════╗\n")
            self.text_consulta.insert(tk.END, f"║            EXPEDIENTE ACADÉMICO DEL ESTUDIANTE           ║\n")
            self.text_consulta.insert(tk.END, f"╚══════════════════════════════════════════════════════════╝\n\n")
            
            self.text_consulta.insert(tk.END, f" ▪️ ID UNICO:       {estudiante['student_id'].values[0]}\n")
            self.text_consulta.insert(tk.END, f" ▪️ NOMBRE:         {estudiante['nombre'].values[0]}\n")
            self.text_consulta.insert(tk.END, f" ▪️ CARRERA:        {estudiante['carrera'].values[0]}\n")
            self.text_consulta.insert(tk.END, f" ▪️ AÑO ACTUAL:     {estudiante['anio'].values[0]}° Año Universitario\n\n")
            
            segs = self.seguimientos[self.seguimientos['student_id'] == student_id]
            self.text_consulta.insert(tk.END, f" 📊 HISTORIAL DE INTERVENCIONES: {len(segs)} evaluaciones hechas\n")
            self.text_consulta.insert(tk.END, "═"*75 + "\n")
            
            if not segs.empty:
                ultimos = segs.sort_values('fecha', ascending=False).head(8)
                for index, row in ultimos.iterrows():
                    fecha_str = row['fecha'].strftime('%Y-%m-%d')
                    self.text_consulta.insert(tk.END, f" 📅 Fecha: {fecha_str} | Canal: {row['tipo']}\n")
                    
                    c_asist = '✅ SI' if row['asistio_clase'] else '❌ NO'
                    c_tarea = '✅ SI' if row['entrego_tareas'] else '❌ NO'
                    c_volun = '✅ SI' if row['act_voluntariado'] else '❌ NO'
                    c_aprob = '✅ SI' if row['aprobo_parcial'] else '❌ NO'
                    
                    self.text_consulta.insert(tk.END, f"   ├─ Asistencia:  {c_asist:6} | Tareas:     {c_tarea}\n")
                    self.text_consulta.insert(tk.END, f"   ├─ Voluntario:  {c_volun:6} | Aprobación: {c_aprob}\n")
                    self.text_consulta.insert(tk.END, f"   └─ Comentario:  \"{row['comentario']}\"\n\n")
            else:
                self.text_consulta.insert(tk.END, " ⚠️ ATENCIÓN: El alumno no cuenta con bitácoras de seguimiento cargadas.\n")
                
        except ValueError:
            messagebox.showerror("Dato Inválido", "Por favor introduzca únicamente caracteres numéricos.")
            
    def limpiar_consulta(self):
        self.entry_buscar.delete(0, tk.END)
        self.text_consulta.delete(1.0, tk.END)

    # ============================================================
    # 📄 PESTAÑA 4: COMPILADOR DE REPORTES Y EXPORTACIÓN PDF
    # ============================================================
    
    def configurar_reporte(self):
        # Limpiar elementos previos si se vuelve a invocar
        for widget in self.tab_reporte.winfo_children(): widget.destroy()

        frame_reporte = tk.Frame(self.tab_reporte, bg='white')
        frame_reporte.pack(fill='both', expand=True, padx=20, pady=15)
        
        frame_filtros = tk.LabelFrame(frame_reporte, text=" 📄 Parametrización del Reporte Mensual ", font=('Segoe UI', 10, 'bold'), fg=self.color_primario, bg='white', padx=15, pady=15)
        frame_filtros.pack(fill='x', side='top', pady=(0, 15))
        
        años_reales = sorted(self.seguimientos['fecha'].dt.year.unique())
        
        tk.Label(frame_filtros, text="Año de Evaluación:", bg='white').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.reporte_anio = ttk.Combobox(frame_filtros, values=[str(a) for a in años_reales], width=12, state="readonly")
        self.reporte_anio.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(frame_filtros, text="Mes de Evaluación:", bg='white').grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.reporte_mes = ttk.Combobox(frame_filtros, values=list(range(1, 13)), width=8, state="readonly")
        self.reporte_mes.grid(row=0, column=3, padx=10, pady=5)
        
        btn_generar = tk.Button(frame_filtros, text="📄 Compilar & Exportar PDF", command=self.generar_reporte, 
                                bg=self.color_alerta, fg='white', font=('Segoe UI', 10, 'bold'), relief='flat', padx=20, cursor='hand2')
        btn_generar.grid(row=0, column=4, padx=25, pady=5)
        
        tk.Label(frame_reporte, text="Vista previa de datos estructurados para exportar:", font=('Segoe UI', 9, 'bold'), fg='#64748b', bg='white').pack(anchor='w')
        self.text_reporte = scrolledtext.ScrolledText(frame_reporte, height=16, font=('Consolas', 10), bg='#f8fafc', fg='#334155', bd=1, relief='solid', padx=10, pady=10)
        self.text_reporte.pack(fill='both', expand=True, pady=5)
        
        tk.Label(frame_reporte, text="💡 Los informes ejecutivos se graban automáticamente en formato de alta definición (.pdf) en el directorio raíz del software.", 
                 font=('Segoe UI', 9, 'italic'), fg=self.color_secundario, bg='white').pack(pady=5)
        
    def generar_reporte(self):
        try:
            anio = self.reporte_anio.get()
            mes = self.reporte_mes.get()
            
            if not anio or not mes:
                messagebox.showerror("Error de Filtro", "Debe fijar un año y un mes válidos para levantar el reporte.")
                return
            
            anio, mes = int(anio), int(mes)
            df = self.seguimientos[(self.seguimientos['fecha'].dt.year == anio) & (self.seguimientos['fecha'].dt.month == mes)]
            
            if df.empty:
                messagebox.showwarning("Cero Registros", f"No se han hallado registros de bitácoras académicas para el periodo {anio}/{mes:02d}.")
                return
            
            metricas = df.groupby('student_id').agg(
                total_seguimientos=('fecha', 'count'),
                tasa_asistencia=('asistio_clase', 'mean'),
                tasa_tareas=('entrego_tareas', 'mean'),
                tasa_voluntariado=('act_voluntariado', 'mean'),
                tasa_aprobacion=('aprobo_parcial', 'mean')
            ).reset_index()
            
            metricas = metricas.merge(self.estudiantes[['student_id', 'nombre', 'carrera', 'anio']], on='student_id')
            for col in ['tasa_asistencia', 'tasa_tareas', 'tasa_voluntariado', 'tasa_aprobacion']:
                metricas[col] = (metricas[col] * 100).round(1)
            
            metricas['rendimiento'] = metricas[['tasa_asistencia', 'tasa_tareas', 'tasa_voluntariado', 'tasa_aprobacion']].mean(axis=1).round(1)
            metricas = metricas.sort_values('rendimiento', ascending=False)
            
            self.text_reporte.delete(1.0, tk.END)
            self.text_reporte.insert(tk.END, f"===============================================================================\n")
            self.text_reporte.insert(tk.END, f"📄 RESUMEN TÉCNICO DE AUDITORÍA ACADÉMICA - PERIODO: {anio}/{mes:02d}\n")
            self.text_reporte.insert(tk.END, f"===============================================================================\n\n")
            self.text_reporte.insert(tk.END, f"  🔹 Volumen de Alumnos Muestreados: {len(metricas)} estudiantes\n")
            self.text_reporte.insert(tk.END, f"  🔹 Total de Evaluaciones Médias:   {len(df)} registros\n")
            self.text_reporte.insert(tk.END, f"  🔹 Eficiencia Promedio del Grupo:  {metricas['rendimiento'].mean():.1f}%\n\n")
            self.text_reporte.insert(tk.END, f"-------------------------------------------------------------------------------\n")
            self.text_reporte.insert(tk.END, f"📋 TABLA DE RENDIMIENTO TOP 10 (MUESTRA DE EXCELENCIA):\n")
            self.text_reporte.insert(tk.END, f"-------------------------------------------------------------------------------\n")
            
            for _, row in metricas.head(10).iterrows():
                self.text_reporte.insert(tk.END, f"  ▪️ {row['nombre']:24} | {row['carrera']:22} | Rend: {row['rendimiento']:.1f}%\n")
            
            self.generar_pdf(metricas, df, anio, mes)
            messagebox.showinfo("Reporte Exportado", f"El archivo 'reporte_becas_{anio}_{mes:02d}.pdf' ha sido creado de forma exitosa.")
            
        except Exception as e:
            messagebox.showerror("Fallo de Renderizado", f"No se pudo escribir el reporte PDF debido a:\n{str(e)}")
            
    def generar_pdf(self, metricas, df, anio, mes):
        """Genera un reporte PDF vectorial limpio y balanceado con fuentes compactas"""
        from matplotlib.backends.backend_pdf import PdfPages
        
        with PdfPages(f'reporte_becas_{anio}_{mes:02d}.pdf') as pdf:
            fig1, ax1 = plt.subplots(figsize=(11, 8.5))
            ax1.axis('tight')
            ax1.axis('off')
            
            tabla_datos = metricas.head(22)[['nombre', 'carrera', 'anio', 'total_seguimientos', 
                                       'tasa_asistencia', 'tasa_tareas', 'tasa_voluntariado', 
                                       'tasa_aprobacion', 'rendimiento']]
            tabla_datos.columns = ['Nombre Estudiante', 'Carrera', 'Año', 'Monit.', 'Asist %', 'Tareas %', 'Vol %', 'Aprob %', 'Rend %']
            
            ui_table = ax1.table(cellText=tabla_datos.values, colLabels=tabla_datos.columns, loc='center', cellLoc='center')
            ui_table.auto_set_font_size(False)
            ui_table.set_fontsize(7.5) 
            ui_table.scale(1.0, 1.4)
            
            ax1.set_title(f'INFORME ANALÍTICO DE RENDIMIENTO DE BECARIOS (PERIODO: {anio} - MES: {mes:02d})', 
                          fontsize=13, fontweight='bold', color='#1e3a8a', pad=25)
            pdf.savefig(fig1, bbox_inches='tight')
            plt.close(fig1)
            
            fig2, axes = plt.subplots(2, 2, figsize=(13, 9.5))
            fig2.suptitle(f'Métricas Estadísticas del Periodo - {anio}/{mes:02d}', fontsize=15, fontweight='bold', color='#1e3a8a')
            
            ax_sub1 = axes[0, 0]
            top10 = metricas.head(10)
            sns.barplot(x='rendimiento', y='nombre', data=top10, ax=ax_sub1, palette="Blues_r")
            ax_sub1.set_title('Top 10 Rendimientos más Sobresalientes', fontsize=10, fontweight='bold')
            ax_sub1.set_xlabel('Rendimiento (%)', fontsize=8)
            ax_sub1.set_ylabel('')
            ax_sub1.tick_params(axis='y', labelsize=7) 
            
            ax_sub2 = axes[0, 1]
            promedios = metricas[['tasa_asistencia', 'tasa_tareas', 'tasa_voluntariado', 'tasa_aprobacion']].mean()
            promedios.index = ['Asistencia', 'Tareas', 'Voluntariado', 'Aprobación']
            ax_sub2.bar(promedios.index, promedios.values, color=['#2ecc71', '#3498db', '#f1c40f', '#e74c3c'], edgecolor='none', width=0.5)
            ax_sub2.set_ylim(0, 100)
            ax_sub2.set_title('Medias Generales por Indicador de Beca', fontsize=10, fontweight='bold')
            ax_sub2.tick_params(labelsize=8)
            for i, v in enumerate(promedios.values):
                ax_sub2.text(i, v + 1.5, f'{v:.1f}%', ha='center', fontsize=8, fontweight='bold')
            
            ax_sub3 = axes[1, 0]
            tipos = df['tipo'].value_counts()
            ax_sub3.pie(tipos.values, labels=tipos.index, autopct='%1.1f%%', startangle=90, 
                        colors=['#60a5fa', '#34d399', '#fbbf24'], textprops={'fontsize': 8, 'fontweight': 'bold'})
            ax_sub3.set_title('Uso Relativo de Canales de Monitoreo', fontsize=10, fontweight='bold')
            
            ax_sub4 = axes[1, 1]
            ax_sub4.hist(metricas['rendimiento'], bins=10, color='#8b5cf6', alpha=0.75, edgecolor='white')
            ax_sub4.set_title('Distribución Grupal de Rendimiento', fontsize=10, fontweight='bold')
            ax_sub4.set_xlabel('Porcentaje General (%)', fontsize=8)
            ax_sub4.axvline(metricas['rendimiento'].mean(), color='red', linestyle='--', linewidth=1.2)
            ax_sub4.tick_params(labelsize=8)
            
            plt.tight_layout(pad=3.0)
            pdf.savefig(fig2, bbox_inches='tight')
            plt.close(fig2)

# ============================================================
# ARRANQUE DE LA APLICACIÓN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaBecasGUI(root)
    root.mainloop()