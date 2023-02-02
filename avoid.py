import picar_4wd as fc
import time

speed = 10

def retrack():
    fc.backward(speed)
    time.sleep(1)
    fc.stop()
    fc.turn_right(speed)
    time.sleep(1)

def main():
    init = 1
    while True:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        tmp = scan_list[3:7] # only focus on reading from the car's line of vision
        print(tmp)
        if tmp != [2,2,2,2] and init == 0:
            retrack();
        else:
            fc.forward(speed)
            init = 0

if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()
