import PySimpleGUI as pg
import time
# TODO: implement threading for timer
from queue import Queue, Empty
from threading import Thread


counter = 5 * 60

remainder = counter

def keep_time(remainder, q):
    # remainder = counter
    started = False
    while remainder > 0:
        # remainder = counter - i
        prog_bar.UpdateBar(remainder, counter)
        text_box.Update(f'{remainder // 60}:{remainder % 60:02d}')
        if started:
            remainder -= 1
        try:
            diff = q.get(timeout=1)
            if isinstance(diff, str):
                if diff == "exit":
                    return
                elif diff == "pause":
                    paused = True
                    while paused:
                        diff = q.get()
                        if isinstance(diff, str):
                            if diff == "start":
                                paused = False
                        elif isinstance(diff, int):
                            remainder += diff
                            prog_bar.UpdateBar(remainder, counter)
                            text_box.Update(f'{remainder // 60}:{remainder % 60:02d}')
                elif diff == "start":
                    started = True
            elif isinstance(diff, int):
                remainder += diff
        except Empty:
            pass
        # time.sleep(1)

    time.sleep(5)
    window.close()


layout = [
    [
        pg.ProgressBar(1, orientation='v', size=(20, 20), key='progress'),
        pg.Text(f'{counter // 60}:{counter % 60:02d}', key='text',
                font=("Helvetica", 55)),
        [
            pg.Button('Start', key='start'),
            pg.Button('Pause', key='pause')
        ]
    ],
    [
        pg.Button('+15 seconds', key='addsecs'),
        pg.Button('-30 seconds', key='subsecs')
    ],
    [
        
        pg.Text('  00  ', key='points', font=("Helvetica", 55),
                justification="top")
    ],
    *[
    [
        pg.Button(f'-{i}', key=f'm{i}'),
        pg.Button(f'+{i}', key=f'p{i}')
    ] for i in range(1, 7)
    ]
]

window = pg.Window('tick tick BOOM', layout).Finalize()

prog_bar = window.FindElement('progress')
text_box = window.FindElement('text')

start_button = window.FindElement('start')
score_text = window.FindElement('points')
addsecs = window.FindElement('addsecs')
subsecs = window.FindElement('subsecs')

score = 0

prog_bar.UpdateBar(remainder, counter)
text_box.Update(f'{remainder // 60}:{remainder % 60:02d}')

q = Queue()
timer = Thread(target=keep_time, args=(remainder, q, ))
timer.start()
while True:
    event, values = window.read()
    print(event, values)
    if event == pg.WIN_CLOSED or event == 'Exit' or event is None:
        q.put("exit")
        break
    elif event == "addsecs":
        q.put(15)
    elif event == "subsecs":
        q.put(-30)
    elif event == "start":
        q.put("start")
    elif event == "pause":
        q.put("pause")
    elif event.startswith("m"):
        diff = int(event[1])
        score -= diff
        if score <= -100:
            score = -99
        print(f"{score}")
        if score >= 100 or score < 0:
            score_text.Update(f' {score:03d}  ')
        else:
            score_text.Update(f"  {score:02d}  ")
    elif event.startswith('p'):
        diff = int(event[1])
        score += diff
        if score >= 100 or score < 0:
            score_text.Update(f' {score:03d}  ')
        else:
            score_text.Update(f"  {score:02d}  ")


timer.join()
window.close()
