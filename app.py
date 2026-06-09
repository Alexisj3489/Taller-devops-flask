from flask import Flask
import psycopg2

app = Flask(__name__)
VERSION = "1.0.0"

@app.route("/")
def index():
    try:
        # Conexión a PostgreSQL (el host "db" coincidirá con Docker Compose)
        conexion = psycopg2.connect(
            host="db",
            database="taller_db",
            user="admin",
            password="12345"
        )
        cursor = conexion.cursor()
        
        # Verificar versión de PostgreSQL
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]

        # Intentar consultar una tabla de usuarios
        html_usuarios = ""
        try:
            cursor.execute("SELECT id, nombre FROM usuarios;")
            usuarios = cursor.fetchall()
            html_usuarios = "<h3>Usuarios Registrados:</h3><ul class='user-list'>"
            for u in usuarios:
                html_usuarios += f"""
                <li class='user-item'>
                    <span class='user-name'>{u[1]}</span>
                    <span class='user-id'>ID: {u[0]}</span>
                </li>
                """
            html_usuarios += "</ul>"
        except psycopg2.errors.UndefinedTable:
            conexion.rollback()
            html_usuarios = "<p class='no-table'><em>⚠️ La tabla 'usuarios' aún no existe. Créala en pgAdmin.</em></p>"

        cursor.close()
        conexion.close()

        # Tu bloque HTML original ahora envuelto en una tarjeta elegante con CSS
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Taller DevOps - Flask</title>
            <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap" rel="stylesheet">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f4f6f9;
                    margin: 0;
                    padding: 40px 20px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 80vh;
                }}
                .container {{
                    background: white;
                    max-width: 550px;
                    width: 100%;
                    padding: 35px;
                    border-radius: 16px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.07);
                    border: 1px solid #e1e8ed;
                }}
                h1 {{
                    color: #1e293b;
                    margin: 0 0 5px 0;
                    font-size: 26px;
                    font-weight: 700;
                }}
                h2 {{
                    font-size: 14px;
                    background: #e2e8f0;
                    color: #475569;
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-weight: 600;
                    display: inline-block;
                    margin: 0 0 20px 0;
                }}
                .status-box {{
                    padding: 12px 15px;
                    border-radius: 10px;
                    font-weight: 600;
                    margin-bottom: 15px;
                    background-color: #ecfdf5;
                    color: #059669;
                    border: 1px solid #a7f3d0;
                }}
                .db-version {{
                    font-size: 11px;
                    color: #64748b;
                    background: #f8fafc;
                    padding: 8px 12px;
                    border-radius: 8px;
                    margin-bottom: 25px;
                    border-left: 4px solid #cbd5e1;
                    word-break: break-all;
                }}
                hr {{
                    border: 0;
                    border-top: 2px solid #f1f5f9;
                    margin: 20px 0;
                }}
                h3 {{
                    color: #334155;
                    font-size: 18px;
                    margin-bottom: 15px;
                }}
                .user-list {{
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }}
                .user-item {{
                    background: #f8fafc;
                    padding: 12px 16px;
                    border-radius: 8px;
                    margin-bottom: 10px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border: 1px solid #e2e8f0;
                    transition: all 0.2s;
                }}
                .user-item:hover {{
                    transform: translateX(4px);
                    background: #f1f5f9;
                    border-color: #cbd5e1;
                }}
                .user-name {{
                    color: #1e293b;
                    font-weight: 600;
                }}
                .user-id {{
                    background: #3b82f6;
                    color: white;
                    font-size: 11px;
                    font-weight: bold;
                    padding: 3px 8px;
                    border-radius: 6px;
                }}
                .no-table {{
                    color: #64748b;
                    background: #fffbeb;
                    padding: 12px;
                    border-radius: 8px;
                    border: 1px solid #fde68a;
                    margin: 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Taller DevOps - Flask</h1>
                <h2>Versión de la App: {VERSION}</h2>
                <div class="status-box">✅ Conexión a Base de Datos Exitosa</div>
                <div class="db-version">{db_version}</div>
                <hr>
                {html_usuarios}
            </div>
        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: sans-serif; display: flex; justify-content: center; padding: 40px; background: #f4f6f9; }}
                .error-container {{ background: white; max-width: 500px; padding: 30px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); border-left: 5px solid #ef4444; }}
                h1 {{ color: #dc2626; margin-top: 0; }}
                p {{ color: #4b5563; background: #fef2f2; padding: 10px; border-radius: 6px; font-family: monospace; }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>❌ Error de Conexión:</h1>
                <p>{str(e)}</p>
            </div>
        </body>
        </html>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)