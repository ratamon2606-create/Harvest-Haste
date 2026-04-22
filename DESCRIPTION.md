# Project Description

## 1. Project Overview

- **Project Name:** Harvest & Haste

- **Brief Description:**
  Harvest & Haste is a cozy little 2D farming-and-cooking game built with Pygame. You start with a few coins and an empty inventory, then work your way up by planting crops, raising cows, fishing, and eventually stepping into the kitchen to cook dishes under a ticking clock. The overworld is all about slow, chill farm management, buying seeds, waiting for rice to grow, catching a fish while a cow wanders around in the background. Then the kitchen flips the mood: recipes are split into timed steps (slicing, boiling, grilling) where one missed click can burn your dinner.

  Every little thing you do, every purchase, every click, every harvest, every burnt steak, gets quietly logged to CSV. When you close the game, an analytics dashboard pops up with six charts showing exactly how your session went: which level tripped you up, where you clicked most often, which ingredients you wasted, and how your farm strategy played out.

- **Problem Statement:**
  Farming games and cooking games usually live in completely separate worlds. One is slow and meditative, the other is fast and chaotic. Harvest & Haste stitches them together: you have to *plan* your farm economy and *perform* under kitchen pressure, and the dashboard afterward tells you which half of the loop needs work. No more guessing why you failed, the data shows you.

- **Target Users:**
  Players who like cozy farming games (Stardew Valley, Harvest Moon) *and* fast-paced cooking games (Overcooked, Cooking Mama), plus anyone curious about seeing their own gameplay turned into charts. A full session runs about 15–30 minutes.

- **Key Features:**
  - A full overworld farm with 2 crop fields (rice, cabbage), a cow pen, a fishing pond, a shop, and a kitchen
  - A living economy. Buying seeds, growing crops, raising cows, catching fish, and stockpiling ingredients for each level
  - Five cooking levels with progressively trickier recipes and tighter time limits
  - Three cooking station types: Cutting Board (slicing), Pot (boiling), Pan (grilling, watch the burn!)
  - Mouse-driven minigame steps: click to chop, drag to stir, flip meat before it's toast
  - Automatic CSV logging of everything that happens, in two files (per-session + cumulative)
  - Post-session analytics dashboard with six charts in a cozy cream-and-terracotta color palette
  - Resizable window that keeps the aspect ratio

- **Screenshots:**
  See the `screenshots/` directory for both gameplay and visualization captures.
  - Gameplay: `screenshots/gameplay/`
  - Data Dashboard: `screenshots/visualization/`

- **Proposal:**
  The original project proposal is in this repo: [Proposal.pdf](./Proposal.pdf)

