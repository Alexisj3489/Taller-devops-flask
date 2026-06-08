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
            password="password123"
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
            html_usuarios = "<h3>Usuarios Registrados:</h3><ul>"
            for u in usuarios:
                html_usuarios += f"<li>ID: {u[0]} - Nombre: {u[1]}</li>"
            html_usuarios += "</ul>"
        except psycopg2.errors.UndefinedTable:
            conexion.rollback()
            html_usuarios = "<p><em>La tabla 'usuarios' aún no existe. Créala en pgAdmin.</em></p>"

        cursor.close()
        conexion.close()

        return f"""
        <h1>🚀 Taller DevOps - Flask</h1>
        <h2>Versión de la App: {VERSION}</h2>
        <p style="color: green;"><strong>✅ Conexión a Base de Datos Exitosa</strong></p>
        <p><small>{db_version}</small></p>
        <hr>
        {html_usuarios}
        """

    except Exception as e:
        return f"<h1 style='color: red;'>❌ Error de Conexión:</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)