'''
    simulation module
'''
import numpy as np

def simulate(gui):

    qext = gui.qext
    hbw = np.pi * gui.bandwidth
    y = gui.y
    fill_power = gui.fill_power
    flat_power = gui.flat_power
    length = gui.length
    fill_time = gui.fill_time
    flat_time = gui.flat_time
    decay_time = gui.decay_time
    total_time = fill_time + flat_time + decay_time
    simulation_points = gui.ui.simulation_points.value()
    roq = gui.roq
    line_impedance = gui.line_impedance

    time_trace = np.linspace(0, total_time, simulation_points)
    
    fill_bins = int(fill_time/total_time*simulation_points)
    flat_bins = int(flat_time/total_time*simulation_points)
    decay_bins = simulation_points - fill_bins - flat_bins

    fwd_power_trace = np.concatenate((np.full(fill_bins, fill_power), 
                                      np.full(flat_bins, flat_power), 
                                      np.zeros(decay_bins)))

    fwd_phase_trace = np.zeros(simulation_points)
    fwd_voltage_trace = np.sqrt(fwd_power_trace*2/line_impedance)


    gui.time_trace = time_trace
    gui.fwd_power_trace = fwd_power_trace
    gui.fwd_voltage_trace = fwd_voltage_trace
    gui.fwd_phase_trace = fwd_phase_trace
