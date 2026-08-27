#!/bin/sh
set -e
echo "verificando el entorno de linux..."
if [ ! -d ".venv" ] ; then 
echo "Error: El entorno virtual (.venv) no existe. Corre 'make venv'."
exit 1
fi
if [ ! -f "/proc/meminfo" ] || [ ! -f "/proc/loadavg" ] ; then 
echo "Error: No se encontraron los archivos del kernel (/proc)."
exit 1
fi
echo "Todo correcto!! el entorno esta listo."

