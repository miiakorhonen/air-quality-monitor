# Kirjastot:
# adafruit_ssd1306.mpy
# adafruit_display_text/
# displayio
# terminalio

import board
import busio
import displayio
import terminalio
import audiocore
import audiopwmio
import adafruit_scd4x
import time
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import i2cdisplaybus
import adafruit_bitmap_font.bitmap_font as bitmap_font

# pins
audio = audiopwmio.PWMAudioOut(board.GP14)  # speaker pin

led_green = digitalio.DigitalInOut(board.)
led_green.direction = digitalio.Direction.OUT

led_yellow = digitalio.DigitalInOut(board.)
led_yellow.direction = digitalio.Direction.OUT

led_red = digitalio.DigitalInOut(board.)
led_red.direction = digitalio.Direction.OUT

switch = True  # TODO placeholder

# i2c
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)  # jaetaan anturille ja näytölle

scd4x = adafruit_scd4x.SCD4X(i2c)  # scd40. oletusosoite 0x62

display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)  # display address

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)  # oled definition


def measure():
    """
    Measures values from scd40.
    """

    scd4x.start_periodic_measurement()
    if scd4x.data_ready:
        co2 = round(scd4x.CO2)
        temp = round(scd4x.temperature, 1)
        hum = round(scd4x.relative_humidity, 1)
    else:
        co2, temp, hum = 20
    return co2, temp, hum


def convert_temp(temp):
    """
    Reads temp and returns it as a string.
    """

    temperature = str(round(temp))
    return temperature


def play_sound(filename):
    """
    Plays the selected audio file.
    """

    # try the filename TODO
    path = "sounds/"
    with open(path + filename + ".wav", "rb") as wave_file:
        wave = audiocore.WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            print("soittaa...")
            # pass	# koodi, joka halutaan suoritettavan kun ääni soi
        print("valmis")


def draw_text(number, unit):
    """
    Draws text on the OLED display.
    """

    displayio.release_displays()
    # Lataa fontti (vaihda polku tarpeen mukaan)
    font = bitmap_font.load_font("/fonts/Arial-Bold-24.bdf")
    main_group = displayio.Group()
    line1 = label.Label(font, text=number + unit, color=0xFFFFFF, x=0, y=12)
    # line2 = label.Label(font, text="Ilmankosteus", color=0xFFFFFF, x=0, y=12)

    main_group.append(line1)
    # main_group.append(line2)
    display.root_group = main_group


def speak():
    """
    Speech logic to main when the keyword has been detected.
    """

    co2, temp, hum = measure()

    draw_text(convert_temp(temp), "°C")

    play_sound("alku")
    time.sleep(0.2)
    play_sound(convert_temp(temp))
    time.sleep(0.2)
    play_sound("C")


def display():
    """
    Displaying data on the display in main.
    """

    co2, temp, hum = measure()

    if keyword is True:
        speak()
        draw_text(str(temp), "°C")
        time.sleep(10)
        if keyword is True:
            speak()
        draw_text(str(hum), "%")
        time.sleep(10)
        if keyword is True:
            speak()
        draw_text(str(co2), "ppm")
        time.sleep(10)

while True:
    if switch is True:  # TODO kytkinlogiikka
        co2, temp, hum = measure()
        if co2 < 800:
            led_green = True
            led_yellow = False
            led_red = False
            if keyword is True:
                speak()

            else:
                display()

        elif co2 => 800 and co2 =< 1200:
            led_green = False
            led_yellow = True
            led_red = False
            if keyword is True:
                speak()

            else:
                display()

        elif co2 > 1200:
            led_green = False
            led_yellow = False
            led_red = True

            if keyword is True:
                speak()

            else:
                display()
