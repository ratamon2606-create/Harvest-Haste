# Harvest & Haste

## Project Description

- **Project by:** _(your name)_
- **Game Genre:** Farming Simulator, Cooking Minigame

Harvest & Haste is a cozy farming + cooking game where you grow crops, raise cows, fish in a pond, and then race to cook dishes under a ticking timer across five increasingly difficult recipes. The game quietly logs everything you do and, when you're done, pops open a dashboard with six charts showing exactly how your session played out from average level times to a heatmap of every single click.

---

## Installation

To clone this project:
```sh
git clone https://github.com/<username>/Harvest-Haste.git
cd Harvest-Haste
```

To create and run the Python environment for this project:

**Windows:**
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Mac / Linux:**
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running Guide

After activating the Python environment, run the game:

**Windows:**
```bat
python "Harvest&Haste.py"
```

**Mac / Linux:**
```sh
python3 "Harvest&Haste.py"
```

The `asset/` folder must be in the same directory as the game script. It contains all the sprites, fonts, and audio.

> The filename contains an `&` symbol, so wrap it in quotes when running from the terminal (as shown above).

---

## Tutorial / Usage

1. **Start Menu** Click anywhere on the title screen to jump in.
2. **Overworld (Farm)** You start with a little money and an empty inventory. Use the mouse to poke around:
   - **Shop** (top-left building) buy seeds, crops, cows, and fish.
   - **Fields** click an empty field with a seed in your inventory to plant, then click the field again once it's ready to harvest.
   - **Cow Pen** drop a cow in, watch it wander, and click it once it's ready to turn it into beef.
   - **Pond** click to fish (there's a timer, so be patient).
   - **Kitchen** (the house) walk in to start the current cooking level.
3. **Cooking Minigame** Each level is a recipe made of multiple steps (slice, boil, grill). Follow the on-screen prompts and use the mouse before the overall timer runs out.
4. **End of Level** A SUCCESS screen shows your reward; a FAIL screen shows which ingredients you lost. Click the return button to head back to the farm.
5. **Dashboard** When you close the game window, the post-session analytics dashboard opens automatically with six charts summarizing your play.

### Controls

| Action | Input |
|---|---|
| Interact with anything | Left Mouse Click |
| Drag / swipe in minigame | Hold and drag Left Mouse |
| Return from SUCCESS / FAIL | Click the return button |
| Close game / open dashboard | Window close button |

---

## Game Features

- **Full farm economy:** shop, 2 crop types (rice, cabbage), a cow pen with wandering cows, and a fishing pond.
- **Five cooking levels**, each with a different recipe and a tighter time budget than the last.
- **Three cooking station types:** Cutting Board (slicing), Pot (boiling), Pan (grilling, don't let it burn!).
- **Composable recipe system:** each recipe is just a list of step objects, so new levels are easy to add.
- **Automatic event logging:** every purchase, harvest, click, interaction, and result gets written to CSV.
- **Dual CSV output:** one per-session file powers the dashboard, one cumulative file keeps long-term history.
- **Post-session analytics dashboard** with 6 charts: table, line graph, pie chart, 2D histogram, bar chart, and box plot.
- **Resizable window** that keeps the aspect ratio nice and tidy.

---

## Known Bugs

- On very slow machines, the boiling / grilling timers can drift a tiny bit because they run on real-time deltas rather than fixed frames.

---

## Unfinished Works

All planned features were completed. All 5 cooking levels, the full farm economy, both CSV logs, and all 6 dashboard visualizations are working in the final build.

---

## External Sources

Acknowledgements:
1. Pygame [pygame.org](https://www.pygame.org) game engine
2. Matplotlib [matplotlib.org](https://matplotlib.org) data visualizations
3. Pandas [pandas.pydata.org](https://pandas.pydata.org) CSV parsing and aggregation
4. Dudu Calligraphy [dafont.com] (https://www.dafont.com/dudu-calligraphy.font) Adderou. main font used
5. 