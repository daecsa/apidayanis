from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# Función para conectar a la base de datos
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

# Ruta para obtener todos los usuarios
@app.route("/api/usuarios", methods=['GET'])
def obtener_usuarios():
    try:
        conn = conectar('localhost', 'root', '', 'AdminUsuariosNet')
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
        data = []
        for row in usuarios:
            usuario = {
                'id': row[0],
                'nombre': row[1],
                'apellido': row[2],
                'correo': row[3],
                'contraseña': row[4]
            }
            data.append(usuario)
        return jsonify({'usuarios': data})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al consultar usuarios'}), 500
    finally:
        cur.close()
        conn.close()

# Ruta para obtener un usuario por ID
@app.route("/api/usuarios/<int:id>", methods=['GET'])
def obtener_usuario(id):
    try:
        conn = conectar('localhost', 'root', '', 'AdminUsuariosNet')
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cur.fetchone()
        if usuario:
            data = {
                'id': usuario[0],
                'nombre': usuario[1],
                'apellido': usuario[2],
                'correo': usuario[3],
                'contraseña': usuario[4]
            }
            return jsonify({'usuario': data})
        else:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al consultar el usuario'}), 500
    finally:
        cur.close()
        conn.close()

# Ruta para crear un nuevo usuario
@app.route("/api/usuarios", methods=['POST'])
def crear_usuario():
    try:
        conn = conectar('localhost', 'root', '', 'AdminUsuariosNet')
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nombre, apellido, correo, contraseña) VALUES (%s, %s, %s, %s)",
                    (request.json['nombre'], request.json['apellido'], request.json['correo'], request.json['contraseña']))
        conn.commit()
        return jsonify({'mensaje': 'Usuario creado'}), 201
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al crear el usuario'}), 500
    finally:
        cur.close()
        conn.close()

# Ruta para actualizar un usuario
@app.route("/api/usuarios/<int:id>", methods=['PUT'])
def actualizar_usuario(id):
    try:
        conn = conectar('localhost', 'root', '', 'AdminUsuariosNet')
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET nombre = %s, apellido = %s, correo = %s, contraseña = %s WHERE id = %s",
                    (request.json['nombre'], request.json['apellido'], request.json['correo'], request.json['contraseña'], id))
        if cur.rowcount > 0:
            conn.commit()
            return jsonify({'mensaje': 'Usuario actualizado'})
        else:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al actualizar el usuario'}), 500
    finally:
        cur.close()
        conn.close()

# Ruta para eliminar un usuario
@app.route("/api/usuarios/<int:id>", methods=['DELETE'])
def eliminar_usuario(id):
    try:
        conn = conectar('localhost', 'root', '', 'AdminUsuariosNet')
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        if cur.rowcount > 0:
            conn.commit()
            return jsonify({'mensaje': 'Usuario eliminado'})
        else:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al eliminar el usuario'}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
