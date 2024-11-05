import mysql.connector
from ganadero import Ganadero
from encargado import Encargado

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ranchmaster_db"
    )

def obtener_contraseña_usuario(nombre_usuario, rol, cursor):
    query = "SELECT contraseña FROM usuarios WHERE nombre_usuario = %s AND rol = %s"
    cursor.execute(query, (nombre_usuario, rol))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

def obtener_id_usuario(nombre_usuario, rol, cursor):
    query = "SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s AND rol = %s"
    cursor.execute(query, (nombre_usuario, rol))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

def main():
    intentos = 3

    while intentos > 0:
        print("-----SISTEMA DE GESTION DE GANADO RANCHMASTER----")
        print("Seleccione su rol:")
        print("1. Ganadero")
        print("2. Encargado")
        print("3. Salir")
        rol_opcion = input("Ingrese el número de su rol: ")

        if rol_opcion == "3":
            print("Saliendo del sistema. ¡Hasta luego!")
            return

        rol = "ganadero" if rol_opcion == "1" else "encargado" if rol_opcion == "2" else None
        if not rol:
            print("Opción de rol inválida. Inténtelo de nuevo.")
            continue

        usuario = input("Ingrese su nombre de usuario: ")
        contraseña = input("Ingrese su contraseña: ")

        try:
            connection = obtener_conexion()
            cursor = connection.cursor()
            contraseña_almacenada = obtener_contraseña_usuario(usuario, rol, cursor)
            id_usuario = obtener_id_usuario(usuario, rol, cursor)  # Obtener el ID del usuario

            if contraseña_almacenada is not None and contraseña_almacenada == contraseña:
                # Crear la instancia de la clase correspondiente según el rol
                if rol == "ganadero":
                    db = Ganadero(usuario, contraseña)
                elif rol == "encargado":
                    db = Encargado(usuario, contraseña)
                    
                else:
                    print("Rol no reconocido.")
                    continue

                # Asignar el id_usuario a la instancia de db
                db.id_usuario = id_usuario
                print(f"Inicio de sesión exitoso como {db.role}.")

                # Ejecutar el menú correspondiente según el rol
                if rol == "ganadero":
                    resultado = db.menu_ganadero()
                    if resultado == "regresar":
                        continue
                elif rol == "encargado":
                    print("Rol actual:", db.role)
                    db.menu_encargado()
                    continue
                break
            else:
                intentos -= 1
                print(f"Usuario o contraseña incorrectos. Intentos restantes: {intentos}")
                if intentos == 0:
                    print("Error al iniciar sesión. Intente más tarde.")
                    return

        except mysql.connector.Error as e:
            print(f"Error de conexión a la base de datos: {e}")
            return
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()