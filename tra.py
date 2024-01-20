import PySimpleGUI as gui

def showtime():
    window['-AOUT-'].update(ATime)
    window['-BOUT-'].update(BTime)
    window['plus-S1'].update('s')
    window['plus-S2'].update('s')

ATime = BTime = 50
has_bus_A = has_bus_B = False
has_pedestrian_A = has_pedestrian_B = False  # 新增两个变量来记录是否有行人
gui.set_options(font=("Consolas", 16))
layout = [
    [gui.Text('A Rd. Traffic Flow'), gui.Input(key='-ATF-', size=(5, 1)), gui.Text('vehicles/s')],
    [gui.Text('B Rd. Traffic Flow'), gui.Input(key='-BTF-', size=(5, 1)), gui.Text('vehicles/s')],
    [gui.Text('A Rd. Incident Rate'), gui.Input(key='-AIR-', size=(3, 1)), gui.Text('%')],
    [gui.Text('B Rd. Incident Rate'), gui.Input(key='-BIR-', size=(3, 1)), gui.Text('%')],
    [gui.Text('A Rd. Emergency'), gui.Radio('Give Way', 'AE', key='-AGT-'), gui.Radio('Block Way', 'AE', key='-ABW-'),
     gui.Radio('None', 'AE', key='-ANONE-')],
    [gui.Text('B Rd. Emergency'), gui.Radio('Give Way', 'BE', key='-BGT-'), gui.Radio('Block Way', 'BE', key='-BBW-'),
     gui.Radio('None', 'BE', key='-BNONE-')],
    [gui.Text('A Rd. Bus'), gui.Radio('Yes', 'ABus', key='-ABUS-'), gui.Radio('No', 'ABus', key='-ANOBUS-')],
    [gui.Text('B Rd. Bus'), gui.Radio('Yes', 'BBus', key='-BBUS-'), gui.Radio('No', 'BBus', key='-BNOBUS-')],
    [gui.Text('A Rd. Pedestrian'), gui.Radio('Yes', 'APedestrian', key='-APED-'), gui.Radio('No', 'APedestrian', key='-ANOPED-')],
    [gui.Text('B Rd. Pedestrian'), gui.Radio('Yes', 'BPedestrian', key='-BPED-'), gui.Radio('No', 'BPedestrian', key='-BNOPED-')],
    [gui.OK()],
    [gui.Text('A Rd. Time: '), gui.Text(key="-AOUT-"), gui.Text(key='plus-S1')],
    [gui.Text('B Rd. Time: '), gui.Text(key="-BOUT-"), gui.Text(key='plus-S2')],
]
window = gui.Window("Real-time Signal Timing System", layout, size=(1200, 740))
while True:
    event, values = window.read()
    print(event, values)

    if values['-ABW-']:
        ATime = 0
        BTime = 100
    elif values['-BBW-']:
        BTime = 0
        ATime = 100
    else:
        ATime = 100 * int(values['-ATF-']) / (int(values['-ATF-']) + int(values['-BTF-']))
        BTime = 100 * int(values['-BTF-']) / (int(values['-ATF-']) + int(values['-BTF-']))
        ATime += 5 * int(values['-AIR-']) / 100
        BTime += 5 * int(values['-BIR-']) / 100

    # 检查是否有公交车，如果有，则增加10秒时间
    if values['-ABUS-']:
        ATime += 10
    if values['-BBUS-']:
        BTime += 10

    # 检查是否有行人，如果有，则减少20%时间
    if values['-APED-']:
        ATime *= 0.8
    if values['-BPED-']:
        BTime *= 0.8

    showtime()

    if event == gui.WIN_CLOSED or event == "Exit":
        break

window.close()
