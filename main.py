import threading
import random
import time

LOWER_NUM   = 1
UPPER_NUM   = 10000
BUFFER_SIZE = 100
MAX_COUNT   = 10000

buffer      = []
lock        = threading.Lock()
not_empty   = threading.Condition(lock)
not_full    = threading.Condition(lock)

produced_count  = 0
consumed_count  = 0
all_numbers     = []

def producer():
    global produced_count

    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)

        with not_full:
            while len(buffer) >= BUFFER_SIZE:
                not_full.wait()

            buffer.append(num)
            all_numbers.append(num)
            produced_count += 1

            not_empty.notify_all()

def consumer(parity: int, filename: str):

    #0 -> even
    #1 -> odd

    global consumed_count
    results = []

    while True:
        with not_empty:
            while True:
                if consumed_count >= MAX_COUNT:
                    break

                if buffer:
                    top = buffer[-1]
                    if top % 2 == parity:
                        buffer.pop()
                        consumed_count += 1
                        results.append(top)

                        not_full.notify_all()
                        break
                    else:
                        not_empty.wait(timeout=0.001)
                else:
                    not_empty.wait(timeout=0.001)

            if consumed_count >= MAX_COUNT and (not buffer or buffer[-1] % 2 != parity):
                while buffer and buffer[-1] % 2 == parity:
                    top = buffer.pop()
                    consumed_count += 1
                    results.append(top)
                    not_full.notify_all()
                break

    with open(filename, "w") as f:
        for n in results:
            f.write(f"{n}\n")

def main():
    t_producer   = threading.Thread(target=producer, name="Producer")
    t_even       = threading.Thread(target=consumer, args=(0, "even.txt"), name="Consumer-Even")
    t_odd        = threading.Thread(target=consumer, args=(1, "odd.txt"),  name="Consumer-Odd")

    t_producer.start()
    t_even.start()
    t_odd.start()

    t_producer.join()
    t_even.join()
    t_odd.join()

    with open("all.txt", "w") as f:
        for n in all_numbers:
            f.write(f"{n}\n")

    print("Done. Files written: all.txt, even.txt, odd.txt")

if __name__ == "__main__":
    main()