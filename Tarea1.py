import logging
import os.path
import secrets
import string
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from argon2 import PasswordHasher
from getpass import getpass

KDF_ALGORITHM = hashes.SHA256()
KDF_LENGTH = 32
KDF_ITERATIONS = 120000

logger = logging.getLogger(__name__)
username = ""

def get_file_data(username):
    data = []
    try:
        with open("{}.txt".format(username)) as fileData:
            data.append(fileData.readline().strip())
            data.append(fileData.readlines())
        return data
    except:
        return []
    return []

def change_password():
    global username
    appPass = None
    logger.info('Iniciando modificación de contraseña')
    try:
        logger.info('Inicio de autenticación')
        print("---Autenticación requerida---")
        appPass = input("Por favor ingrese su contraseña: ")
        if not login(username, appPass):
            logger.warning('Autenticación incorrecta, finalizando creación de contraseña')
            return
    except:
        logger.error('Ocurrió un error en el proceso de autenticación')
        return
    logger.info('Usuario autenticado')
    try:
        logger.info('Inicio de proceso de modificación de contraseña')
        keyword = input("Por favor ingrese la palabra clave asociada a la contraseña: ")
        password = input("Por favor ingrese la nueva contraseña: ")

        data = get_file_data(username)
        if len(data) == 0:
            print("No fue posible recuperar información del usuario")
            return
        
        newData = []

        plaintext = (keyword+':'+password).encode()
        
        salt = b'salt_'  # You should use a different salt for each user
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(appPass.encode())
        key = base64.urlsafe_b64encode(key)
        f = Fernet(key)
        
        found = False
        
        for cipher in data[1]:
            encrypted = base64.urlsafe_b64decode(cipher.strip()).decode()
            content = f.decrypt(encrypted).decode().split(':')
            if content[0] == keyword:
                found = True
                plaintext = (keyword+':'+password).encode()
                ciphertext = f.encrypt(plaintext)
                ciphertext = base64.urlsafe_b64encode(ciphertext).decode()
                newData.append(ciphertext)
            else:
                newData.append(cipher)
            
        if not found:
            print("No encontrado")
        else:
            with open("{}.txt".format(username), 'w') as newFile:
                newFile.write(data[0]+'\n')
                newFile.write('\n'.join(newData))
            print("Contraseña modificada correctamente.")
    except:
        print("Error en la operación")
        return
    logger.info('Fin de modificación de contraseña')
    return


def create_password():
    global username
    appPass = None
    logger.info('Iniciando creación de contraseña')
    try:
        logger.info('Inicio de autenticación')
        print("---Autenticación requerida---")
        appPass = input("Por favor ingrese su contraseña: ")
        if not login(username, appPass):
            logger.warning('Autenticación incorrecta, finalizando creación de contraseña')
            return
    except:
        logger.error('Ocurrió un error en el proceso de autenticación')
        return
    logger.info('Usuario autenticado')
    try:
        logger.info('Inicio de proceso de creación de contraseña')
        password = input("Por favor ingrese la contraseña a almacenar: ")
        keyword = input("Por favor ingrese una palabra clave a asociar con la contraseña: ")
        plaintext = (keyword+':'+password).encode()
        
        salt = b'salt_'  # You should use a different salt for each user
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(appPass.encode())
        key = base64.urlsafe_b64encode(key)
        f = Fernet(key)
        ciphertext = f.encrypt(plaintext)
        ciphertext = base64.urlsafe_b64encode(ciphertext).decode()
        
        with open("{}.txt".format(username), 'a') as newPassword:
            newPassword.write(ciphertext + "\n")
        logger.info('Contraseña creada y almacenada exitosamente')
        print("Contraseña creada")
    except:
        print("Error al crear contraseña")
        logger.error('No fue posible almacenar la contraseña')
        return
    logger.info('Fin de creación de contraseña')
    return

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
    return

def get_password():
    global username
    appPass = None
    logger.info('Iniciando creación de contraseña')
    try:
        logger.info('Inicio de autenticación')
        print("---Autenticación requerida---")
        appPass = input("Por favor ingrese su contraseña: ")
        if not login(username, appPass):
            logger.warning('Autenticación incorrecta, finalizando creación de contraseña')
            return
    except:
        logger.error('Ocurrió un error en el proceso de autenticación')
        return
    logger.info('Usuario autenticado')
    try:
        logger.info('Inicio de proceso de recuperación de contraseña')
        keyword = input("Por favor ingrese una palabra clave asociada con la contraseña: ")
        salt = b'salt_'  # You should use a different salt for each user
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(appPass.encode())
        key = base64.urlsafe_b64encode(key)
        f = Fernet(key)
        file = open("{}.txt".format(username), 'r')
        num_lines = len(file.readlines())
        file.close()
        count = 0
        file = open("{}.txt".format(username), 'r')
        file.readline()
        plaintext = ""
        while count < num_lines:
            text = base64.urlsafe_b64decode(file.readline()).decode()
            if text != "":
                text = f.decrypt(text).decode()
            if keyword == text.split(":")[0]:
                logger.info("Se encontró contraseña coincidente")
                plaintext = text.split(":")[1]
                print("La contraseña es: ", plaintext,"\n")
            count += 1
        if plaintext == "":
            print("No se ha encontrado la contraseña o no existe \n")
        
    except:
        logger.error('Ocurrió un error en la recuperación de contraseña')
        return
    logger.info('Cerrando proceso de recuperación de contraseña')
    return
def user():
    global username
    while True:
        logger.info('Ingresado a menú principal de usuario')
        print(
            '''Usuario\n\n
            Por favor seleccione una opción:\n\n
            1. Crear contraseña
            2. Recuperar contraseña
            3. Modificar contraseña
            4. Eliminar contraseña
            5. Generador de contraseñas
            6. Cerrar sesión
            ''')
        try:
            option = int(input("Ingrese una opción: "))
            if option == 1:
                create_password()
            elif option == 2:
                get_password()
            elif option == 3:
                change_password()
            elif option == 4:
                print()
            elif option == 5:
                generator()
            elif option == 6:
                logger.info('Opción seleccionada: Cerrar sesión')
                break
            else:
                print("Opción incorrecta, por favor ingrese una opción nuevamente")
                logger.warning('Opción seleccionada incorrecta')  
        except:
            print("Opción incorrecta, por favor ingrese una opción nuevamente")
            logger.warning('Opción seleccionada incorrecta')
    username = ""
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
    global username
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
    username = ""
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
    global username
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