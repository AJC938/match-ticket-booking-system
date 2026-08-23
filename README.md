# Match Ticket Booking System

<div align="center">

<img src="assets/project-banner.png" alt="Match Ticket Booking System" width="100%">

</div>

A Python-based **Data Structures & Algorithms** project that simulates a high-demand football match ticket booking system and evaluates how algorithmic choices affect lookup, sorting, and booking performance.

> **Course:** EE367 — Data Structures & Algorithms  
> **Institution:** King Abdulaziz University  
> **Department:** Electrical & Computer Engineering

## Overview

Ticket releases can create a burst of users competing for a limited number of seats. This project models that scenario and uses purpose-built data structures and algorithms to manage users, booking requests, seats, and performance measurements.

The system provides two operating approaches:

- **Standard:** Linear Search + Bubble Sort
- **Optimized:** Hash Table + Binary Search + Merge Sort + Binary Min-Heap Priority Queue

The application then exposes operational KPIs and benchmark results so the effect of those choices can be observed rather than discussed only theoretically.

## Key Features

- Football match selection and ticket booking workflow
- Custom Hash Table with separate chaining and dynamic resizing
- Priority Queue implemented with a Binary Min-Heap
- 2D seat grid for real-time seat availability
- Merge Sort and Bubble Sort implementations
- Linear Search, Binary Search, and Hash Search implementations
- Priority-based booking windows for VIP, High-Attendance, and General users
- Automatic generation of mock users
- Persistent storage for newly registered users
- Admin dashboard with live booking state and simulation controls
- Automatic booking simulation for high-demand scenarios
- KPI tracking for waiting time, processing time, throughput, occupancy, revenue, and lookups
- Built-in performance benchmarking for search and sorting algorithms
- Tkinter GUI with no third-party Python dependencies

## Data Structures & Algorithms

| Component | Implementation | Complexity | Purpose |
|---|---|---:|---|
| User lookup | Custom Hash Table | O(1) average | Fast Fan ID lookup |
| Booking queue | Binary Min-Heap Priority Queue | O(log n) push/pop | Process requests by priority |
| Seat management | 2D Array | O(1) indexed access | Track seat availability |
| Sorting | Merge Sort | O(n log n) | Efficient attendance ordering |
| Sorting baseline | Bubble Sort | O(n²) | Benchmark baseline |
| Searching | Binary Search | O(log n) | Lookup in sorted user data |
| Searching baseline | Linear Search | O(n) | Benchmark baseline |
| Searching optimized | Hash Search | O(1) average | Direct lookup through the Hash Table |

## Booking Priority Model

Booking requests are processed according to user tier:

1. **VIP** — highest priority
2. **High Attendance**
3. **General** — lowest priority

The priority queue uses the tier value as its ordering key, allowing higher-priority requests to be processed first while retaining FIFO behavior for requests with the same priority.

## Seat Model

The simulated stadium contains **392 seats** across three zones:

| Zone | Seats | Price Multiplier |
|---|---:|---:|
| VIP | 48 | ×4 |
| Premium / High | 144 | ×2 |
| General | 200 | ×1 |
| **Total** | **392** | — |

Users can select up to two seats per match. Seat state is maintained through a dedicated 2D grid abstraction.

## System Workflow

```text
Match Selection
      ↓
Fan Login / Registration
      ↓
User Lookup
(Hash / Linear / Binary depending on mode)
      ↓
Seat Selection
      ↓
Booking Request
      ↓
Priority Queue
(Binary Min-Heap)
      ↓
Booking Processing
      ↓
Seat Grid Update
      ↓
KPI Collection
```

## Performance Evaluation

The project includes a benchmarking layer to compare algorithmic alternatives.

### Search Benchmark

- Linear Search — O(n)
- Binary Search — O(log n)
- Hash Search — O(1) average

### Sorting Benchmark

- Bubble Sort — O(n²)
- Merge Sort — O(n log n)

The benchmark interface reports timing measurements and the repository includes the resulting comparison charts under [`results/`](results/).

## KPIs

The booking simulation records operational metrics including:

- **Average Waiting Time** — average time a request spends waiting before processing
- **Processing Time** — time spent processing booking requests
- **Throughput** — booking processing rate
- **Lookup Time** — user lookup performance
- **Occupancy** — booked seats relative to total capacity
- **Revenue** — revenue generated from successful seat assignments
- **Bookings Processed / Rejected** — booking outcome counts

These metrics connect the underlying DSA implementations to observable system behavior.

## Project Structure

```text
match-ticket-booking-system/
├── README.md
├── .gitignore
├── assets/
│   └── project-banner.png
├── src/
│   ├── main.py
│   └── modules/
│       ├── __init__.py
│       ├── booking_system.py
│       ├── hash_table.py
│       ├── match_catalogue.py
│       ├── mock_database.py
│       ├── models.py
│       ├── priority_queue.py
│       ├── searching.py
│       ├── seat_grid.py
│       ├── sorting.py
│       └── user_store.py
├── results/
│   ├── KPI_Linear_vs_Binary_Search.png
│   └── KPI_Merge_vs_Bubble_Sort.png
└── docs/
    └── README.md
```

## Requirements

- Python **3.8+**
- Tkinter

No third-party Python packages are required.

### Linux

If Tkinter is not installed:

```bash
sudo apt install python3-tk
```

## Run the Application

From the repository root:

```bash
python src/main.py
```

The application opens the match-selection interface. The Admin Dashboard provides session controls, live seat monitoring, automatic simulation, KPI information, and DSA benchmarking.

## Sample Fan IDs

The mock database includes examples such as:

```text
VIP001
VIP002
VIP003
HA001
HA005
HA010
GP001
GP010
GP025
```

If an unknown ID is entered, the system registers it as a General-tier user and persists it locally in `src/registered_users.json`. That runtime file is intentionally excluded from Git tracking.

## Why This Is a DSA Project

The booking interface is only the application layer. The core objective is to demonstrate the effect of data-structure and algorithm selection on a realistic workload.

The project follows this engineering flow:

```text
Real-world problem
       ↓
Data structure selection
       ↓
Algorithm implementation
       ↓
Baseline implementation
       ↓
Benchmarking
       ↓
KPI measurement
       ↓
Performance analysis
```

This makes the project suitable for demonstrating practical understanding of **hash tables, heaps, arrays, searching, sorting, asymptotic complexity, simulation, and performance analysis**.

## Results

The repository contains the benchmark comparison charts generated by the project:

- [Linear Search vs Binary Search](results/KPI_Linear_vs_Binary_Search.png)
- [Merge Sort vs Bubble Sort](results/KPI_Merge_vs_Bubble_Sort.png)

## Academic Materials

The original course report and presentation were intentionally not copied into this public-ready repository because they contain student identification numbers. They can be kept privately or added manually if the team decides that publishing those details is appropriate.

## Team

- Abdulaziz Alzahrani — GUI & Coding
- Abdullah Almutiri — Report Writing & Coding
- Abdulaziz Alqassab — Presentation & Coding
- Ali Almalki — GUI & Coding

## License

This repository is an academic team project created for EE367 at King Abdulaziz University. No open-source license is currently declared.
