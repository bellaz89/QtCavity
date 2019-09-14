'''
    simulation module
'''
import numpy as np
from scipy.integrate import solve_ivp

def simulate(gui):

    qext = gui.qext
    ql = gui.qext
    turn_ratio = gui.turn_ratio
    hbw = np.pi * gui.bandwidth
    frequency = gui.frequency
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
    drive_trace = np.sqrt(2*roq*(ql**2) /
                          (qext*line_impedance))*fwd_voltage_trace

    def simulation_function(t, iq):
        diq = [0, 0]
        diq[0] = -hbw*(iq[0] + y*iq[1]) + hbw*np.interp(t, time_trace,
                                                        drive_trace)
        diq[1] = -hbw*(-y*iq[0] + iq[1])
        return diq
    
    sol = solve_ivp(simulation_function, [0, total_time], 
                    [0, 0], t_eval=time_trace)

    cavity_gradient_trace = np.sqrt(sol.y[0]**2 + sol.y[1]**2)/length
    cavity_phase_trace = 180/np.pi*np.arctan2(sol.y[0], sol.y[1])
    cavity_energy_trace = (cavity_gradient_trace*length)**2/(2*np.pi*frequency*roq)

    remapped_cavity_voltage = [sol.y[0]/turn_ratio, sol.y[1]/turn_ratio]
    refl_voltage_trace = np.sqrt((remapped_cavity_voltage[0]-fwd_voltage_trace)**2 +
                                 remapped_cavity_voltage[1]**2)
    refl_phase_trace = 180/np.pi*np.arctan2(remapped_cavity_voltage[0]-fwd_voltage_trace,
                                 remapped_cavity_voltage[1])

    refl_power_trace = refl_voltage_trace**2/(2*line_impedance)
    
    gui.time_trace = time_trace
    gui.cavity_gradient_trace = cavity_gradient_trace
    gui.cavity_energy_trace = cavity_energy_trace
    gui.cavity_phase_trace = cavity_phase_trace
    gui.refl_power_trace = refl_power_trace
    gui.refl_voltage_trace = refl_voltage_trace
    gui.refl_phase_trace = refl_phase_trace
    gui.fwd_power_trace = fwd_power_trace
    gui.fwd_voltage_trace = fwd_voltage_trace
    gui.fwd_phase_trace = fwd_phase_trace
