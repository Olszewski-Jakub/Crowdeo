# uart_handler.py
from machine import UART
from time import sleep

uart = UART(0, baudrate=9600)


def uart_write(data):
    uart.write((data + "\n").encode('utf-8'))
    sleep(0.5)
