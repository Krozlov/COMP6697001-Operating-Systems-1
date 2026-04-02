# BINUS University International
## COMP6697001 Operating Systems
### Assignment 1 Producer-Consumer Thread Sync

---

## Description

Multi-threaded program with **1 Producer** and **2 Consumer** threads:

- **Producer** generates random integers in range `[1, 10000]` and pushes them to a bounded stack buffer. All generated numbers are written to `all.txt`.
- **Consumer 1 (Even)** removes even numbers from the top of the stack → writes to `even.txt`
- **Consumer 2 (Odd)** removes odd numbers from the top of the stack → writes to `odd.txt`

---

## Synchronization Tools Used

| Tool | Purpose |
|---|---|
| `threading.Lock` | Mutual exclusion for buffer access |
| `threading.Semaphore` | Counting semaphores (empty slots, filled slots) |
| `threading.Condition` | Allows consumers to peek and wait without removing wrong-parity items |

> **Standard libraries only:** `threading`, `random`, `time`

---

## Execution Time

| Metric | Value |
|---|---|
| Days | 0 |
| Hours | 0 |
| Minutes | 0 |
| **Seconds** | **0** |
| Milliseconds | 661 |
| Ticks | 6,618,787 |
| TotalDays | 7.66063310185185E-06 |
| TotalHours | 0.000183855194444444 |
| TotalMinutes | 0.0110313116666667 |
| **TotalSeconds** | **0.6618787** |
| TotalMilliseconds | 661.8787 |

---

## Output Files

| File | Contents |
|---|---|
| `all.txt` | All 10,000 generated numbers in order |
| `even.txt` | Only even numbers removed from stack |
| `odd.txt` | Only odd numbers removed from stack |