import keyboard
while True:
    try:
        if keyboard.is_pressed('q'):
            print('You Pressed A Key!')
            break
    except:
        break