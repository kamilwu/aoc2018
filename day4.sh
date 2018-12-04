#!/bin/bash

declare -A total_asleep
minutes=()

guard_id=-1
from=-1
to=-1

sorted=$(sort data/4.txt)
while read -r line; do
    tm=$(echo $line | egrep "..:.." -o)
    if [[ $line =~ 'begins shift' ]]; then
        guard_id=$(echo $line | egrep "#[0-9]+" -o)
    fi;

    if [[ $line =~ 'falls asleep' ]]; then
        from=10#${tm[@]:3}
    fi;

    if [[ $line =~ 'wakes up' ]]; then
        to=10#${tm[@]:3}
        let to=$to-1
        let asleep=$to-$from
        let sum=${total_asleep[$guard_id]}+$asleep
        total_asleep[$guard_id]=$sum
    fi
done < <(printf '%s' "$sorted")

# find guard that has the most minutes asleep
max=-1
guard_id_with_max=-1
for key in ${!total_asleep[@]}; do
    if [[ "${total_asleep[$key]}" -gt "$max" ]]; then
        max=${total_asleep[$key]}
        guard_id_with_max=$key
    fi
done

echo $guard_id_with_max
