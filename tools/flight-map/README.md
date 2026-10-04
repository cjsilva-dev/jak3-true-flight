# Flight ground map tools

`goal_src/jak3/engine/target/flight-map.gc` is generated. It records which level owns the ground of
every 16 m cell of the areas the flight streamer manages, and how high that ground is. The streamer
(`flight-stream.gc`) looks levels up there instead of guessing them.

Files here:

- `fs-mapscan.gc`: dev-only GOAL file. Loaded into a debug boot of the game through the REPL, it
  casts four rays per cell against one level's collision and prints the result to the game log.
- `mapscan.sh`: runs the scan for a list of levels (teleports to each, or loads it by name).
- `boot-debug.sh`: debug-boots the game with a goalc REPL in tmux.
- `scan-jak3.txt`: the raw scan this repo's map was generated from.
- `mapgen.py`: turns a scan into `flight-map.gc`.

Regenerate the map from the stored scan:

```
python3 tools/flight-map/mapgen.py jak3 tools/flight-map/scan-jak3.txt goal_src/jak3 --skip waspala
```

To add an area, scan its levels (append to the scan file) and regenerate. A level that is not in the
map is left to the game's own load triggers.
