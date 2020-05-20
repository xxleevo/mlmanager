import time
import sys
import threading


class Manager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("Processing file #{} started...".format(x))
        time.sleep(1)
        print(" finished.")


if __name__ == "__main__":
    print("Script started.")
    x = 0
    while True:
        x += 1
        task = Manager()
        task.start()
        try:
            task.join()
        except KeyboardInterrupt:
            break

    print("Bye")
    print("x=", x)

    sys.exit()
