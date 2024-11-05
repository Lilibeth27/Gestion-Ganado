import mysql.connector

class Encargado:
    def __init__(self, role, contraseña):
        # Establecemos la conexión y cursor iniciales
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ranchmaster_db"
        )
        self.cursor = self.connection.cursor()
        self.role = 'encargado'
        self.contraseña = contraseña
        self.id_usuario = None

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
    
    def registrar_alimentacion(self, tipo_alimento, cantidad, frecuencia, fecha_registro, id_usuario):
        query = "INSERT INTO alimentacion (tipo_alimento, cantidad, frecuencia, fecha_registro, id_usuario) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (tipo_alimento, cantidad, frecuencia, fecha_registro, id_usuario))
        self.connection.commit()
        print("Alimento registrado correctamente.")
       

    def consultar_alimentacion(self):
        query = "SELECT id_alimentacion, tipo_alimento, cantidad, frecuencia, fecha_registro, id_usuario FROM alimentacion"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def modificar_alimentacion(self, id_alimentacion, nuevo_tipo_alimento=None, nueva_cantidad=None, nueva_frecuencia=None):
        # Obtener valores actuales de alimentacion
        consulta_actual = "SELECT tipo_alimento, cantidad, frecuencia FROM alimentacion WHERE id_alimentacion = %s"
        self.cursor.execute(consulta_actual, (id_alimentacion,))
        resultado = self.cursor.fetchone()
        

        if not resultado:
            print("No se encontró el alimento con el ID especificado.")
            return

        # Actualizamos solo si se proporciona un nuevo valor, o mantenemos el actual
        tipo_alimento = nuevo_tipo_alimento if nuevo_tipo_alimento is not None else resultado[0]
        cantidad = nueva_cantidad if nueva_cantidad is not None else resultado[1]
        frecuencia = nueva_frecuencia if nueva_frecuencia is not None else resultado[2]

        # Actualizar el registro de alimentacion
        query = """
        UPDATE alimentacion 
        SET tipo_alimento = %s, cantidad = %s, frecuencia = %s 
        WHERE id_alimentacion = %s
        """
        self.cursor.execute(query, (tipo_alimento, cantidad, frecuencia, id_alimentacion))
        self.connection.commit()
        print("Datos del alimento actualizados correctamente.")



    
    #alimenacion ganado
    def registrar_alimentacion_ganado(self, id_ganado, id_alimentacion):
         # Verificar si la combinación ya existe
        query_verificar = "SELECT * FROM alimentacion_ganado WHERE id_ganado = %s AND id_alimentacion = %s"
        self.cursor.execute(query_verificar, (id_ganado, id_alimentacion))
        registro_existente = self.cursor.fetchone()
    
        if registro_existente:
             print("Este ganado ya tiene esta alimentación registrada.")
             return
    
         # Si no existe, realizar la inserción
        query_insertar = "INSERT INTO alimentacion_ganado (id_ganado, id_alimentacion) VALUES (%s, %s)"
        self.cursor.execute(query_insertar, (id_ganado, id_alimentacion))
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



    def vincular_alimentacion_ganado(self, id_ganado, id_alimentacion):
        query = "INSERT INTO alimentacion_ganado (id_ganado, id_alimentacion) VALUES (%s, %s)"
        self.cursor.execute(query, (id_ganado, id_alimentacion))
        self.connection.commit()
        print("Alimentación para el ganado registrada correctamente.")

    
    def registrar_alerta_agua(self, nivel_agua, id_usuario):
        query = "INSERT INTO alertas_agua (nivel_agua, id_usuario) VALUES (%s, %s)"
        self.cursor.execute(query, (nivel_agua, self.id_usuario))
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
    
        # Método para modificar una alerta de agua
    def modificar_alerta_agua(self, id_alerta, nivel_agua=None, estado_alerta=None):
        # Primero, recuperamos los datos actuales de la alerta
        consulta_actual = "SELECT nivel_agua, estado_alerta FROM alertas_agua WHERE id_alerta = %s"
        self.cursor.execute(consulta_actual, (id_alerta,))
        resultado = self.cursor.fetchone()
        
        if not resultado:
            print("No se encontró la alerta de agua con el ID especificado.")
            return

        # Si el valor es None (no se quiere cambiar), se conserva el valor actual
        nivel_agua = nivel_agua if nivel_agua is not None else resultado[0]
        estado_alerta = estado_alerta if estado_alerta is not None else resultado[1]

        # Realizamos la actualización con los valores nuevos o los actuales si no se cambian
        query = """
        UPDATE alertas_agua 
        SET nivel_agua = %s, estado_alerta = %s 
        WHERE id_alerta = %s
        """
        self.cursor.execute(query, (nivel_agua, estado_alerta, id_alerta))
        self.connection.commit()
        print("Alerta de agua modificada correctamente.")

    def consultar_ganado(self):
        query = "SELECT * FROM ganado"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    
    def cerrar_conexion(self):
        self.cursor.close()
        self.connection.close()


    def menu_ganado(self):
        while True:
            print("\n--- Submenú de Ganado ---")
            print("1. Consultar ganado registrado")
            print("2. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                ganado = self.consultar_ganado()
                if ganado:
                    for g in ganado:
                        print(f"ID: {g[0]}, Raza: {g[1]}, Edad: {g[2]}, Peso: {g[3]} kg, Estado: {g[4]}")
                else:
                    print("No hay ganado registrado.")
            elif opcion == "2":
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
        print("4. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            tipo_alimento = input("Ingrese el tipo de alimento: ")
            cantidad = float(input("Ingrese la cantidad (en kg): "))
            frecuencia = input("Ingrese la frecuencia de alimentación: ")
            fecha_registro = input("ingrese la fecha (YYYY-MM-DD)")
            self.registrar_alimentacion(tipo_alimento, cantidad, frecuencia, fecha_registro, id_usuario=self.id_usuario)
        
            
        elif opcion == "2":
            alimentacion_registrada = self.consultar_alimentacion()
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
            self.modificar_alimentacion(id_alimentacion, tipo_alimento, cantidad, frecuencia)
        
        
        elif opcion == "4":
            print("Saliendo del menú gestion de alimentación.")
            break
        else:
            print("Opción no válida.")


    def sub_menu_alimentacion_ganado(self):
     while True:
        print("\n--- Menú de Alimentación del Ganado ---")
        print("1. Consultar ganado registrado")
        print("2. Consultar alimentacion registrada")
        print("3. Consultar Alimentación de Ganado")
        print("4. Vincular Alimentación a Ganado")
        print("5. Modificar Alimentación de Ganado")
        print("6. Volver al menu principal")

        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            ganado = self.consultar_ganado()
            if ganado:
                for g in ganado:
                    print(f"ID: {g[0]}, Raza: {g[1]}, Edad: {g[2]}, Peso: {g[3]} kg, Estado: {g[4]}")
            else:
                print("No hay ganado registrado.")

        elif opcion == '2':
            alimentacion_registrada = self.consultar_alimentacion()
            if alimentacion_registrada:
                for registro in alimentacion_registrada:
                    print(f"ID: {registro[0]}, Tipo: {registro[1]}, Cantidad: {registro[2]} kg, Frecuencia: {registro[3]}, Fecha: {registro[4]}")
            else:
                print("No hay registros de alimentación.")

        elif opcion == '3':
            id_ganado = input("Ingrese el ID del ganado: ")
            resultados = self.consultar_alimentacion_ganado(id_ganado)
            if resultados:
                print(f"Alimentación del ganado con ID {id_ganado}:")
                for fila in resultados:
                    print(f"Raza: {fila[0]}, ID Alimentación: {fila[1]}, Tipo: {fila[2]}, Cantidad: {fila[3]} kg, Frecuencia: {fila[4]}, Fecha: {fila[5]}")
            else:
                print(f"No se encontró información de alimentación para el ganado con ID: {id_ganado}")
                
        elif opcion == '4':
            id_ganado = input("Ingrese el ID del ganado: ")
            id_alimentacion = input("Ingrese el ID de la alimentación: ")
            self.vincular_alimentacion_ganado(id_ganado, id_alimentacion)
            print("Vinculacion Exitosa ")

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


        elif opcion == '6':
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
        print("6. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("Rol actual:", self.role)
            nivel_agua = float(input("Ingrese el nivel de agua actual: "))

            # Verificar que el rol sea 'encargado' o 'ganadero'
            if self.role in ['ganadero', 'encargado']:
                id_usuario = self.id_usuario  # Usar id_usuario directamente de la instancia
            else:
                print("Rol no reconocido. No se puede registrar la alerta.")
                continue
            
            self.registrar_alerta_agua(nivel_agua, id_usuario=id_usuario)
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
            print("Saliendo del menu gestion de alertas de agua.")
            break
        else:
            print("Opción no válida.")

    def mostrar_menu(self):
        if self.role == 'encargado':
            self.menu_encargado()
        else:
            print("Acceso denegado: solo los usuarios con el rol de encargado pueden acceder a este menú.")
            
    def menu_encargado(self):
        while True:
            print("\n---BIENVENID@ A RANCHMASTER---")
            print("\n--- Menú Principal Ganadero ---")
            print("1. Gestión de Ganado")
            print("2. Gestión de Alimentación")
            print("3. Vincular alimentación")
            print("4. Gestión de Alertas de Agua")
            print("5. Cerrar sesión y regresar al menu principal(roles)")
    
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.menu_ganado()  

            elif opcion == "2":
                self.menu_alimentacion()  
    
            elif opcion == "3":
                self.sub_menu_alimentacion_ganado()  
    
            elif opcion == "4":
                self.menu_alertas_agua()  

            elif opcion == "5":
                print("Cerrando sesión. ¡Hasta luego!")
                return
            else:
                print("Opción no válida.")
    

    
        