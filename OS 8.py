import threading
import time
import random

resource = threading.Semaphore(1)   
read_count_lock = threading.Lock()  
turnstile = threading.Semaphore(1)  

read_count = 0
shared_data = "Initial Data"


def reader(reader_id):
    global read_count

    turnstile.acquire()
    turnstile.release()

    with read_count_lock:
        read_count += 1
        if read_count == 1:
            resource.acquire()  

    print(f"Reader {reader_id} is reading: {shared_data}")
    time.sleep(random.uniform(0.5, 1))

    with read_count_lock:
        read_count -= 1
        if read_count == 0:
            resource.release()   

    print(f"Reader {reader_id} finished.")


def writer(writer_id):
    global shared_data

    turnstile.acquire()
    resource.acquire()

    shared_data = f"Data written by Writer {writer_id}"
    print(f"Writer {writer_id} is writing...")
    time.sleep(1)
    print(f"Writer {writer_id} finished writing.")

    resource.release()
    turnstile.release()


threads = [
    threading.Thread(target=reader, args=(1,)),
    threading.Thread(target=reader, args=(2,)),
    threading.Thread(target=writer, args=(1,)),
    threading.Thread(target=reader, args=(3,)),
    threading.Thread(target=writer, args=(2,))
]

for t in threads:
    t.start()

for t in threads:
    t.join()

print("\nAll readers and writers completed successfully.")
