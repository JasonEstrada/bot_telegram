import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from sympy import *
from estrellas import estrellas, constelacion
import RRNH 

bot = telebot.TeleBot("6141107908:AAEfYAug7bei9kW80EWyvSxlb8jFc9E7kQ4")

@bot.message_handler(commands=["start"])
def start(message):
    audio = open('media/bienvenido.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)
    audio.close()
    photo = open("media\gato-baile.gif", 'rb')
    bot.send_animation(message.chat.id, photo)
    photo.close()
    bot.send_message(message.chat.id, "Miaw!👋😺, ¿cómo estás? Estos son los comandos disponibles:")
    comandos(message)

@bot.message_handler(commands=["help"])
def ayuda(message):
    print("entra 2")
    bot.reply_to(message, "Estas son las ayudas ... ") # HACER LAS AYUDASSSSSS

@bot.message_handler(commands=["commands"])
def comandos(message):
    commands_list = ""
    with open("comandos.txt", "r", encoding="utf-8") as f:
        for line in f:
            commands_list += line
    bot.reply_to(message, commands_list)

@bot.message_handler(commands=["estrella"])
def estrella(message):
    grafico_estrellas(message.chat.id)

@bot.message_handler(commands=["constelaciones"])
def constelaciones(message):
    constelaciones_list = "/boyero\n/casiopea\n/cazo\n/cygnet\n/geminis\n/hydra\n/osa_mayor\n/osa_menor"
    bot.reply_to(message, f"Elige una constelación 🌌: \n {constelaciones_list}")

@bot.message_handler(commands=["boyero"])
def boyero(message):
    print("entra 1")
    grafico_constelacion("Boyero", message.chat.id)

@bot.message_handler(commands=["casiopea"])
def casiopea(message):
    grafico_constelacion("Casiopea", message.chat.id)

@bot.message_handler(commands=["cazo"])
def cazo(message):
    grafico_constelacion("Cazo", message.chat.id)

@bot.message_handler(commands=["cygnet"])
def cygnet(message):
    grafico_constelacion("Cygnet", message.chat.id)

@bot.message_handler(commands=["geminis"])
def geminis(message):
    grafico_constelacion("Geminis", message.chat.id)

@bot.message_handler(commands=["hydra"])
def hydra(message):
    grafico_constelacion("Hydra", message.chat.id)

@bot.message_handler(commands=["osa_mayor"])
def osa_mayor(message):
    grafico_constelacion("Osa mayor", message.chat.id)

@bot.message_handler(commands=["osa_menor"])
def osa_menor(message):
    grafico_constelacion("Osa menor", message.chat.id)

@bot.message_handler(commands=["rrnh"])
def rrnh(message):
    bot.send_message(message.chat.id, "¿Cuál es el grado de la función recurrente?")
    bot.register_next_step_handler(message, pedir_grado)

def pedir_grado(message):
    try:
        RRNH.k = int(message.text)
        if RRNH.k <= 0:
            bot.send_message(message.chat.id, "El grado debe ser mayor que 0😾, intenta de nuevo")
            bot.register_next_step_handler(message, pedir_grado)
        else:
            bot.send_message(message.chat.id, "¿Qué tipo de termino no homogeneo es g(n)?🥸\n\t1. Constante\n\t2. Valor n\n\t3. Valor n^2 \n\t4. Raíz de grado n")
            bot.register_next_step_handler(message, grado)
    except ValueError:
        bot.send_message(message.chat.id, "Ese tipo de dato no es correcto, miaw miaw! 😿\nIntenta de nuevo con un número")
        rrnh(message)

def grado(message):
    try:
        RRNH.dec_g = int(message.text)
        if message.text=="1":
            bot.send_message(message.chat.id, "¿Cuál es el valor de la constante?")
            bot.register_next_step_handler(message, constante)
        elif message.text == "2":
            RRNH.g = RRNH.n
            pedir_condiciones(message)
        elif message.text == "3":
            RRNH.g = RRNH.n**2
            pedir_condiciones(message)
        elif message.text == "4":
            bot.send_message(message.chat.id, "¿Cuál es el valor de la raíz? 🤓")
            bot.register_next_step_handler(message, valor_R)
        else:
            bot.send_message(message.chat.id, "Solo hay 4 opciones, selecciona una (escribe el número) 😾")
            bot.register_next_step_handler(message, grado)
    except ValueError:
        bot.send_message(message.chat.id, "Ups, algo pasó con ese dato, intenta otra vez")
        bot.register_next_step_handler(message, grado)
    

def constante(message):
    try:
        RRNH.g = int(message.text)
        pedir_condiciones(message)
    except ValueError:
        bot.send_message(message.chat.id, "Ese tipo de dato no es correcto, miaw miaw! 😿\nIntenta de nuevo con un número")
        bot.register_next_step_handler(message, constante)


def valor_R(message):
    try:
        RRNH.R = int(message.text)
        RRNH.g = RRNH.R**RRNH.n
        pedir_condiciones(message)
    except ValueError:
        bot.send_message(message.chat.id, "Ese tipo de dato no es correcto, miaw miaw! 😿\nIntenta de nuevo con un número")
        bot.register_next_step_handler(message, valor_R)

def pedir_coeficientes(message):
    bot.send_message(message.chat.id, "¿Cuáles son los coeficientes de " + "".join("f(n -" + str(i) +"), " for i in range(RRNH.k, 1, -1)) + f" y f(n-1)? Ingresalos separados por comas.")
    bot.register_next_step_handler(message, coeficientes)

def coeficientes(message):
    RRNH.coeff = []
    check = true
    try:
        coef_ingresado = message.text.split(",")
        for c in coef_ingresado: 
            RRNH.coeff.append(-int(c))

        if len(RRNH.coeff)!=RRNH.k:
            bot.send_message(message.chat.id, f"Jum, la cantidad de números ingresados es {len(RRNH.coeff)} y el grado de la función es {RRNH.k}, deberían ser iguales, vuelve a ingresar los números 🤔")
            bot.register_next_step_handler(message, coeficientes)
            RRNH.coeff = []
            check = false
        
        if check: 
            RRNH.principal_rrnh()
        bot.send_photo
        
        #bot.send_message(message.chat.id, "Esta es la función recurrente que ingresaste: ")
        photo = open('function.png', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Esta es la función recurrente que ingresaste")
        photo.close()
        #bot.send_photo(message.chat.id, open('function.png', 'rb'))

        photo = open('sol_h.png', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Esta es la solución homogénea que resulta en términos de b")
        photo.close()

        if(RRNH.dec_g != 4):
            print("entra")
            photo = open('sol_p.png', 'rb')
            bot.send_photo(message.chat.id, photo, caption="Esta es la solución particular que resulta del termino g(n)")
            photo.close()

        photo = open('expr.png', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Esta es la solución general de la función")
        photo.close()

        photo = open('ec_sol.png', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Esta es la solución no recurrente de la función en términos de n")
        photo.close()

        RRNH.dec_g = 0
        #set variables from RRNH to default
        RRNH.k = 0
        RRNH.g = 0
        RRNH.R = 0
        RRNH.coeff = []
        RRNH.init = []
        RRNH.funcion_p = []
        RRNH.funcion = []
 
    except ValueError:
        bot.send_message(message.chat.id, f"Hubo un error, recuerda que debes ingresar números separados por comas. Intenta de nuevo 🤔")
        bot.register_next_step_handler(message, coeficientes)
    

def pedir_condiciones(message):
    bot.send_message(message.chat.id, "¿Cuáles son los valores de " + "".join("f(" + str(i) +"), " for i in range(RRNH.k-1)) + f" y f({RRNH.k-1})? Ingresalos separados por comas.")
    bot.register_next_step_handler(message, condiciones_iniciales)

def condiciones_iniciales(message):
    RRNH.init = []
    check = true
    try:
        condiciones = message.text.split(",")
        for condicion in condiciones: 
            RRNH.init.append(int(condicion))
        if len(RRNH.init)!=RRNH.k:
            bot.send_message(message.chat.id, f"Jum, la cantidad de números ingresados es {len(RRNH.init)} y el grado de la función es {RRNH.k}, deberían ser iguales, vuelve a ingresar los números 🤔")
            bot.register_next_step_handler(message, condiciones_iniciales)
            RRNH.init = []
            check = false
        if check: 
            pedir_coeficientes(message)

    except ValueError:
        bot.send_message(message.chat.id, f"Hubo un error, recuerda que debes ingresar números separados por comas. Intenta de nuevo 🤔")
        bot.register_next_step_handler(message, condiciones_iniciales)


@bot.message_handler(func=lambda message:True)


def mensaje(message):
    comandos(message)

def enviar_archivos(id, src_pic):
    photo = open(src_pic, 'rb')
    bot.send_photo(id, photo)
    photo.close()
    document = open('grafico.html', 'rb')
    bot.send_document(id, document, caption="Para ver con más detalle, abre este archivo en tu navegador favorito. 🤫Tranquilo, es 100% confiable.")
    document.close()
    
def grafico_estrellas(id):
    estrellas()
    enviar_archivos(id, "Coordenadas estrellas.png", caption="Aquí tienes un gráfico con todas las estrellas")

def grafico_constelacion(conste, id):
    constelacion(conste)
    enviar_archivos(id, "Constelacion.png", caption=f"Aquí tienes la constelación {conste}")


bot.polling()