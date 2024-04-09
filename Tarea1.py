import logging
import os.path
from argon2 import PasswordHasher
from getpass import getpass

logger = logging.getLogger(__name__)

def user():
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