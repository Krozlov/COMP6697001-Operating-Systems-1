"""
BINUS University International
COMP6697001 - Operating Systems
Assignment 1 - Producer-Consumer with Thread Synchronization

Description:
    Multi-threaded program with 1 Producer and 2 Consumer threads.
    - Producer generates random integers [1, 10000] and pushes to a bounded stack buffer.
    - Consumer 1 (even): removes even numbers from top of stack -> even.txt
    - Consumer 2 (odd):  removes odd numbers from top of stack -> odd.txt
    - Producer also writes ALL generated numbers -> all.txt

Synchronization tools used:
    - threading.Lock      : mutual exclusion for buffer access
    - threading.Semaphore : counting semaphores (empty slots, filled slots)
    - threading.Condition : to allow consumers to peek and wait without removing wrong parity

Standard libraries only: threading, random, time

Days              : 0
Hours             : 0
Minutes           : 0
Seconds           : 1
Milliseconds      : 815
Ticks             : 18154703
TotalDays         : 2.10123877314815E-05
TotalHours        : 0.000504297305555556
TotalMinutes      : 0.0302578383333333
TotalSeconds      : 1.8154703
TotalMilliseconds : 1815.4703

"""

import threading
import random
import time

# ─── Constants ───────────────────────────────────────────────────────────────
LOWER_NUM   = 1
UPPER_NUM   = 10000
BUFFER_SIZE = 100
MAX_COUNT   = 10000

# ─── Shared state ─────────────────────────────────────────────────────────────
buffer      = []                          # stack (LIFO)
lock        = threading.Lock()
not_empty   = threading.Condition(lock)   # signals consumers when data is available
not_full    = threading.Condition(lock)   # signals producer when space is available

produced_count  = 0                       # how many numbers producer has pushed total
consumed_count  = 0                       # how many numbers consumers have removed total
all_numbers     = []                      # all generated numbers (for all.txt)

# ─── Producer ─────────────────────────────────────────────────────────────────
def producer():
    global produced_count

    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)

        with not_full:
            # Wait until there is space in the buffer
            while len(buffer) >= BUFFER_SIZE:
                not_full.wait()

            buffer.append(num)
            all_numbers.append(num)
            produced_count += 1

            # Wake up both consumers
            not_empty.notify_all()

# ─── Consumer factory ─────────────────────────────────────────────────────────
def consumer(parity: int, filename: str):
    """
    parity=0 -> even consumer  (writes to even.txt)
    parity=1 -> odd  consumer  (writes to odd.txt)
    """
    global consumed_count
    results = []

    while True:
        with not_empty:
            while True:
                # Exit condition: all produced and consumed
                if consumed_count >= MAX_COUNT:
                    break

                if buffer:
                    top = buffer[-1]
                    if top % 2 == parity:
                        # Correct parity — remove it
                        buffer.pop()
                        consumed_count += 1
                        results.append(top)

                        # Signal producer that a slot freed up
                        not_full.notify_all()
                        break
                    else:
                        # Wrong parity — peek only, wait for the other consumer
                        not_empty.wait(timeout=0.001)
                else:
                    # Buffer empty — wait for producer
                    not_empty.wait(timeout=0.001)

            if consumed_count >= MAX_COUNT and (not buffer or buffer[-1] % 2 != parity):
                # Check one more time if there's still work for this consumer
                # Drain remaining matching numbers before exiting
                while buffer and buffer[-1] % 2 == parity:
                    top = buffer.pop()
                    consumed_count += 1
                    results.append(top)
                    not_full.notify_all()
                break

    # Write results to file
    with open(filename, "w") as f:
        for n in results:
            f.write(f"{n}\n")

# ─── Main ──────────────────────────────────────────────────────────────────────
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

    # Write all.txt after all threads finish
    with open("all.txt", "w") as f:
        for n in all_numbers:
            f.write(f"{n}\n")

    print("Done. Files written: all.txt, even.txt, odd.txt")

if __name__ == "__main__":
    main()