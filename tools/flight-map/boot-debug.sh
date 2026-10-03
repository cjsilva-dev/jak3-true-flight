#!/bin/bash
# usage (on the device): boot-debug.sh <jak2|jak3> <mod dir> <iso dir> <steam shortcut id>
# Debug-boots the game with a persistent goalc REPL in tmux (socket goal2/goal3) and loads fs-mapscan.gc.
game=$1; mod=$2; iso=$3; id=$4; sock=goal${game#jak}; port=$([ $game = jak2 ] && echo 8113 || echo 8114)
for p in $(pgrep -x gk); do kill $p; done; sleep 2
touch $mod/.debug
if ! tmux -L $sock has-session -t goal 2>/dev/null; then
  : > /tmp/goalc-$sock.log
  systemd-run --user --unit=goalc-$sock-$(date +%s) --collect -p KillMode=none -p RemainAfterExit=yes tmux -L $sock new-session -d -s goal "cd $mod && ./goalc --game $game --iso-path $iso 2>&1 | tee /tmp/goalc-$sock.log; sleep 36000"
  until [ -s /tmp/goalc-$sock.log ]; do sleep 1; done; sleep 3
  tmux -L $sock send-keys -t goal '(mi)' Enter
  until tr '\r' '\n' < /tmp/goalc-$sock.log | grep -qE 'Successfully built|Build failed|Compilation Error'; do sleep 3; done
else
  tmux -L $sock send-keys -t goal C-c; sleep 1; tmux -L $sock send-keys -t goal "" Enter
fi
export DISPLAY=:0; (steam steam://rungameid/$id >/dev/null 2>&1 &)
for i in $(seq 1 60); do sleep 3; ss -tln | grep -q $port && break; done; sleep 30
tmux -L $sock send-keys -t goal "(lt)" Enter; sleep 5
tmux -L $sock send-keys -t goal "(ml \"goal_src/$game/fs-mapscan.gc\")" Enter; sleep 7
pgrep -x gk >/dev/null && echo "$game up" || echo "$game DEAD"
