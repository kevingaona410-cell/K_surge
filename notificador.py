import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_reporte_email(total_eventos, lista_eventos):
    # --- CONFIGURACIÓN DEL EMISOR ---
    remitente = "tu_correo@gmail.com"
    # IMPORTANTE: Para Gmail necesitas una "Contraseña de Aplicación"
    password = "tu_contraseña_de_aplicacion" 
    destinatario = "correo_del_jurado_o_tu_socio@gmail.com"

    # --- CREACIÓN DEL MENSAJE ---
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = f"📊 Reporte QSurge: {total_eventos} eventos detectados"

    # Cuerpo del mensaje en formato HTML
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #A52A2A;">🚀 Informe de Actualización Kesurge?!</h2>
        <p>Se ha completado un nuevo ciclo de rastreo con éxito.</p>
        <p><b>Total de eventos encontrados:</b> {total_eventos}</p>
        <hr>
        <p style="font-size: 12px; color: #666;">Sistema automatizado QSurge - Asunción, Paraguay</p>
    </body>
    </html>
    """
    mensaje.attach(MIMEText(cuerpo, 'html'))

    # --- ENVÍO DEL CORREO ---
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(mensaje)
        server.quit()
        print("📧 Reporte enviado por correo con éxito.")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")