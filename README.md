# True Flight — Jak 3

**Light Jak really flies.** An [OpenGOAL](https://opengoal.dev) mod for *Jak 3* that turns Light Jak's
short glide into full flight: stacking wing flaps, a momentum glide, a turbo, and a superhero landing
that sets off a Dark Bomb blast.

## Controls (as Light Jak)

| Input | Action |
|---|---|
| **X** in the air | Flap. Every flap stacks more height; **hold X** through a flap for extra lift |
| **Hold L1** | Glide. Diving turns into forward speed, and the momentum carries |
| **X while gliding** | Big launch upward (Jak lifts his nose into it) |
| **R1** | Turbo — while flapping, or on top of a glide |
| **Square** in the air | Superhero landing: an accelerating dive (hold Square to dive harder) ending in a Dark Bomb blast that scales with the drop. No fall damage from any height |

The camera follows Jak's height while flying and rises for a better view while gliding.

### In Haven City

Haven only keeps a couple of districts loaded at once, so flight there is tuned to it: each district has
its own ceiling (just above the highest place you can stand), the turbo is capped, and districts are
loaded and shown ahead of you as you fly — including over the walls between them.

## Options

At the top of the options block in `goal_src/jak3/engine/target/target-lightjak.gc` (off by default):

- `*tf-opt-all-light-powers?*` — every Light Jak power and endless light eco from any save
- `*tf-opt-unlock-extras?*` — every Secrets-menu item and OpenGOAL PC cheat unlocked

## What this mod changes

- `goal_src/jak3/engine/target/target-lightjak.gc` — the flight, glide, turbo and landing
- `goal_src/jak3/engine/camera/cam-master.gc` — the camera tracks Jak's height while flying
- `goal_src/jak3/engine/level/region.gc` — city district triggers are tested ahead of a flying Jak

## Not included

This mod contains only code. Everything it shows or plays — Light Jak, his wings, sounds, the Dark Bomb
effects — comes from your own copy of *Jak 3*. HD texture packs are not part of it; install your
favourite pack through the OpenGOAL launcher as usual.

## Credits

- Built on the [OG-Mod-Base](https://github.com/OpenGOAL-Mods/OG-Mod-Base) template and the
  [OpenGOAL](https://github.com/open-goal/jak-project) project.
- *Jak 3* © Naughty Dog / Sony Interactive Entertainment. This is a fan project.

OpenGOAL's own readme is kept in [README.opengoal.md](README.opengoal.md).
