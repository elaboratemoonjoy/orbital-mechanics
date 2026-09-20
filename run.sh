#!/bin/bash
values=(1 5 10 20 50 100 200 500 1000)

for i in "${values[@]}"; do
    python -m orbits.newtonian_leapfrog "$i" &
    python -m orbits.newtonian_copy "$i" &
done

wait