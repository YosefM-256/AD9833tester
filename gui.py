import PySimpleGUI as psg
import serial
import time

wave = None

esp = serial.Serial(baudrate = 250e3, port = "COM3")

layout = [[psg.Text("Frequency:"), psg.Input(key = 'f')],\
          [psg.Button('sine'),psg.Button('square'),psg.Button('triangle')],\
          [psg.Button(button_text = 'update')]]

win = psg.Window("GUI", layout)

while True:
    event, values = win.read()
    if event in (psg.WIN_CLOSED, 'Exit'):
        win.close()
        esp.close()
        break
    if event in ('sine', 'triangle', 'square'):
        win[event].update(button_color = ('white', 'red'))
        if wave:
            win[wave].update(button_color = ('#FFFFFF', '#283b5b'))
        wave = str(event)
    if event == 'update':
        if wave:
            txt = values['f']
            mul=1
            if txt[-1] in ('k', 'K', 'M'):
                mul = {'k':1e3,'K':1e3,'M':1e6}[txt[-1]]
                txt = txt[:-1]
            try:
                num = float(txt)*(2**28)*mul/25e6
            except ValueError:
                print("could not convert", txt, "into float")
            num = int(num)
            to_send = []
            for i in range(4):
                to_send.append(num%128)
                num //= 128
            to_send.append({'sine':0,'triangle':1,'square':2}[wave])
            to_send[0] += 128
            print(num, to_send)
            esp.write(to_send)
    print(event, values)
