import sqlite3
import os

def verificar_sistema():
    db_path = 'qsurge.db'
    print("\n--- 🛠️ INFORME DE ESTADO DEL PROYECTO ---")
    
    if not os.path.exists(db_path):
        print("❌ La base de datos no existe.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM lugares")
    lugares = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM eventos")
    eventos = cur.fetchone()[0]

    print(f"📊 Estadísticas: {lugares} Lugares | {eventos} Eventos")
    print("-" * 50)

    cur.execute("""
        SELECT e.titulo, l.nombre, e.fecha 
        FROM eventos e 
        JOIN lugares l ON e.lugar_id = l.id 
        ORDER BY e.id DESC LIMIT 5
    """)
    
    for row in cur.fetchall():
        print(f"🔹 {row[0]} | {row[1]} | {row[2]}")

    conn.close()

if __name__ == "__main__":
    verificar_sistema()
