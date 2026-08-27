import shutil

def get_health():
    # 1. Carga del sistema desde /proc/loadavg
    try:
        with open ( '/proc/loadavg', 'r' ) as f:
            load = f.read().split()[0]
    except FileNotFoundError:
        load = "N/A"

    # 2. Uso de RAM desde /proc/meminfo
    mem_total = 0
    mem_free = 0
    try:
        with open ( '/proc/meminfo', 'r' ) as f:
            for line in f:
                if line.startswith ( 'MemTotal:' ):
                    mem_total = int (line.split()[1])
                elif line.startswith ( 'MemAvailable:' ):
                    mem_free = int ( line.split()[1])
    except FileNotFoundError:
       pass

    ram_used_percent = 0
    if mem_total > 0:
       ram_used_percent = round ((( mem_total - mem_free) / mem_total ) * 100,1 )

    # 3. Uso de Disco en la raiz (/)
    disk = shutil.disk_usage ('/')
    disk_used_percent = round (( disk.used / disk.total) * 100,1)

    # 4. Diagnostico general
    status = "OK"
    if ram_used_percent > 85 or disk_used_percent > 90:
       status = "WARNING"

    print ( f"Estado general: {status}" )
    print ( f"Carga CPU (1 min): {load}" )
    print ( f"Uso de RAM: {ram_used_percent}%" )
    print ( f"Uso de Disco (/): {disk_used_percent}%" )

if __name__ == '__main__':
    get_health()

