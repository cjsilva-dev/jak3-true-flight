# True Flight — Jak 3

**Light Jak really flies — and so does Dark Jak.** An [OpenGOAL](https://opengoal.dev) mod for *Jak 3*
that turns Light Jak's short glide into full flight: stacking wing flaps, a momentum glide, a turbo, a
dash, and a superhero landing. Dark Jak gets his own, meaner version of it.

## Controls (as Light Jak)

| Input | Action |
|---|---|
| **X** in the air | Flap. Every flap stacks more height; **hold X** through a flap for extra lift |
| **Hold L1** | Glide. Diving turns into forward speed, and the momentum carries |
| **X while gliding** | Big launch upward (Jak lifts his nose into it) |
| **Tap R1** | Dash: a quick lunge forward in a trail of glittering light |
| **Hold R1** | Turbo — while flapping, or on top of a glide |
| **Square** in the air | Superhero landing: an accelerating dive (hold Square to dive harder) ending in a burst of light that hits everything around, bigger the higher you fell |

The camera follows Jak's height while flying and rises for a better view while gliding. Shot while
flying, Jak flinches in the air and flies on. There's no fall damage after flying, from any height.

## Dark Jak flies too

As Dark Jak, **double-jump** to take off: Light Jak's wings burst out of him, reshaped into jagged,
spiky, twitching dark wings with Dark Jak's own lightning crackling between the feathers. Their glow
flickers like unstable dark eco and flares on every flap. **R3** while flying switches the wing style:

- **Smoked glass** (the default): dark, see-through wings cut to the jagged shape of the feathers
- **Glow**: Light Jak's see-through glow, in dark-eco purple

The controls are the same, but Dark Jak flies the way he does in Dark Flight (the Jak II mod), with
exactly the same flight:

- fewer, harder flaps that throw him forward, and a heavier fall between them; each flap kicks in the
  moment you press X, and holding X lifts him higher
- **R1** right after a flap is a turbo; holding **L1** glides, sinking faster and cutting sharper turns
  than Light Jak, leaning into it with his chest hunched forward
- **tap R1** for a dash attack: a lunge in a streak of dark energy and lightning that hits whatever he
  flies through
- **Square** is the real Dark Bomb: the wings fold, he dives in the bomb pose and lands in its blast

About a second after he lands, the wings fold away and his dark attacks come back (straight away if
you press an attack). Dark Jak can take off any time you have him — Light Jak's flight power isn't
needed.

### In Haven City

Haven only keeps a couple of districts loaded at once, so flight there is tuned to it: each district has
its own ceiling (just above the highest place you can stand) and the turbo is capped.

The mod knows which district owns the ground under you and along your path, so the one you're heading
into is loaded before you get there, even when you fly over the walls between them at full speed.
Loading itself is faster too, and districts are drawn as soon as they arrive. Jak 3 also does this in Spargus, and stops you at the edge of Spargus where the only thing beyond is the desert (the desert can't be flown into from the air; fly out through the garage). If you
glide off the edge of the world anyway, you're put back where you left solid ground instead of dying.

## Unlimited Light Jak

Jak 3's own *Secrets* menu item **Unlimited Light Jak** is unlocked and switched **on** in any save that
doesn't have it yet, so you can fly as long as you like. Switch it off there if you'd rather manage
light eco (each flap then uses some, as in the original game). It's saved with your game.

## Options

At the top of the options block in `goal_src/jak3/engine/target/target-lightjak.gc` (off by default):

- `*tf-opt-all-light-powers?*` — every Light Jak power and endless light eco from any save
- `*tf-opt-unlock-extras?*` — every Secrets-menu item and OpenGOAL PC cheat unlocked
- `*tf-opt-all-dark-powers?*` — Dark Jak and all his powers, Unlimited Dark Jak and a full dark eco meter from any save
- `*tf-opt-quiet-debug?*` — for development: hides the debug text and cursor in a `-debug` boot

What these unlock is saved (in your save file and PC settings) and stays unlocked if you switch the
option off again. With both off — the default — the mod writes nothing to your save.

## What this mod changes

- `goal_src/jak3/engine/target/target-lightjak.gc` — the flight, glide, turbo, dash, landing and Dark Jak's flight
- `goal_src/jak3/engine/target/flight-core.gc` — the flight both mods share: Dark Jak's flap, glide, turbo, dash and
  posture, and the tuning both games agree on (the same file is in Dark Flight)
- `goal_src/jak3/engine/target/lightjak-wings.gc` — the wings' dark look: jagged shape, colors and flicker, the two styles,
  sparks and lightning (Light Jak's own colors are put back whenever he flies)
- `goal_src/jak3/engine/target/target.gc` — Dark Jak takes off from the double jump
- `goal_src/jak3/engine/target/target-death.gc` — a hit while flying is a flinch in the air
- `goal_src/jak3/engine/common-obs/powerups.gc` — the wings are removed before their animations are unloaded
- `goal_src/jak3/engine/camera/cam-master.gc` — the camera tracks Jak's height while flying
- `goal_src/jak3/engine/level/region.gc` — while flying in the city, district triggers are tested a little ahead of Jak (at most 30 m)
- `goal_src/jak3/engine/target/flight-stream.gc`, `flight-stream-h.gc`, `flight-map.gc` — level streaming while flying: a map of
  which level owns the ground (generated by `tools/flight-map/`), the loader that follows it, and the fall-out-of-the-world rescue
- `goal_src/jak3/engine/level/level.gc`, `level-h.gc`, `engine/load/load-state.gc`, `engine/game/main.gc`, `engine/camera/cam-update.gc` —
  faster level loading, levels drawn as soon as they arrive from the air, and a level that can't load is skipped instead of stopping the game
- `game/graphics/…/loader/*`, `game/graphics/pipelines/opengl.cpp` — **engine change:** the renderer uploads a new level's
  graphics faster and keeps more of them cached
- `game/graphics/opengl_renderer/foreground/Merc2.*`, `shaders/merc2.frag`, `goal_src/jak3/engine/gfx/foreground/foreground.gc`,
  `engine/data/art-h.gc` — **engine change:** a switch the game sets per model to draw it as a see-through surface instead of
  a glow, with its darkest parts cut away (used only for Dark Jak's smoked-glass wings)

## Not included

This mod contains only code. Everything it shows or plays — Light and Dark Jak, the wings, sounds, the
Dark Bomb effects — comes from your own copy of *Jak 3*. HD texture packs are not part of it; install your favourite pack
through the OpenGOAL launcher as usual.

## Credits

- Built on the [OG-Mod-Base](https://github.com/OpenGOAL-Mods/OG-Mod-Base) template and the
  [OpenGOAL](https://github.com/open-goal/jak-project) project.
- *Jak 3* © Naughty Dog / Sony Interactive Entertainment. This is a fan project.

The mod base's own readme (with OpenGOAL setup links) is kept in [README.opengoal.md](README.opengoal.md).
