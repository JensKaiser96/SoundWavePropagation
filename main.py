from src.numerics import Simulation
from src.physics import Space
from src.visuals import Window


def main():
    room = Space(300)
    sim = Simulation(room)
    win = Window(room, 2, 25)

    sim.data[0, 100, 100] = 120
    while True:
        if win.draw_now():
            sim.update()
            win.update(sim.data[0])


if __name__ == '__main__':
    main()
