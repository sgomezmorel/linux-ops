# linux-ops

A lightweight CLI monitoring tool built with Python for Linux systems.

## Features
- **System Health:** Quick check of CPU Load, RAM, and Disk usage with alert thresholds.
- **Hardware Inventory:** Summarizes Linux kernel version, uptime, and system specifications directly from `/proc`.
- **Easy Execution:** Includes a local launcher script for seamless execution.

## Installation & Usage

1. Clone the repository:
   ```bash
   git clone [https://github.com/sgomezmorel/linux-ops.git](https://github.com/sgomezmorel/linux-ops.git)
   cd linux-ops

# 🐧 Linux-Ops CLI

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Linux](https://img.shields.io/badge/Linux-Kali_/_Debian-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Bash](https://img.shields.io/badge/Shell_Script-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Git](https://img.shields.io/badge/Git-Version_Control-F05032?style=for-the-badge&logo=git&logoColor=white)

Una herramienta de línea de comandos (CLI) unificada y ligera para el **monitoreo del estado del sistema en tiempo real** e **inventario de hardware**, diseñada para entornos de administración de sistemas Linux e integración en escritorio gráfico.

---

## 🎯 Características Principales

* **Diagnóstico de Salud en Tiempo Real:** Métricas clave del sistema utilizando `psutil` (Carga de CPU, Uso de Memoria RAM y Ocupación del Disco `/`).
* **Alertas Visuales dinámicas:** Semáforo de estados (`OK`, `WARNING`, `CRITICAL`) implementado con **códigos de escape ANSI** según umbrales de consumo.
* **Inventario de Hardware & SO:** Extracción estructurada del modelo de procesador (vía `lscpu`), versión de Kernel, arquitectura y RAM instalada.
* **Persistencia Acumulativa JSON:** Registro histórico (`reporte.json`) que lee, parsea y concatena la telemetría de cada ejecución con marca de tiempo ISO (`YYYY-MM-DD HH:MM:SS`).
* **Integración con Desktop Environment (GUI):** Lanzador `.desktop` configurado con variables de entorno (`Path` de trabajo dedicado) y promps interactivos para ejecución directa desde el escritorio sin cierre prematuro de ventana.
* **Wrapper Bash Flexible:** Script ejecutable con soporte de subcomandos (`health`, `inventory`) y fallback automático al flujo unificado.

---

## 🛠️ Tecnologías y Arquitectura

* **Lenguaje:** Python 3
* **Librerías Core:** `psutil`, `json`, `subprocess`, `os`, `sys`, `datetime`
* **Shelling & Scripting:** Bash (`scripts/linux-ops`)
* **Formato de Configuración:** `.desktop` Entry Specifications (XDG Desktop Entry)

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/linux-ops.git](https://github.com/TU_USUARIO/linux-ops.git)
cd linux-ops
