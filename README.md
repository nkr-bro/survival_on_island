# Survival on Island

My first 2D game. Your ship crashes and you end up stuck on an island, and the only way out is to build a raft.

## Description

After the shipwreck you wake up on a small island with nothing. You walk around, collect wood and stone, craft a tool and then use it to build a raft. Once the raft is ready, you get on it and sail away.

Crafting recipes:

* Tool: 1 wood + 2 stone
* Raft: tool + 2 wood + 3 stone (you have to build it next to the sign)

There's a main menu with Play, How to play and Exit, so you can check the rules before starting.

I made the game with Python and Pygame. The map was made in Tiled, and I drew all the pixel art myself in Piskel, including the main character and his walking animation.

### Screenshots

<img width="1470" height="956" alt="Снимок экрана — 2026-11-22 в 18 45 14" src="https://github.com/user-attachments/assets/23d24e6f-0bd7-4b29-966e-48a9c3c4e2a9" />


## Getting Started

### Dependencies

* Python 3.9 or newer (I used Python 3.15)
* pygame-ce
* PyTMX
* Tested on macOS

### Installing

* Download the project: click the green **Code** button on GitHub and choose **Download ZIP**, or clone it:
```
git clone https://github.com/nkr-bro/survival_on_island.git
cd survival_on_island
```
* Install the libraries:
```
pip install -r requirements.txt
```

### Executing program

* Run the game:
```
python main.py
```
* Controls:
  * WASD - move
  * E - collect wood or stone
  * C - craft a tool
  * F - build a raft at the sign
  * Space - get on the raft
  * Esc - quit

## Help

The game opens in fullscreen. If you want to close it, press Esc.

If you get an error like `No module named pygame` or `No module named pytmx`, the libraries are not installed yet:
```
pip install -r requirements.txt
```
On macOS you may need to use `python3` and `pip3` instead of `python` and `pip`.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
