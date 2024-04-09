import logging
import os.path
import secrets
import string
from argon2 import PasswordHasher
from getpass import getpass

logger = logging.getLogger(__name__)

def generator():
    logger.info('Iniciando generador de contraseñas')
    try:    
        print("Generador de Contraseñas: \n ¿Qué caracteres desea utilizar? \n 1. Alfabéticos \n 2. Alfanúmericos \n 3. Alfanúmericos con signos de puntuación \n")
        elec = 0
        while elec < 1 or elec > 3:
            elec = int(input("Ingrese elección: "))
            if elec < 1 or elec > 3:
                print("Opción inválida, seleccione una de las opciones permitidas. \n")
        num_car = 0
        while num_car < 8:
            num_car = int(input("Ingrese número de caracteres (8 mínimo):"))
            if num_car < 8:
                print("El mínimo de caracteres es 8. \n")
                logger.warning("No cumple con el mínimo de caracteres")
        logger.info("Generando la contraseña")
        if elec == 1:
            alphabet = string.ascii_letters
            password = ''.join(secrets.choice(alphabet) for i in range(num_car))
            print("La contraseña generada es: " ,password, "\n")
        elif elec == 2:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(num_car))
            print("La contraseña generada es: " ,password, "\n")
        elif elec == 3:
            alphabet = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(secrets.choice(alphabet) for i in range(num_car))
            print("La contraseña generada es: " ,password, "\n")
                
    except:
        logger.error("Falló la generación de contraseñas")
    logger.info("Cerrando generador de contraseñas")


def user():
    while True:
        logger.info('Ingresado a menú principal de usuario')
        print(
            '''Usuario\n\n
            Por favor seleccione una opción:\n\n
            1. Crear contraseña
            2. Recuperar contraseña
            3. Modificar contraseña
            4. Eliminar contraseña
            5. Cerrar sesión
            ''')
        try:
            option = int(input("Ingrese una opción: "))
            if option == 1:
                generator()
            elif option == 2:
                print()
            elif option == 3:
                print()
            elif option == 4:
                print()
            elif option == 5:
                logger.info('Opción seleccionada: Cerrar sesión')
                break
            else:
                print("Opción incorrecta, por favor ingrese una opción nuevamente")
                logger.warning('Opción seleccionada incorrecta')  
        except:
            print("Opción incorrecta, por favor ingrese una opción nuevamente")
            logger.warning('Opción seleccionada incorrecta')
    logger.info('Sesión cerrada')
    return

def create_user(username, password):
    try:
        hashed = PasswordHasher().hash(password)
        if os.path.isfile("{}.txt".format(username)):
            print("Usuario ya existe!")
            logger.warning('Falló la creación de usuario. Usuario ya existe')
            return False
        else:
            with open("{}.txt".format(username), 'w') as newUser:
                newUser.write("{}\n".format(hashed))
            print("usuario '{}' ha sido creado".format(username))
            logger.info('Usuario creado: {}'.format(username))
            return True
    except:
        logger.error('Falló la creación de nuevo usuario')
    return False

def admin():
    while True:
        logger.info('Ingresado a menú principal de administrador')
        print(
            '''Administrador\n\n
            Por favor seleccione una opción:\n\n
            1. Crear usuario
            2. Cerrar sesión
            ''')
        try:
            option = int(input("Ingrese una opción: "))
            if option == 1:
                logger.info('Opción seleccionada: Crear usuario')
                username = input("Ingrese nombre de usuario: ")
                print()
                password = getpass("Ingrese su contraseña: ")
                if create_user(username,password):
                    print("Usuario ha sido creado exitosamente")
                else:
                    print("No se pudo crear usuario")
            elif option == 2:
                logger.info('Opción seleccionada: Cerrar sesión')
                break
            else:
                print("Opción incorrecta, por favor ingrese una opción nuevamente")
                logger.warning('Opción seleccionada incorrecta')  
        except:
            print("Opción incorrecta, por favor ingrese una opción nuevamente")
            logger.warning('Opción seleccionada incorrecta')
    logger.info('Sesión cerrada')
    return

def login(username, password):
    with open("{}.txt".format(username)) as fopen:
        hashed = fopen.readline().strip()
    try:
        if PasswordHasher().verify(hashed, password):
            return True
        else:
            return False
    except:
        logger.error('Falló verificación de contraseña')
        return False
        
def main():
    logging.basicConfig(filename='tarea1.log', level=logging.INFO)
    logger.info('Inicio de aplicación')
    while True:
        print(
           '''Bienvenido!\n\n
           Por favor seleccione una opción:\n\n     
           1. Iniciar sesión\n
           2. Cerrar aplicación\n\n
           ''')
        try:
            option = int(input("Ingrese una opción: "))
            if option == 1:
                logger.info('Opción seleccionada: Iniciar sesión')
                username = input("Ingrese nombre de usuario: ")
                print()
                password = getpass("Ingrese su contraseña: ")
                if login(username, password):
                    print("Sesión iniciada")
                    if username == 'Admin':
                        logger.info('Sesión iniciada como administrador')
                        admin()
                    else:
                        logger.info('Sesión iniciada')
                        user()
                else:
                    print("Inicio de sesión incorrecto")
                    logger.info('No fue posible iniciar sesión')
            elif option == 2:
                logger.info('Opción seleccionada: Cerrar aplicación')
                break
            else:
                print("Opción incorrecta, por favor ingrese una opción nuevamente")
                logger.warning('Opción seleccionada incorrecta')    
        except:
            print("Opción incorrecta, por favor ingrese una opción nuevamente")
            logger.warning('Opción seleccionada incorrecta')
    print('Cerrando aplicación...')
    logger.info('Finalización de aplicación')
    return
    
if __name__ == '__main__':
    main()