import os
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Importación de tus módulos locales
from scraper_villamorra import QSurgeScraper
from database import VillaMorraDB
import generar_html_interactivo

# --- CONFIGURACIÓN DE CORREO ---
# Reemplaza con tus datos reales para la hackatón
EMAIL_REMITENTE = "tu_usuario@gmail.com"
EMAIL_PASSWORD = "abcd efgh ijkl mnop"  # Tu "Contraseña de Aplicación" de Google
EMAIL_DESTINATARIO = "destinatario@ejemplo.com"

def enviar_notificacion_email(total_eventos):
    """Envía un reporte formal con los colores de la marca Kesurge?!"""
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    mensaje = MIMEMultipart()
    mensaje['From'] = EMAIL_REMITENTE
    mensaje['To'] = EMAIL_DESTINATARIO
    mensaje['Subject'] = f"📊 Reporte QSurge: {total_eventos} Eventos Detectados"

    cuerpo_html = f"""
    <html>
    <body style="font-family: 'Segoe UI', sans-serif; background-color: #FDF5E6; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 15px; border: 1px solid #A52A2A; overflow: hidden;">
            <div style="background-color: #A52A2A; color: white; padding: 20px; text-align: center;">
                <h1 style="margin: 0;">Kesurge?!</h1>
                <p style="margin: 0; font-size: 14px;">Inteligencia Urbana - Asunción</p>
            </div>
            <div style="padding: 30px; color: #1A1A1A;">
                <h2 style="color: #2D5A27;">Ciclo de Actualización Completado</h2>
                <p>El sistema ha rastreado con éxito las fuentes locales.</p>
                <div style="background: #F7A00A; color: #1A1A1A; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 20px;">
                    {total_eventos} Eventos Activos
                </div>
                <p style="margin-top: 20px;"><b>Hora del reporte:</b> {ahora}</p>
                <p style="font-size: 12px; color: #666;">Este es un mensaje automático generado por el motor QSurge cada 10 minutos.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    mensaje.attach(MIMEText(cuerpo_html, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
        server.send_message(mensaje)
        server.quit()
        print(f"📧 Reporte enviado a {EMAIL_DESTINATARIO}")
    except Exception as e:
        print(f"⚠️ No se pudo enviar el correo: {e}")

def ciclo_principal():
    ahora_str = datetime.now().strftime('%H:%M:%S')
    print(f"\n🔄 INICIANDO CICLO DE ACTUALIZACIÓN: {ahora_str}")
    print("=" * 45)
    
    # 1. Ejecución del Scraper
    scraper = QSurgeScraper(api_key="NOZSS2PZJ2GYQ7RYHJKU")
    scraper.run()
    
    # 2. Base de Datos y Logs
    db = VillaMorraDB()
    total = db.obtener_conteo()
    db.registrar_log_actualizacion(total)
    
    # 3. Generación de la Interfaz con diseño del compañero
    generar_html_interactivo.generar()
    
    # 4. Notificación por Email
    print(f"📊 Informe: {total} eventos procesados.")
    enviar_notificacion_email(total)
    
    print(f"✅ Proceso finalizado a las {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    TIEMPO_ESPERA = 600  # 10 Minutos
    print("🚀 ECOSISTEMA QSURGE ACTIVADO (Ciclos de 10 min + Email)")
    
    try:
        while True:
            ciclo_principal()
            print(f"😴 Modo espera: Próximo rastreo en {TIEMPO_ESPERA} segundos...")
            time.sleep(TIEMPO_ESPERA)
    except KeyboardInterrupt:
        print("\n🛑 Sistema detenido por el usuario. Cerrando...")