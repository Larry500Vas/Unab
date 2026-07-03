# 📊 Sistema de Monitoreo de Becarios (1000 Estudiantes)

Este es un sistema de escritorio (GUI) desarrollado en Python para el seguimiento académico, asistencia y actividades de voluntariado de una base de 1,000 estudiantes becados. Permite registrar nuevos alumnos, añadir seguimientos periódicos, visualizar métricas en tiempo real a través de un dashboard integrado y exportar reportes ejecutivos en formato PDF.

## ✨ Características Principales

*   **📊 Dashboard Interactivo:** Gráficos en tiempo real que muestran el Top 10 de rendimiento, promedios generales por indicador (asistencia, tareas, voluntariado, aprobación), distribución por tipo de canal (Llamada, Presencial, Virtual) y un histograma de densidad del rendimiento.
*   **📝 Módulo de Registro:** Permite dar de alta a nuevos becarios y capturar seguimientos con métricas booleanas (Sí/No) y comentarios personalizados.
*   **🔍 Buscador Avanzado:** Consulta el historial completo y los datos generales de cualquier becario ingresando únicamente su ID.
*   **📄 Generador de Reportes:** Filtra la actividad por año/mes, genera una vista previa del rendimiento y exporta un documento PDF de dos páginas con tablas de datos y gráficos vectoriales.
*   **🔋 Autogeneración de Datos (Modo Demo):** Si los archivos de la base de datos no existen al iniciar la aplicación, el sistema genera automáticamente un entorno de prueba con 1,000 becarios y 5,000 seguimientos aleatorios reproducibles.

---

## 🛠️ Requisitos del Sistema

Para ejecutar esta aplicación necesitas tener instalado Python 3.x y las siguientes librerías científicas y de interfaz gráfica:

```bash
pip install pandas numpy matplotlib seaborn