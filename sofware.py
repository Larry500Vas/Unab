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
from tkinter import font as tkfont
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURACIÓN Y CARGA DE DATOS
# ============================================================

STUDENTS_CSV = 'becarios.csv'
FOLLOWUPS_CSV = 'seguimientos.csv'

class SistemaBecasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Monitoreo de Becarios - 1000 Estudiantes")
        self.root.geometry("1200x700")
        
        # Cargar datos
        self.estudiantes, self.seguimientos = self.cargar_datos()
        
        # Configurar estilo
        self.root.configure(bg='#f0f0f0')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Crear pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Pestañas
        self.tab_dashboard = ttk.Frame(self.notebook)
        self.tab_registro = ttk.Frame(self.notebook)
        self.tab_consulta = ttk.Frame(self.notebook)
        self.tab_reporte = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_dashboard, text="📊 Dashboard")
        self.notebook.add(self.tab_registro, text="📝 Registro")
        self.notebook.add(self.tab_consulta, text="🔍 Consulta")
        self.notebook.add(self.tab_reporte, text="📄 Reportes")
        
        # Configurar cada pestaña
        self.configurar_dashboard()
        self.configurar_registro()
        self.configurar_consulta()
        self.configurar_reporte()
        
        # Mostrar dashboard al iniciar
        self.actualizar_dashboard()
    
    def cargar_datos(self):
        """Carga o genera datos de prueba"""
        if os.path.exists(STUDENTS_CSV) and os.path.exists(FOLLOWUPS_CSV):
            estudiantes = pd.read_csv(STUDENTS_CSV)
            seguimientos = pd.read_csv(FOLLOWUPS_CSV)
            seguimientos['fecha'] = pd.to_datetime(seguimientos['fecha'])
            return estudiantes, seguimientos
        
        # Generar datos de prueba
        print("Generando datos de prueba...")
        np.random.seed(42)
        
        carreras = ['Ing. Sistemas', 'Medicina', 'Derecho', 'Administración', 'Arquitectura', 
                    'Psicología', 'Contaduría', 'Diseño', 'Comunicación', 'Ing. Civil']
        estudiantes = pd.DataFrame({
            'student_id': range(1, 1001),
            'nombre': [f'Becario_{i}' for i in range(1, 1001)],
            'carrera': np.random.choice(carreras, 1000),
            'anio': np.random.choice([1, 2, 3, 4, 5], 1000, p=[0.2, 0.25, 0.25, 0.2, 0.1])
        })
        
        fechas = [datetime.now() - timedelta(days=np.random.randint(1, 180)) for _ in range(5000)]
        seguimientos = pd.DataFrame({
            'student_id': np.random.choice(range(1, 1001), 5000),
            'fecha': [f.strftime('%Y-%m-%d') for f in fechas],
            'tipo': np.random.choice(['Llamada', 'Presencial', 'Virtual'], 5000, p=[0.4, 0.35, 0.25]),
            'asistio_clase': np.random.choice([True, False], 5000, p=[0.78, 0.22]),
            'entrego_tareas': np.random.choice([True, False], 5000, p=[0.72, 0.28]),
            'act_voluntariado': np.random.choice([True, False], 5000, p=[0.68, 0.32]),
            'aprobo_parcial': np.random.choice([True, False], 5000, p=[0.63, 0.37]),
            'comentario': [f'Seg #{i}' for i in range(5000)]
        })
        
        estudiantes.to_csv(STUDENTS_CSV, index=False)
        seguimientos.to_csv(FOLLOWUPS_CSV, index=False)
        seguimientos['fecha'] = pd.to_datetime(seguimientos['fecha'])
        return estudiantes, seguimientos
    
    def guardar_datos(self):
        """Guarda los datos actuales"""
        self.estudiantes.to_csv(STUDENTS_CSV, index=False)
        self.seguimientos.to_csv(FOLLOWUPS_CSV, index=False)
        messagebox.showinfo("Éxito", "Datos guardados correctamente")
    
    # ============================================================
    # PESTAÑA 1: DASHBOARD
    # ============================================================
    
    def configurar_dashboard(self):
        # Frame superior con filtros
        frame_filtros = tk.Frame(self.tab_dashboard, bg='#f0f0f0')
        frame_filtros.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_filtros, text="Filtros:", font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(side='left', padx=5)
        
        # Año
        tk.Label(frame_filtros, text="Año:", bg='#f0f0f0').pack(side='left', padx=5)
        self.filtro_anio = ttk.Combobox(frame_filtros, values=['Todos'] + list(range(2020, 2027)), width=8)
        self.filtro_anio.set('Todos')
        self.filtro_anio.pack(side='left', padx=5)
        
        # Mes
        tk.Label(frame_filtros, text="Mes:", bg='#f0f0f0').pack(side='left', padx=5)
        self.filtro_mes = ttk.Combobox(frame_filtros, values=['Todos'] + list(range(1, 13)), width=5)
        self.filtro_mes.set('Todos')
        self.filtro_mes.pack(side='left', padx=5)
        
        # Botón actualizar
        btn_actualizar = tk.Button(frame_filtros, text="🔄 Actualizar", 
                                   command=self.actualizar_dashboard, 
                                   bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
        btn_actualizar.pack(side='left', padx=10)
        
        # Frame para gráficos
        self.frame_graficos = tk.Frame(self.tab_dashboard, bg='white')
        self.frame_graficos.pack(fill='both', expand=True, padx=10, pady=5)
    
    def actualizar_dashboard(self):
        # Limpiar frame anterior
        for widget in self.frame_graficos.winfo_children():
            widget.destroy()
        
        # Aplicar filtros
        df = self.seguimientos.copy()
        anio = self.filtro_anio.get()
        mes = self.filtro_mes.get()
        
        if anio != 'Todos':
            df = df[df['fecha'].dt.year == int(anio)]
        if mes != 'Todos':
            df = df[df['fecha'].dt.month == int(mes)]
        
        if df.empty:
            tk.Label(self.frame_graficos, text="⚠️ No hay datos para los filtros seleccionados", 
                    font=('Arial', 14), fg='red').pack(expand=True)
            return
        
        # Calcular métricas
        metricas = df.groupby('student_id').agg(
            total_seguimientos=('fecha', 'count'),
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
        
        # Crear figura con 2x2 gráficos
        fig = Figure(figsize=(12, 8), dpi=80)
        
        # Gráfico 1: Top 10 rendimiento
        ax1 = fig.add_subplot(221)
        top10 = metricas.head(10)
        ax1.barh(top10['nombre'], top10['rendimiento'], color='skyblue')
        ax1.set_xlabel('Rendimiento %')
        ax1.set_title('Top 10 Mejores Rendimientos')
        ax1.invert_yaxis()
        
        # Gráfico 2: Promedios generales
        ax2 = fig.add_subplot(222)
        promedios = metricas[['tasa_asistencia', 'tasa_tareas', 'tasa_voluntariado', 'tasa_aprobacion']].mean()
        colores = ['#2ecc71', '#3498db', '#f1c40f', '#e74c3c']
        ax2.bar(promedios.index, promedios.values, color=colores)
        ax2.set_ylim(0, 100)
        ax2.set_title('Promedio General por Indicador')
        ax2.set_ylabel('Porcentaje %')
        for i, v in enumerate(promedios.values):
            ax2.text(i, v + 1, f'{v:.1f}%', ha='center')
        
        # Gráfico 3: Distribución por tipo
        ax3 = fig.add_subplot(223)
        tipos = df['tipo'].value_counts()
        ax3.pie(tipos.values, labels=tipos.index, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Distribución por Tipo de Seguimiento')
        
        # Gráfico 4: Histograma rendimiento
        ax4 = fig.add_subplot(224)
        ax4.hist(metricas['rendimiento'], bins=10, color='purple', alpha=0.7, edgecolor='black')
        ax4.set_xlabel('Rendimiento %')
        ax4.set_ylabel('Cantidad')
        ax4.set_title('Distribución del Rendimiento')
        ax4.axvline(metricas['rendimiento'].mean(), color='red', linestyle='dashed', label='Promedio')
        ax4.legend()
        
        fig.tight_layout()
        
        # Incrustar en tkinter
        canvas = FigureCanvasTkAgg(fig, self.frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Mostrar estadísticas
        frame_stats = tk.Frame(self.tab_dashboard, bg='#f0f0f0')
        frame_stats.pack(fill='x', padx=10, pady=5)
        
        stats = f"📊 Total estudiantes: {len(self.estudiantes)} | Total seguimientos: {len(df)} | Rendimiento promedio: {metricas['rendimiento'].mean():.1f}%"
        tk.Label(frame_stats, text=stats, font=('Arial', 10), bg='#f0f0f0').pack()
    
    # ============================================================
    # PESTAÑA 2: REGISTRO
    # ============================================================
    
    def configurar_registro(self):
        # Frame para registro de becario
        frame_becario = tk.LabelFrame(self.tab_registro, text="Registrar Nuevo Becario", font=('Arial', 10, 'bold'))
        frame_becario.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_becario, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_becario, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_becario, text="Carrera:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_carrera = tk.Entry(frame_becario, width=20)
        self.entry_carrera.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_becario, text="Año:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_anio = ttk.Combobox(frame_becario, values=[1,2,3,4,5], width=5)
        self.entry_anio.grid(row=0, column=5, padx=5, pady=5)
        
        btn_registrar = tk.Button(frame_becario, text="✅ Registrar Becario", 
                                  command=self.registrar_becario, bg='#4CAF50', fg='white')
        btn_registrar.grid(row=0, column=6, padx=10, pady=5)
        
        # Separador
        ttk.Separator(self.tab_registro, orient='horizontal').pack(fill='x', padx=10, pady=10)
        
        # Frame para registro de seguimiento
        frame_seguimiento = tk.LabelFrame(self.tab_registro, text="Registrar Seguimiento", font=('Arial', 10, 'bold'))
        frame_seguimiento.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_seguimiento, text="ID Becario:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(frame_seguimiento, width=10)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_seguimiento, text="Tipo:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_tipo = ttk.Combobox(frame_seguimiento, values=['Llamada', 'Presencial', 'Virtual'], width=10)
        self.entry_tipo.grid(row=0, column=3, padx=5, pady=5)
        
        # Checkboxes
        self.var_asistio = tk.BooleanVar()
        self.var_tareas = tk.BooleanVar()
        self.var_voluntariado = tk.BooleanVar()
        self.var_aprobo = tk.BooleanVar()
        
        tk.Checkbutton(frame_seguimiento, text="Asistió a clases", variable=self.var_asistio).grid(row=1, column=0, padx=5, pady=5)
        tk.Checkbutton(frame_seguimiento, text="Entregó tareas", variable=self.var_tareas).grid(row=1, column=1, padx=5, pady=5)
        tk.Checkbutton(frame_seguimiento, text="Hizo voluntariado", variable=self.var_voluntariado).grid(row=1, column=2, padx=5, pady=5)
        tk.Checkbutton(frame_seguimiento, text="Aprobó parcial", variable=self.var_aprobo).grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(frame_seguimiento, text="Comentario:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_comentario = tk.Entry(frame_seguimiento, width=50)
        self.entry_comentario.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        
        btn_seguimiento = tk.Button(frame_seguimiento, text="📝 Registrar Seguimiento", 
                                    command=self.registrar_seguimiento, bg='#2196F3', fg='white')
        btn_seguimiento.grid(row=2, column=4, padx=10, pady=5)
    
    def registrar_becario(self):
        nombre = self.entry_nombre.get().strip()
        carrera = self.entry_carrera.get().strip()
        anio = self.entry_anio.get()
        
        if not nombre or not carrera or not anio:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        nuevo_id = self.estudiantes['student_id'].max() + 1
        nuevo = pd.DataFrame({
            'student_id': [nuevo_id],
            'nombre': [nombre],
            'carrera': [carrera],
            'anio': [int(anio)]
        })
        self.estudiantes = pd.concat([self.estudiantes, nuevo], ignore_index=True)
        self.guardar_datos()
        messagebox.showinfo("Éxito", f"Becario {nombre} registrado con ID {nuevo_id}")
        
        # Limpiar campos
        self.entry_nombre.delete(0, tk.END)
        self.entry_carrera.delete(0, tk.END)
        self.entry_anio.set('')
    
    def registrar_seguimiento(self):
        try:
            student_id = int(self.entry_id.get().strip())
            if student_id not in self.estudiantes['student_id'].values:
                messagebox.showerror("Error", "ID de becario no encontrado")
                return
            
            tipo = self.entry_tipo.get()
            if not tipo:
                messagebox.showerror("Error", "Seleccione un tipo")
                return
            
            nuevo = pd.DataFrame({
                'student_id': [student_id],
                'fecha': [datetime.now()],
                'tipo': [tipo],
                'asistio_clase': [self.var_asistio.get()],
                'entrego_tareas': [self.var_tareas.get()],
                'act_voluntariado': [self.var_voluntariado.get()],
                'aprobo_parcial': [self.var_aprobo.get()],
                'comentario': [self.entry_comentario.get().strip() or 'Sin comentario']
            })
            self.seguimientos = pd.concat([self.seguimientos, nuevo], ignore_index=True)
            self.guardar_datos()
            messagebox.showinfo("Éxito", "Seguimiento registrado correctamente")
            
            # Limpiar campos
            self.entry_id.delete(0, tk.END)
            self.entry_tipo.set('')
            self.var_asistio.set(False)
            self.var_tareas.set(False)
            self.var_voluntariado.set(False)
            self.var_aprobo.set(False)
            self.entry_comentario.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ID válido")
    
    # ============================================================
    # PESTAÑA 3: CONSULTA
    # ============================================================
    
    def configurar_consulta(self):
        frame_consulta = tk.Frame(self.tab_consulta)
        frame_consulta.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Búsqueda
        frame_busqueda = tk.Frame(frame_consulta)
        frame_busqueda.pack(fill='x', pady=5)
        
        tk.Label(frame_busqueda, text="ID Becario:").pack(side='left', padx=5)
        self.entry_buscar = tk.Entry(frame_busqueda, width=10)
        self.entry_buscar.pack(side='left', padx=5)
        self.entry_buscar.bind('<Return>', lambda e: self.buscar_becario())
        
        btn_buscar = tk.Button(frame_busqueda, text="🔍 Buscar", command=self.buscar_becario, bg='#2196F3', fg='white')
        btn_buscar.pack(side='left', padx=5)
        
        btn_limpiar = tk.Button(frame_busqueda, text="🗑️ Limpiar", command=self.limpiar_consulta, bg='#f44336', fg='white')
        btn_limpiar.pack(side='left', padx=5)
        
        # Área de resultados
        self.text_consulta = scrolledtext.ScrolledText(frame_consulta, height=20, font=('Courier', 10))
        self.text_consulta.pack(fill='both', expand=True, pady=5)
    
    def buscar_becario(self):
        try:
            student_id = int(self.entry_buscar.get().strip())
            estudiante = self.estudiantes[self.estudiantes['student_id'] == student_id]
            
            if estudiante.empty:
                self.text_consulta.delete(1.0, tk.END)
                self.text_consulta.insert(tk.END, "❌ Becario no encontrado")
                return
            
            self.text_consulta.delete(1.0, tk.END)
            
            # Datos del becario
            self.text_consulta.insert(tk.END, "="*60 + "\n")
            self.text_consulta.insert(tk.END, f"📋 DATOS DEL BECARIO\n")
            self.text_consulta.insert(tk.END, "="*60 + "\n\n")
            
            for col in estudiante.columns:
                self.text_consulta.insert(tk.END, f"{col}: {estudiante[col].values[0]}\n")
            
            # Seguimientos
            segs = self.seguimientos[self.seguimientos['student_id'] == student_id]
            self.text_consulta.insert(tk.END, f"\n📊 Total de seguimientos: {len(segs)}\n")
            self.text_consulta.insert(tk.END, "="*60 + "\n")
            
            if not segs.empty:
                self.text_consulta.insert(tk.END, "\nÚLTIMOS 10 SEGUIMIENTOS:\n\n")
                ultimos = segs.sort_values('fecha', ascending=False).head(10)
                for _, row in ultimos.iterrows():
                    self.text_consulta.insert(tk.END, f"📅 {row['fecha'].strftime('%Y-%m-%d')} | {row['tipo']} | ")
                    self.text_consulta.insert(tk.END, f"Asist: {'✅' if row['asistio_clase'] else '❌'} | ")
                    self.text_consulta.insert(tk.END, f"Tareas: {'✅' if row['entrego_tareas'] else '❌'} | ")
                    self.text_consulta.insert(tk.END, f"Vol: {'✅' if row['act_voluntariado'] else '❌'} | ")
                    self.text_consulta.insert(tk.END, f"Aprob: {'✅' if row['aprobo_parcial'] else '❌'}\n")
                    self.text_consulta.insert(tk.END, f"   💬 {row['comentario']}\n\n")
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ID válido")
    
    def limpiar_consulta(self):
        self.text_consulta.delete(1.0, tk.END)
        self.entry_buscar.delete(0, tk.END)
    
    # ============================================================
    # PESTAÑA 4: REPORTES
    # ============================================================
    
    def configurar_reporte(self):
        frame_reporte = tk.Frame(self.tab_reporte)
        frame_reporte.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Filtros
        frame_filtros = tk.LabelFrame(frame_reporte, text="Filtros para Reporte", font=('Arial', 10, 'bold'))
        frame_filtros.pack(fill='x', pady=5)
        
        tk.Label(frame_filtros, text="Año:").grid(row=0, column=0, padx=5, pady=5)
        self.reporte_anio = ttk.Combobox(frame_filtros, values=list(range(2020, 2027)), width=8)
        self.reporte_anio.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_filtros, text="Mes:").grid(row=0, column=2, padx=5, pady=5)
        self.reporte_mes = ttk.Combobox(frame_filtros, values=list(range(1, 13)), width=5)
        self.reporte_mes.grid(row=0, column=3, padx=5, pady=5)
        
        btn_generar = tk.Button(frame_filtros, text="📄 Generar Reporte PDF", 
                                command=self.generar_reporte, bg='#FF9800', fg='white', 
                                font=('Arial', 10, 'bold'))
        btn_generar.grid(row=0, column=4, padx=10, pady=5)
        
        # Vista previa
        self.text_reporte = scrolledtext.ScrolledText(frame_reporte, height=15, font=('Courier', 9))
        self.text_reporte.pack(fill='both', expand=True, pady=5)
        
        # Info
        tk.Label(frame_reporte, text="💡 El reporte se guardará como 'reporte_becas.pdf' en la carpeta del programa", 
                font=('Arial', 9), fg='blue').pack()
    
    def generar_reporte(self):
        try:
            anio = self.reporte_anio.get()
            mes = self.reporte_mes.get()
            
            if not anio or not mes:
                messagebox.showerror("Error", "Seleccione año y mes")
                return
            
            anio = int(anio)
            mes = int(mes)
            
            # Filtrar datos
            df = self.seguimientos[
                (self.seguimientos['fecha'].dt.year == anio) & 
                (self.seguimientos['fecha'].dt.month == mes)
            ]
            
            if df.empty:
                messagebox.showwarning("Sin datos", f"No hay seguimientos para {anio}/{mes}")
                return
            
            # Calcular métricas
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
            
            # Mostrar en texto
            self.text_reporte.delete(1.0, tk.END)
            self.text_reporte.insert(tk.END, f"{'='*80}\n")
            self.text_reporte.insert(tk.END, f"REPORTE DE RENDIMIENTO - {anio}/{mes:02d}\n")
            self.text_reporte.insert(tk.END, f"{'='*80}\n\n")
            self.text_reporte.insert(tk.END, f"Total estudiantes evaluados: {len(metricas)}\n")
            self.text_reporte.insert(tk.END, f"Total seguimientos: {len(df)}\n")
            self.text_reporte.insert(tk.END, f"Rendimiento promedio: {metricas['rendimiento'].mean():.1f}%\n\n")
            self.text_reporte.insert(tk.END, f"{'TOP 10 MEJORES RENDIMIENTOS':^80}\n")
            self.text_reporte.insert(tk.END, f"{'-'*80}\n")
            
            for i, row in metricas.head(10).iterrows():
                self.text_reporte.insert(tk.END, f"{row['nombre']:25} | {row['carrera']:20} | Rend: {row['rendimiento']:5.1f}%\n")
            
            # Generar PDF (usando la función del script anterior)
            self.generar_pdf(metricas, df, anio, mes)
            
            messagebox.showinfo("Éxito", f"Reporte generado: reporte_becas_{anio}_{mes:02d}.pdf")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def generar_pdf(self, metricas, df, anio, mes):
        """Genera PDF con el reporte"""
        from matplotlib.backends.backend_pdf import PdfPages
        
        with PdfPages(f'reporte_becas_{anio}_{mes:02d}.pdf') as pdf:
            # Página 1: Tabla
            fig1, ax1 = plt.subplots(figsize=(12, 8))
            ax1.axis('tight')
            ax1.axis('off')
            
            tabla = metricas.head(20)[['nombre', 'carrera', 'anio', 'total_seguimientos', 
                                       'tasa_asistencia', 'tasa_tareas', 'tasa_voluntariado', 
                                       'tasa_aprobacion', 'rendimiento']]
            tabla.columns = ['Nombre', 'Carrera', 'Año', '#Segs', 'Asist.%', 'Tareas%', 'Vol.%', 'Aprob.%', 'Rend.%']
            
            table = ax1.table(cellText=tabla.values, colLabels=tabla.columns, loc='center', cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 1.5)
            ax1.set_title(f'REPORTE DE RENDIMIENTO - {anio}/{mes:02d}', fontsize=14, fontweight='bold', pad=20)
            pdf.savefig(fig1, bbox_inches='tight')
            plt.close(fig1)
            
            # Página 2: Gráficos
            fig2, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig2.suptitle(f'Dashboard - {anio}/{mes:02d}', fontsize=16, fontweight='bold')
            
            # Top 10
            ax1 = axes[0, 0]
            top10 = metricas.head(10)
            ax1.barh(top10['nombre'], top10['rendimiento'], color='skyblue')
            ax1.set_xlabel('Rendimiento %')
            ax1.set_title('Top 10 Mejores Rendimientos')
            ax1.invert_yaxis()
            
            # Promedios
            ax2 = axes[0, 1]
            promedios = metricas[['tasa_asistencia', 'tasa_tareas', 'tasa_voluntariado', 'tasa_aprobacion']].mean()
            colores = ['#2ecc71', '#3498db', '#f1c40f', '#e74c3c']
            ax2.bar(promedios.index, promedios.values, color=colores)
            ax2.set_ylim(0, 100)
            ax2.set_title('Promedio General por Indicador')
            ax2.set_ylabel('Porcentaje %')
            for i, v in enumerate(promedios.values):
                ax2.text(i, v + 1, f'{v:.1f}%', ha='center')
            
            # Tipos
            ax3 = axes[1, 0]
            tipos = df['tipo'].value_counts()
            ax3.pie(tipos.values, labels=tipos.index, autopct='%1.1f%%', startangle=90)
            ax3.set_title('Distribución por Tipo de Seguimiento')
            
            # Histograma
            ax4 = axes[1, 1]
            ax4.hist(metricas['rendimiento'], bins=10, color='purple', alpha=0.7, edgecolor='black')
            ax4.set_xlabel('Rendimiento %')
            ax4.set_ylabel('Cantidad')
            ax4.set_title('Distribución del Rendimiento')
            ax4.axvline(metricas['rendimiento'].mean(), color='red', linestyle='dashed', label='Promedio')
            ax4.legend()
            
            plt.tight_layout()
            pdf.savefig(fig2, bbox_inches='tight')
            plt.close(fig2)

# ============================================================
# EJECUTAR APLICACIÓN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaBecasGUI(root)
    root.mainloop()