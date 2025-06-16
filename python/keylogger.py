import keyboard

print("Press keys (press ENTER to stop):")

while True:
    event = keyboard.read_event()
    if event.event_type == 'down':
        print(event.name)
        if event.name == 'enter':
            print("Exiting...")
            break
