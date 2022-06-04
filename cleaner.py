from datetime import datetime
import time
while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if current_time == '00:00:00':
        open('already used','w').write('000|')
    time.sleep(1)
    print(current_time)
