import numpy as np

from src.numerics import Simulation
from src.physics import Space, Point2D
from src.signals import InputSignal, OutputSignal
from src.visuals import LiveSimulationView


def main():
    room = Space(300)
    in_signal = InputSignal.from_wav(Point2D(150, 100), "data/wav/short.wav")
    out_signal = OutputSignal(Point2D(150, 200))
    obstacles = np.ones(room.dimensions)
    obstacles[50:250, 150] = 0
    sim = Simulation(room, input_signals=[in_signal], output_signals=[out_signal], obstacles=obstacles, open_borders=True)
    win = LiveSimulationView(sim, scale=2, fps=600)
    extra_ticks = 1000
    last_input_tick = 0

    interesting_ticks = [300, 600, 10_000]

    experiment_name = "fancy_demo"
    while True:
        if win.draw_now():
            sim.update()
            win.draw()
            if sim.tick in interesting_ticks:
                win.screenshot(f"data/img/{experiment_name}_{sim.tick}")
            if not last_input_tick and sim.all_inputs_done:
                sim.save_all_output_signals(f"data/out_wav/{experiment_name}")
                last_input_tick = sim.tick
            if last_input_tick and sim.tick > last_input_tick + extra_ticks:
                break


if __name__ == '__main__':
    main()
