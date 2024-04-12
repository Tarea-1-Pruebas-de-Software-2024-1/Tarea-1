# MyPass

## Descripción

MyPass permite a sus usuarios gestionar sus contraseñas al permitir que gestionen permitiendo el guardado, edición, revisión y eliminación de sus contaseñas, todo esto de manera segura al requerir autenticación de usuario además de encriptación de las claves, además posee un modulo el cual permite generar contraseñas con los tipos de caracter preferidos por el usuario

## Instalación

El programa no requiere una instalación, sin embargo se requiere instalar [Python3](https://www.python.org/downloads/) y de los siguientes paquetes:

* [logging](https://pypi.org/project/logging/)
* [secrets](https://pypi.org/project/secrets/)
* [cryptography](https://pypi.org/project/cryptography/)
* [argon2](https://pypi.org/project/argon2-cffi/)

Estos se instalan ingresando el código entregado en su sitio en la consola.

## Cómo usar

Para usar MyPass debe ejecutar el archivo .py del programa con el comando "python MyPass.py", se le mostará las opciones de "Iniciar Sesión" y "Cerrar el programa", para crear un usuario se requiere que se encuentre como administrador en el sistema, luego de crear el nuevo usuario, puede cerrar sesión e iniciar sesión con su perfil de usuario, ya ingresado en el sistema se le presentarán las opciones "Crear contraseña", donde tendrá que ingresar su contraseña nuevamente, para propositos de seguridad, después tendrá que ingresar una contraseña que cumpla con los parámetros de longitud y una palabra clave (idealmente algo que permite identificar la plataforma para que sea fácil de recordar), "Recuperar contraseña", donde tendrá que autenticarse y ingresar la palabra clave asociada a su contraseña, "Modificar contraseña", donde tendrá que autenticarse y ingresar la palabra clave de la contraseña que desea modificar, si esta corresponde a alguna de las contraseñas se le permitirá generar el cambio ingresando la nueva contraseña, "Eliminar contraseña", donde tendrá que autenticarse y ingresar la palabra clave asociada a la contraseña que desea eliminar al ingresarla se eliminará la clave, "Generador de contraseñas", se le pedirá que elija los caracteres que puede contener su contraseña, ya sea, alfabeticos, alfanúmericos o alfanúmericos con signos de puntuación, y un largo que debe ser mínimo de 8 caracteres, al ingresar el valor se generará una contraseña con este formato.

## Cómo contribuir

La manera recomendada de realizar contribuciones a este proyecto es a traves del flujo de trabajo ["fork and pull request"](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project).

## Licencia

