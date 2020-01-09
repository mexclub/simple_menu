# Menu de aplicaciones basado en micropython y placa NodeMCU ESP8266

Para este ejemplo se esta usando una placa NodeMCU ESP8266 con firmware de micropython versión de firmware
**<a href="https://micropython.org/resources/firmware/esp8266-20190529-v1.11.bin">esp8266-20190529-v1.11.bin</a>**
el cual hs sido cargado siguiendo las 
**<a href="http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#deploying-the-firmware">instrucciones</a>**
del sitio de micropython.
Se esta usando los drivers para chipset **<a href="https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers">CP2102</a>**.

También es necesario contar con la aplicación de consola
**<a href="https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy">ampy de Adafruit</a>**
 para poder cargar los scripts de python a la placa NodeMCU

A continuación la tabla de conexiones:

| NodeMCU | Rotary Encoder |
| ------:| -----------:|
| D0 | Push Button (PB) |
| D3 | PinA |
| D4 | PinB |
| 3.3 | PullUp PinA/PinB/PB |
| GND | Middle Pin/PB |

Versión SPI

| NodeMCU | Display SPI 128x64 |
| ------:| -----------:|
| D1 | RES |
| D2 | DC |
| 3.3 | VDD |
| GND | GND |
| D5 | SCK |
| D7 | SDA |
| D8 | CS |

Versión I2C

| NodeMCU | Display I2C 128x64 |
| ------:| -----------:|
| 3.3 | VDD |
| GND | GND |
| D5 | SCK |
| D7 | SDA |


En la figura 1 se muestra de forma de conectar los componentes, para el caso de I2C se deben conectar solo los pines del 1 al 4, el resto se omite.

<center> <img src=img01.png> <br/>Figura 1 </center>

Se deben de copiar todos los archivos que se encuentren en la carpeta **simple_menu** hacia la raíz de la placa de la siguiente forma:

~~~bash
ampy -p com3 put main.py
ampy -p com3 put ssd1306.py
ampy -p com3 put simple_encoder.py
ampy -p com3 put simple_menu.py
ampy -p com3 put clock.py
ampy -p com3 put reset.py
ampy -p com3 put settings.json
~~~

com3 es el puerto Windows donde ha quedado instalado el controlador del chip usb-serial CH340G o CP2102 dependiendo del modelo de la placa. Si se tiene Linux el puerto generalmente es /dev/ttyUSB0


El archivo main.py es el primer programa que se carga al inicializar o reiniciar la placa. Aquí se muestra cu contenido en donde se puede ver como se inicializa el objeto *display* que se reutiliza en los módulos cargados, también se muestra la creación del menú y sus acciones de cada elemento del menú, dentro de cada aplicación puede contener un menú (submenu) o un programa final, dicho programa final debe tener una forma de finalizar para regresar el control al menú de donde se ejecutó. Se recomienda que la terminación del programa sea pulsando el push button del rotary encoder. Como ejemplo existe el archivo clock.py
~~~micropython
import time
import ssd1306
import simple_menu
from machine import SPI, Pin
# from machine import I2C, Pin

pb = Pin(16, Pin.IN)

# i2c = I2C(-1, Pin(14), Pin(13))
# display = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, external_vcc=False)
display = ssd1306.SSD1306_SPI(128,64,SPI(1), Pin(4), Pin(5), Pin(15), False)

menu_list = ['back', 'clock', 'alarm', 'wifi connect', 'settings', 'reset']
menu_actions = ['<BACK>', 'clock', 'alarm', 'wificonnect', 'settings', 'reset']
menu = simple_menu.simple_menu(display, pb, menu_list, menu_actions)

while True:
    display.fill_rect(0,0,128,64,0)
    display.text("{: ^16s}".format("WELCOME"),0,0,1)
    display.text("{: ^16s}".format("PRESS START"),0,30,1)
    display.show()

    if not pb.value():
        menu.show()
    time.sleep_ms(10)
~~~

Algunos videos de Youtube para complementar información:

<iframe width="420" height="315"
src="https://www.youtube.com/channel/UCOhshmzwIlELoF38J2j9k-w">
</iframe>