- **YouTube Presentation:**
  Watch the ~7 minute project demo here: [YouTube Link](https://youtu.be/YOUR_VIDEO_ID)

  The video walks through (1) a quick tour of the farm, the kitchen, and the dashboard, (2) how the classes are designed and how they talk to each other, and (3) what each chart in the dashboard actually tells you.

---

## 2. Concept

### 2.1 Background

- **Why this project exists:** I wanted to make something that felt *slow* when you were on the farm and *panicked* the moment you stepped into the kitchen and then, once the dust settled, I wanted the game to hand you a neat little report card of what just happened. Most games don't do that last part, and I think they should.

- **What inspired it:** Stardew Valley's chill farm loop mashed up with the kitchen chaos of Overcooked. The goal was to capture that whole "farm to table" arc in a single project. Small enough to finish, but deep enough to actually feel like a game.

- **Importance/Highlight:** Cooking minigames usually feel like black boxes. You either win or you lose, and you don't really know why. By logging click positions, ingredient waste, level times, and every overworld interaction, Harvest & Haste turns each session into a feedback loop. You can look at your own heatmap and realize "oh, I kept clicking the wrong side of the pan." That's the fun part.

### 2.2 Objectives

- Build a complete farm economy with multiple income sources (crops, fish, livestock).
- Design a modular cooking minigame system where each step (slice / boil / grill) is its own class, so new recipes can be built by just listing the steps in order.
- Ship five progressive cooking levels that ask for increasingly varied ingredients and tighter timing.
- Log every gameplay event to CSV automatically, with no popups or "did you want to save this" prompts.
- Maintain both a per-session file (for the dashboard) and a cumulative file (for anyone who wants to dig into long-term history later).
- Present the session's data in six distinct visualizations that each answer a different question.

---

## 3. UML Class Diagram

The UML class diagram shows all classes, their key attributes and methods, and their relationships (inheritance and association).

**Submission Requirement:**
- The UML Class Diagram is attached as a separate file: [UML.pdf](./UML.pdf)

---

## 4. Object-Oriented Programming Implementation

Here's every class in the project and what it's responsible for:

- **FarmEntity (Base Class):** The abstract parent for anything that lives on the farm and produces something over time. Holds the shared `growthState`, `timeToProduce`, and `isReady` attributes, plus the `updateState()` / `interactToHarvest()` interface subclasses override.

- **Crop (inherits FarmEntity):** A plantable tile (rice or cabbage). Tracks water level, its own state machine (EMPTY → SEEDED → READY), and the time it was planted. Handles seeding, growth, and harvesting logic.

- **Animal (inherits FarmEntity):** A cow. Wanders around inside its pen using a little state machine (PAUSED ↔ MOVING), tracks hunger, and can be turned into beef when it's ready.

- **Ingredient:** A tiny data class that represents a food item with a `currentState` (Raw / Cooked / Burnt). This is the object passed between cooking stations.

- **CookingStation (Base Class):** The abstract parent for all kitchen stations. Holds `isOccupied`, `currentItem`, and `processingTimer`, plus the `placeItem()` / `retrieveItem()` interface.

- **CuttingBoard (inherits CookingStation):** A station for slicing. Exposes a `chop()` method.

- **Stove (inherits CookingStation):** Base class for anything involving heat. Adds an `isBurning` flag and a `boilOrFry()` method.

- **SlicingStep (inherits CuttingBoard):** A concrete minigame step where you swipe a knife a target number of times before the step timer runs out.

- **BoilingStep (inherits Stove):** A concrete minigame step where you add ingredients to a pot in the right order and stir until done.

- **GrillingStep (inherits Stove):** A concrete minigame step where you flip meat on a pan and pull it off before it burns.

- **OrderManager (Base Class):** Abstract parent for anything that manages a recipe order. Holds `activeOrders` and a `timeLimit`.

- **MinigameManager (inherits OrderManager):** Runs a full cooking level. Owns the ordered list of step objects, drives their updates, watches for success/failure, manages the overall timer, and handles the SUCCESS / FAIL / DISH_REVEAL screens.

- **DataTracker:** The logger. Exposes a single `log()` method that records events as rows (Timestamp, EventType, Level, Item, Value1, Value2) and flushes them to two CSV files: one per-session, one cumulative.

- **Game:** The top-level controller. Owns the window, the game state, the inventory, the money, the fields, the cows, the active minigame, and the DataTracker. Runs the main loop, handles scene switching (START_MENU / OVERWORLD / MINIGAME / DASHBOARD), routes input, and launches the analytics dashboard at the end.

---

## 5. Statistical Data

### 5.1 Data Recording Method

All gameplay data is captured by the `DataTracker` class. It exposes a single method `log(event_type, level, item, val1, val2)` that the `Game` and minigame classes call whenever something noteworthy happens. Each log entry gets a timestamp, an event type, a level number, and up to two value fields whose meaning depends on the event.

The events being logged include:
- **Shop_Purchase** — when you buy something (item, quantity, price)
- **Harvest** — when you pick a crop or catch a fish (item, field)
- **Click_Position** — every click during a cooking minigame (x, y)
- **Interaction** — every overworld click on an entity (target, result)
- **Waste_Event** — when an ingredient gets wasted (burnt steak, over-chopped cabbage, etc.)
- **Level_Result** — when a cooking level ends (completion time, SUCCESS or FAIL)

The tracker keeps **two CSV files** going at the same time:
- `current_session_stats.csv` wiped at the start of each new session; drives the in-game dashboard.
- `all_gameplay_stats.csv` appended to forever; good for long-term data across multiple playthroughs.

Splitting the two files keeps the dashboard focused on the current run while still preserving everything for later analysis.

### 5.2 Data Features

The logged data feeds six separate analyses in the dashboard:

- **Level Success Times (Stats Table)** — mean, median, min, and max of successful completion times.
- **Average Time to Complete Level (Line Graph)** — average successful completion time per level (1–5), visualizing the difficulty curve.
- **Ingredient Waste Ratio (Pie Chart)** — share of waste events by ingredient (cabbage, beef, fish, rice).
- **Click Distribution (2D Histogram)** — heatmap of every minigame click across the 1024×720 kitchen.
- **Crop Harvest Yields (Bar Chart)** — total harvest event count per ingredient.
- **Interaction Frequency Spread (Box Plot)** — distribution of interaction counts per overworld target across levels.

---

## 6. Changed Proposed Features (Optional)

- **What was changed:** The player character was taken out of the game and replaced with point-and-click mechanism.
- **Why the change was made:** The game will be easier and more enjoyable for player.

---

## 7. External Sources

Acknowledgements:
1. Pygame [pygame.org](https://www.pygame.org) game engine
2. Matplotlib [matplotlib.org](https://matplotlib.org) data visualizations
3. Pandas [pandas.pydata.org](https://pandas.pydata.org) CSV parsing and aggregation
4. Dudu Calligraphy [dafont.com] (https://www.dafont.com/dudu-calligraphy.font) Adderou. main UI font
5. success 1 [pixabay.com] (https://pixabay.com/sound-effects/film-special-effects-success-1-6297/) Leszek_Szary. success sound effect
6. fail [pixabay.com] (https://pixabay.com/sound-effects/film-special-effects-fail-234710/) u_8g40a9z0la. fail sound effect
7. Slow Cinematic Clock Ticking [pixabay.com] (https://pixabay.com/sound-effects/film-special-effects-slow-cinematic-clock-ticking-405471/) DRAGON-STUDIO. ticking sound effect in kitchen
8. Cat Bag [pixabay.com] (https://pixabay.com/th/music/%e0%b9%80%e0%b8%9e%e0%b8%a5%e0%b8%87%e0%b9%80%e0%b8%94%e0%b8%81%e0%b8%a1%e0%b8%84%e0%b8%a7%e0%b8%b2%e0%b8%a1%e0%b8%aa%e0%b8%82-cat-bag-382798/) ChillRightsMusic. background music for starting page
9. Playful Mood [chosic.com] (https://www.chosic.com/download-audio/59085/) MaxkoMusic. background music for farming