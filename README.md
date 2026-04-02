# BINUS University International
## COMP6697001 - Operating Systems
### Assignment 1 — Producer-Consumer Thread Synchronization

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
| **Seconds** | **1** |
| Milliseconds | 815 |
| Ticks | 18,154,703 |
| TotalDays | 2.10123877314815E-05 |
| TotalHours | 0.000504297305555556 |
| TotalMinutes | 0.0302578383333333 |
| **TotalSeconds** | **1.8154703** |

---

## Output Files

| File | Contents |
|---|---|
| `all.txt` | All 10,000 generated numbers in order |
| `even.txt` | Only even numbers removed from stack |
| `odd.txt` | Only odd numbers removed from stack |