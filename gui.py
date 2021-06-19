import PySimpleGUI as pg
import time
# TODO: implement threading for timer
from threading import Thread


counter = 5 * 60

layout = [
    [
        pg.ProgressBar(1, orientation='v', size=(20, 20), key='progress'),
        pg.Text(f'{counter // 60}:{counter % 60:02d}', key='text')
    ],
    [
        pg.Button('+15 seconds', key='addsecs'),
        pg.Button('-30 seconds', key='subsecs')
    ]
]

window = pg.Window('tick tick BOOM', layout).Finalize()

prog_bar = window.FindElement('progress')
text_box = window.FindElement('text')

addsecs = window.FindElement('addsecs')
subsecs = window.FindElement('subsecs')

for i in range(counter + 1):
    remainder = counter - i
    prog_bar.UpdateBar(remainder, counter)
    text_box.Update(f'{remainder // 60}:{remainder % 60:02d}')
    time.sleep(1)

time.sleep(5)
window.Close()
