# C-Labs

This repository contains first year of **KPI University FICE** Labs written in C.

Labs summaries:
- Lab 1: Simple algorithms that calculate **y** value and check it's existence for segments of a given function depending on **x** variable. First program doesn't use boolean operators *(and, or, not)*, while second - does.
- Lab 2: Algorithms that calculate hardcoded expression that contains nested math operations, like:
  - $\sum_{i=1}^{n} a_i = a_1 + a_2 + \dots + a_n$
  - $\prod_{i=1}^{n} a_i = a_1 \cdot a_2 \cdot \dots \cdot a_n$
  First algorithm uses **Nested Loops** approach, which has $O(n^2)$ time complexity, otherwise second algorithm uses **Dynamic Programing** simple memoization approach that is much more efficient and has $O(log(n))$ time complexity.

# Usage

To compile and run program, move to directory where it's located:
```bash
cd path/to/programs/dir
```

Compile the desired program:
```bash
gcc ./filename.c -o compiled-name # gcc example
```

Run the executable:
```bash
./compiled-name
```
