#!/bin/bash
# usage (on the device, game in debug boot with goalc connected and fs-mapscan.gc ml'd):
#   mapscan.sh <jak2|jak3> <mod dir> <out file> level[=continue-name|=@] [level...]   (=@[master]: load by want with its master level first, Jak stays put; goto=<continue>: just teleport)
# Teleports to each level, waits for it to be active, scans it; appends the MS/MR/MSEND lines to <out file>.
game=$1; mod=$2; out=$3; shift 3
sock=goal${game#jak}
log() { ls -t $mod/data/log/jak*.log | head -1; }
send() { tmux -L $sock send-keys -t goal "$1" Enter; }
for arg in "$@"; do
  lv=${arg%%=*}; cn=${arg#*=}
  [ "$lv" = "goto" ] && { send "(ms-go-c \"$cn\")"; sleep 25; echo "went to $cn"; continue; }
  grep -qa "^MSEND $lv " $out 2>/dev/null && { echo "$lv: already scanned"; continue; }
  L=$(log); n=$(wc -l < $L)
  if [ "${cn:0:1}" = "@" ]; then m=${cn:1}; send "(ms-want (quote $lv) $([ -n "$m" ] && echo "(quote $m)" || echo "#f"))"; elif [ "$cn" != "$arg" ]; then send "(ms-go-c \"$cn\")"; else send "(ms-go (quote $lv))"; fi; sleep 3
  if tail -n +$((n+1)) $L | grep -qa "^MG-FAIL"; then echo "$lv: no continue"; continue; fi
  ok=0
  for i in $(seq 1 30); do
    sleep 2; m=$(wc -l < $L); send "(ms-status (quote $lv))"; sleep 1
    tail -n +$((m+1)) $L | grep -qa "^MQ $lv active" && { ok=1; break; }
    pgrep -x gk >/dev/null || { echo "$lv: GAME DIED"; exit 1; }
  done
  [ $ok = 1 ] || { echo "$lv: never active"; continue; }
  sleep 4
  m=$(wc -l < $L); send "(fs-mapscan (quote $lv))"
  for i in $(seq 1 60); do sleep 1; tail -n +$((m+1)) $L | grep -qa "^MSEND $lv\|^MS-FAIL $lv" && break; done
  tail -n +$((m+1)) $L | grep -a "^MS \|^MR \|^MSEND \|^MS-FAIL" >> $out
  echo "$lv: $(tail -n +$((m+1)) $L | grep -a '^MS \|^MSEND \|^MS-FAIL' | tr '\n' ' ')"
done
