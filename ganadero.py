import mysql.connector


class Ganadero:
    def __init__(self, role, contraseña):
        # Establecemos la conexión y cursor iniciales
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ranchmaster_db"
        )
        self.cursor = self.connection.cursor()
        self.role = 'ganadero'
        self.contraseña = contraseña


    def cerrar_conexion(self):
        # Cerramos el cursor y la conexión
        self.cursor.close()
        self.connection.close()

    def verificar_contraseña(self):
        consulta = "SELECT id_usuario FROM usuarios WHERE role = %s AND contraseña = %s"
        self.cursor.execute(consulta, (self.role, self.contraseña))
        resultado = self.cursor.fetchone()
        if resultado:
            self.id_usuario = resultado[0]  # Guardamos el ID del usuario autenticado
            return True
        return False

    def registrar_usuario(self, nombre_usuario, rol, contraseña):
        query = "INSERT INTO usuarios (nombre_usuario, rol, contraseña) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (nombre_usuario, rol, contraseña))
        self.connection.commit()
        print("Usuario registrado correctamente.")

    def consultar_usuarios(self):
        query = "SELECT * FROM usuarios"
        self.cursor.execute(query)
        usuarios = self.cursor.fetchall()
        return usuarios

    def modificar_usuario(self, id_usuario, nuevo_nombre_usuario=None, nuevo_rol=None, nueva_contraseña=None):
        consulta_actual = "SELECT nombre_usuario, rol, contraseña FROM usuarios WHERE id_usuario = %s"
        self.cursor.execute(consulta_actual, (id_usuario,))
        resultado = self.cursor.fetchone()

        if not resultado:
            print("No se encontró el usuario con el ID especificado.")
            return

        nuevo_nombre_usuario = nuevo_nombre_usuario if nuevo_nombre_usuario is not None else resultado[0]
        nuevo_rol = nuevo_rol if nuevo_rol is not None else resultado[1]

        # Si se proporciona una nueva contraseña, hashearla
        if nueva_contraseña is not None:
            nueva_contraseña = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt())
        else:
            nueva_contraseña = resultado[2]

        query = """
        UPDATE usuarios 
        SET nombre_usuario = %s, rol = %s, contraseña = %s 
        WHERE id_usuario = %s
        """
        self.cursor.execute(query, (nuevo_nombre_usuario, nuevo_rol, nueva_contraseña, id_usuario))
        self.connection.commit()
        print("Usuario modificado correctamente.")

    def eliminar_usuario(self, id_usuario):
        query = "DELETE FROM usuarios WHERE id_usuario = %s"
        self.cursor.execute(query, (id_usuario,))
        self.connection.commit()
        print("Usuario eliminado correctamente.")


    def sub_menu_gestion_usuarios(self):
        while True:
            print("\n--- Submenú de gestion de Usuarios ---")
            print("1. Registrar usuario")
            print("2. Consultar usuarios")
            print("3. Modificar usuario")
            print("4. Eliminar usuario")
            print("5. Volver al menu principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre_usuario = input("Ingrese el nombre del usuario: ")
                rol = input("Ingrese el rol del usuario (ganadero/encargado): ")
                contraseña = input("Ingrese la contraseña del usuario: ")
                self.registrar_usuario(nombre_usuario, rol, contraseña)

            elif opcion == "2":
                usuarios = self.consultar_usuarios()
                if usuarios:
                    for u in usuarios:
                        print(f"ID: {u[0]}, Nombre de Usuario: {u[1]}, Rol: {u[3]}")
                else:
                    print("No hay usuarios registrados.")


            elif opcion == "3":
                id_usuario = int(input("Ingrese el ID del usuario a modificar: "))
                nombre = input("Nuevo nombre (dejar vacío para no modificar): ") or None
                role = input("Nuevo rol (dejar vacío para no modificar): ") or None
                contraseña = input("Nueva contraseña (dejar vacío para no modificar): ") or None
                self.modificar_usuario(id_usuario, nombre, role, contraseña)


            elif opcion == "4":
                id_usuario = int(input("Ingrese el ID del usuario a eliminar: "))
                self.eliminar_usuario(id_usuario)

            elif opcion == "5":
                break

            else:
                print("Opción no válida. Intente de nuevo.")
    
    # Métodos para la tabla ganado
    def registrar_ganado(self, raza, edad, peso, estado):
        query = "INSERT INTO ganado (raza, edad, peso, estado, id_usuario) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (raza, edad, peso, estado, self.id_usuario))
        self.connection.commit()
        print("Ganado registrado correctamente.")
    

    def consultar_ganado(self):
        query = "SELECT * FROM ganado"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def modificar_ganado(self, id_ganado, raza=None, edad=None, peso=None, estado=None):
        consulta_actual = "SELECT raza, edad, peso, estado FROM ganado WHERE id_ganado = %s"
        self.cursor.execute(consulta_actual, (id_ganado,))
        resultado = self.cursor.fetchone()
    
        if not resultado:
            print("No se encontró el ganado con el ID especificado.")
            return
    
        raza = raza if raza is not None else resultado[0]
        edad = edad if edad is not None else resultado[1]
        peso = peso if peso is not None else resultado[2]
        estado = estado if estado is not None else resultado[3]
    
        query = """
        UPDATE ganado 
        SET raza = %s, edad = %s, peso = %s, estado = %s 
        WHERE id_ganado = %s
        """
        self.cursor.execute(query, (raza, edad, peso, estado, id_ganado))
        self.connection.commit()
        print("Datos del ganado actualizados correctamente.")


    def eliminar_ganado(self, id_ganado):
        query = "DELETE FROM ganado WHERE id_ganado = %s"
        self.cursor.execute(query, (id_ganado,))
        self.connection.commit()
        print("Ganado eliminado.")
    

    # Métodos para la tabla alimentacion
    def registrar_alimento(self, tipo_alimento, cantidad, frecuencia, fecha_registro, id_usuario):
        query = "INSERT INTO alimentacion (tipo_alimento, cantidad, frecuencia, fecha_registro, id_usuario) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (tipo_alimento, cantidad, frecuencia, fecha_registro, id_usuario))
        self.connection.commit()
        print("Alimento registrado correctamente.")

    def consultar_alimentacion_total(self):
        query = "SELECT id_alimentacion, tipo_alimento, cantidad, frecuencia, fecha_registro, id_usuario FROM alimentacion"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def modificar_alimento(self, id_alimentacion, nuevo_tipo_alimento=None, nueva_cantidad=None, nueva_frecuencia=None):
        consulta_actual = "SELECT tipo_alimento, cantidad, frecuencia FROM alimentacion WHERE id_alimentacion = %s"
        self.cursor.execute(consulta_actual, (id_alimentacion,))
        resultado = self.cursor.fetchone()
        

        if not resultado:
            print("No se encontró el alimento con el ID especificado.")
            return

        tipo_alimento = nuevo_tipo_alimento if nuevo_tipo_alimento is not None else resultado[0]
        cantidad = nueva_cantidad if nueva_cantidad is not None else resultado[1]
        frecuencia = nueva_frecuencia if nueva_frecuencia is not None else resultado[2]

        query = """
        UPDATE alimentacion 
        SET tipo_alimento = %s, cantidad = %s, frecuencia = %s 
        WHERE id_alimentacion = %s
        """
        self.cursor.execute(query, (tipo_alimento, cantidad, frecuencia, id_alimentacion))
        self.connection.commit()
        print("Datos del alimento actualizados correctamente.")

    
    def eliminar_alimento(self, id_alimentacion):
        query = "DELETE FROM alimentacion WHERE id_alimentacion = %s"
        self.cursor.execute(query, (id_alimentacion,))
        self.connection.commit()
        print("Registro de alimento eliminado correctamente.")

    # Métodos para la tabla alimentacion_ganado
    def vincular_alimentacion_ganado(self, id_ganado, id_alimentacion):
        query = "INSERT INTO alimentacion_ganado (id_ganado, id_alimentacion) VALUES (%s, %s)"
        self.cursor.execute(query, (id_ganado, id_alimentacion))
        self.connection.commit()
        print("Alimentación para el ganado registrada correctamente.")

    def consultar_alimentacion_ganado(self, id_ganado):
        query = """
        SELECT g.raza, a.id_alimentacion, a.tipo_alimento, a.cantidad, a.frecuencia, a.fecha_registro 
        FROM alimentacion_ganado ag 
        JOIN alimentacion a ON ag.id_alimentacion = a.id_alimentacion 
        JOIN ganado g ON ag.id_ganado = g.id_ganado
        WHERE ag.id_ganado = %s
        """
        self.cursor.execute(query, (id_ganado,))
        resultados = self.cursor.fetchall()
        return resultados  
    
    def modificar_alimentacion_ganado(self, id_ganado, num_alimentaciones):
        query_select = "SELECT ag.id_alimentacion, a.tipo_alimento, a.cantidad, a.frecuencia, a.fecha_registro " \
                   "FROM alimentacion_ganado ag " \
                   "JOIN alimentacion a ON ag.id_alimentacion = a.id_alimentacion " \
                   "WHERE ag.id_ganado = %s"
        self.cursor.execute(query_select, (id_ganado,))
        alimentaciones = self.cursor.fetchall()

        if not alimentaciones:
            print("No hay alimentaciones vinculadas a este ganado.")
            return

        print("Alimentación actual:")
        for alimentacion in alimentaciones:
            print(f"ID Alimentación: {alimentacion[0]}, Tipo: {alimentacion[1]}, Cantidad: {alimentacion[2]} kg, "
                f"Frecuencia: {alimentacion[3]}, Fecha: {alimentacion[4]}")

        for _ in range(num_alimentaciones):
            id_alimentacion_a_modificar = input("Ingrese el ID de alimentación que desea modificar: ")
            nuevo_id_alimentacion = input("Ingrese el nuevo ID de alimentación: ")

            query_check = "SELECT * FROM alimentacion_ganado WHERE id_ganado = %s AND id_alimentacion = %s"
            self.cursor.execute(query_check, (id_ganado, nuevo_id_alimentacion))

            if self.cursor.fetchone() is not None:
                print("La combinación de ganado y alimentación ya existe. No se puede modificar.")
                continue

            query_update = "UPDATE alimentacion_ganado SET id_alimentacion = %s WHERE id_ganado = %s AND id_alimentacion = %s"
            self.cursor.execute(query_update, (nuevo_id_alimentacion, id_ganado, id_alimentacion_a_modificar))

        self.connection.commit()
        print("Las alimentaciones del ganado han sido actualizadas correctamente.")


    def eliminar_alimentacion_ganado(self, id_ganado, id_alimentacion):
        query = "DELETE FROM alimentacion_ganado WHERE id_ganado = %s AND id_alimentacion = %s"
        self.cursor.execute(query, (id_ganado, id_alimentacion))
        self.connection.commit()
        print("Registro de alimentación de ganado eliminado correctamente.")

    # Métodos para la tabla alertas_agua
    def registrar_alerta_agua(self, nivel_agua, id_usuario):
        query = "INSERT INTO alertas_agua (nivel_agua, id_usuario) VALUES (%s, %s)"
        self.cursor.execute(query, (nivel_agua, id_usuario))
        self.connection.commit()
        print("Alerta de nivel de agua registrada correctamente.")
    
    def consultar_alertas_agua(self):
        query = "SELECT * FROM alertas_agua"
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def consultar_alertas_agua_activas(self):
        query = "SELECT * FROM alertas_agua WHERE estado_alerta = 'activa'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def resolver_alerta_agua(self, id_alerta, estado_alerta):
        query = "UPDATE alertas_agua SET estado_alerta = %s WHERE id_alerta = %s"
        self.cursor.execute(query, (estado_alerta, id_alerta))
        self.connection.commit()
        print("Alerta de agua resuelta correctamente.")
    
    
    def modificar_alerta_agua(self, id_alerta, nivel_agua=None, estado_alerta=None):
        consulta_actual = "SELECT nivel_agua, estado_alerta FROM alertas_agua WHERE id_alerta = %s"
        self.cursor.execute(consulta_actual, (id_alerta,))
        resultado = self.cursor.fetchone()
        
        if not resultado:
            print("No se encontró la alerta de agua con el ID especificado.")
            return

        nivel_agua = nivel_agua if nivel_agua is not None else resultado[0]
        estado_alerta = estado_alerta if estado_alerta is not None else resultado[1]

        query = """
        UPDATE alertas_agua 
        SET nivel_agua = %s, estado_alerta = %s 
        WHERE id_alerta = %s
        """
        self.cursor.execute(query, (nivel_agua, estado_alerta, id_alerta))
        self.connection.commit()
        print("Alerta de agua modificada correctamente.")

    # Método para eliminar una alerta de agua
    def eliminar_alerta_agua(self, id_alerta):
        query = "DELETE FROM alertas_agua WHERE id_alerta = %s"
        self.cursor.execute(query, (id_alerta,))
        self.connection.commit()
        print("Alerta de agua eliminada correctamente.")




    def menu_ganado(self):
        while True:
            print("\n--- Submenú de Ganado ---")
            print("1. Registrar ganado")
            print("2. Consultar ganado registrado")
            print("3. Modificar datos de ganado")
            print("4. Eliminar ganado")
            print("5. Volver al menú principal")
        
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                raza = input("Ingrese la raza del ganado: ")
                edad = int(input("Ingrese la edad del ganado: "))
                peso = float(input("Ingrese el peso del ganado (en kg): "))
                estado = input("Ingrese el estado de salud del ganado: ")
                self.registrar_ganado(raza, edad, peso, estado)

            elif opcion == "2":
                ganado = self.consultar_ganado()
                if ganado:
                    for g in ganado:
                        print(f"ID: {g[0]}, Raza: {g[1]}, Edad: {g[2]}, Peso: {g[3]} kg, Estado: {g[4]}")
                else:
                    print("No hay ganado registrado.")

            elif opcion == "3":
                id_ganado = int(input("Ingrese el ID del ganado a modificar: "))
                raza = input("Nueva raza (dejar vacío para no modificar): ") or None
                edad = input("Nueva edad (dejar vacío para no modificar): ") or None
                peso = input("Nuevo peso (dejar vacío para no modificar): ")
                peso = float(peso) if peso else None
                estado = input("Nuevo estado (dejar vacío para no modificar): ") or None
                self.modificar_ganado(id_ganado, raza, edad, peso, estado)

            elif opcion == "4":
                id_ganado = int(input("Ingrese el ID del ganado a eliminar: "))
                self.eliminar_ganado(id_ganado)

            elif opcion == "5":
                print("Saliendo del menú gestion de ganado.")
                break

            else:
                print("Opción no válida.")


    def menu_alimentacion(self):
        while True:
            print("\n--- Submenú de Alimentación ---")
            print("1. Registrar un nuevo alimento")
            print("2. Consultar alimentación registrada")
            print("3. Modificar un alimento")
            print("4. Eliminar un alimento")
            print("5. Volver al menú principal")
        
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                tipo_alimento = input("Ingrese el tipo de alimento: ")
                cantidad = float(input("Ingrese la cantidad (en kg): "))
                frecuencia = input("Ingrese la frecuencia de alimentación: ")
                fecha_registro = input("Ingrese la fecha de registro (YYYY-MM-DD): ")
                self.registrar_alimento(tipo_alimento, cantidad, frecuencia, fecha_registro, id_usuario=self.id_usuario)

            elif opcion == "2":
                alimentacion_registrada = self.consultar_alimentacion_total()
                if alimentacion_registrada:
                    for registro in alimentacion_registrada:
                        print(f"ID: {registro[0]}, Tipo: {registro[1]}, Cantidad: {registro[2]} kg, Frecuencia: {registro[3]}, Fecha: {registro[4]}")
                else:
                    print("No hay registros de alimentación.")

            elif opcion == "3":
                id_alimentacion = int(input("Ingrese el ID del alimento a modificar: "))
                tipo_alimento = input("Nuevo tipo de alimento (dejar vacío para no modificar): ") or None
                cantidad = input("Nueva cantidad (dejar vacío para no modificar): ")
                cantidad = float(cantidad) if cantidad else None
                frecuencia = input("Nueva frecuencia (dejar vacío para no modificar): ") or None
                self.modificar_alimento(id_alimentacion, tipo_alimento, cantidad, frecuencia)

            elif opcion == "4":
                id_alimentacion = int(input("Ingrese el ID del alimento a eliminar: "))
                self.eliminar_alimento(id_alimentacion)

            elif opcion == "5":
                print("Saliendo del menú gestion de alimentación.")
                break
            else:
                print("Opción no válida.")


    def sub_menu_alimentacion_ganado(self):
        while True:
            print("\n--- Menú de Alimentación del Ganado ---")
            print("1. Consultar alimentación registrada")
            print("2. Consultar ganado registrado")
            print("3. Vincular Alimentación a Ganado")
            print("4. Consultar Alimentación de Ganado")
            print("5. Modificar Alimentación de Ganado")
            print("6. Eliminar Alimentación de Ganado")
            print("7. volver al menu principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                alimentacion_registrada = self.consultar_alimentacion_total()
                if alimentacion_registrada:
                    print("Alimentación registrada:")
                    for registro in alimentacion_registrada:
                        print(f"ID: {registro[0]}, Tipo: {registro[1]}, Cantidad: {registro[2]} kg, Frecuencia: {registro[3]}, Fecha: {registro[4]}")
                else:
                    print("No hay registros de alimentación.")

            elif opcion == "2":
                ganado = self.consultar_ganado()
                if ganado:
                    for g in ganado:
                        print(f"ID: {g[0]}, Raza: {g[1]}, Edad: {g[2]}, Peso: {g[3]} kg, Estado: {g[4]}")
                else:
                    print("No hay ganado registrado.")

            elif opcion == "3":
                id_ganado = input("Ingrese el ID del ganado: ")
                id_alimentacion = input("Ingrese el ID de la alimentación: ")
                self.vincular_alimentacion_ganado(id_ganado, id_alimentacion)
                print("Alimentación vinculada exitosamente.")

            elif opcion == "4":
                id_ganado = input("Ingrese el ID del ganado: ")
                resultados = self.consultar_alimentacion_ganado(id_ganado)
                if resultados:
                    print(f"Alimentación del ganado con ID {id_ganado}:")
                    for fila in resultados:
                        print(f"Raza: {fila[0]}, ID Alimentación: {fila[1]}, Tipo: {fila[2]}, Cantidad: {fila[3]} kg, Frecuencia: {fila[4]}, Fecha: {fila[5]}")
                else:
                    print(f"No se encontró información de alimentación para el ganado con ID: {id_ganado}")

            elif opcion == "5":
                id_ganado = input("Ingrese el ID del ganado: ")
                resultados = self.consultar_alimentacion_ganado(id_ganado)
                if resultados:
                    print("Alimentación actual:")
                    for fila in resultados:
                        print(f"ID Alimentación: {fila[1]}, Tipo: {fila[2]}, Cantidad: {fila[3]} kg, Frecuencia: {fila[4]}, Fecha: {fila[5]}")

                    num_alimentaciones = int(input("¿Cuántas alimentaciones desea modificar? (Ingrese un número): "))
                    self.modificar_alimentacion_ganado(id_ganado, num_alimentaciones)
                else:
                    print(f"No hay alimentación registrada para el ganado con ID: {id_ganado}")

            elif opcion == "6":
                id_ganado = input("Ingrese el ID del ganado: ")
                id_alimentacion = input("Ingrese el ID de la alimentación a eliminar: ")
                self.eliminar_alimentacion_ganado(id_ganado, id_alimentacion)
                print("Alimentación eliminada exitosamente.")

            elif opcion == "7":
                print("Saliendo del menú vinculacion de alimentación del ganado.")
                break
            else:
                print("Opción no válida. Por favor, intente nuevamente.")

    def menu_alertas_agua(self):
        while True:
            print("\n--- Submenú de Alertas de Agua ---")
            print("1. Registrar alerta de agua")
            print("2. Consultar alertas de agua activas")
            print("3. Consultar historial de alertas")
            print("4. Resolver alerta de agua")
            print("5. Modificar alerta de agua")
            print("6. Eliminar alerta de agua")
            print("7. Volver al menú principal")
        
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                id_usuario = 1
                nivel_agua = float(input("Ingrese el nivel de agua actual: "))
                self.registrar_alerta_agua(nivel_agua, id_usuario=self.id_usuario)
                print("Alerta de agua registrada con éxito para el usuario con rol:", self.role)

            elif opcion == "2":
                alertas = self.consultar_alertas_agua_activas()
                if alertas:
                    for alerta in alertas:
                        print(f"Id_alerta: {alerta[0]}, Nivel_agua: {alerta[1]}, Fecha_alerta: {alerta[2]}, Id_usuario: {alerta[3]}, Estado_alerta: {alerta[4]}")
                else:
                    print("No hay alertas activas.")

            elif opcion == "3":
                alertas = self.consultar_alertas_agua()
                if alertas:
                    for alerta in alertas:
                        print(f"Id_alerta: {alerta[0]}, Nivel_agua: {alerta[1]}, Fecha_alerta: {alerta[2]}, Id_usuario: {alerta[3]}, Estado_alerta: {alerta[4]}")
                else:
                    print("No hay alertas registradas")

            elif opcion == "4":
                id_alerta = int(input("Ingrese el ID de la alerta a resolver: "))
                estado_resuelta = input("¿Está resuelta la alerta? (si/no): ").strip().lower()
                estado_alerta = "resuelta" if estado_resuelta == "si" else "activa"
                self.resolver_alerta_agua(id_alerta, estado_alerta=estado_alerta)

            elif opcion == "5":
                id_alerta = int(input("Ingrese el ID de la alerta a modificar: "))
                nivel_agua = input("Nuevo nivel de agua (dejar vacío para no modificar): ")
                nivel_agua = float(nivel_agua) if nivel_agua else None
                estado_alerta = input("Nuevo estado de la alerta (dejar vacío para no modificar): ") or None
                self.modificar_alerta_agua(id_alerta, nivel_agua, estado_alerta)

            elif opcion == "6":
                id_alerta = int(input("Ingrese el ID de la alerta a eliminar: "))
                self.eliminar_alerta_agua(id_alerta)

            elif opcion == "7":
                print("Saliendo del menu gestion de alertas de agua.")
                break
            else:
                print("Opción no válida.")

    def menu_ganadero(self):
        while True:
            print("\n---BIENVENID@ A RANCHMASTER---")
            print("\n--- Menú Principal Ganadero ---")
            print("1. Gestion de usuarios")
            print("2. Gestión de Ganado")
            print("3. Gestión de Alimentación")
            print("4. Vincular alimentación")
            print("5. Gestión de Alertas de Agua")
            print("6. Cerrar sesión y regresar al menu principal(roles)")
    
            opcion = input("Seleccione una opción: ")

            if opcion == "1" and self.role == "ganadero":
               self.sub_menu_gestion_usuarios()
            
            elif opcion == "2":
                self.menu_ganado()  

            elif opcion == "3":
                self.menu_alimentacion()  
    
            elif opcion == "4":
                self.sub_menu_alimentacion_ganado()  
    
            elif opcion == "5":
                self.menu_alertas_agua()  

            elif opcion == "6":
                print("Cerrando sesión.")
                return "regresar"
            else:
                print("Opción no válida.")
