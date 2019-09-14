import numpy as np
import toml


def save_data(fname, gui):
    '''
        save simulated data to fname
    '''
   
    if not fname.endswith('.csv'):
        fname = fname + '.csv'
    
    header = 'Time[s], Cavity gradient[V/m], Cavity energy[J], Cavity phase[deg],' \
              'Forward voltage[V], Forward power[W], Forward phase[deg]' \
              'Reflected voltage[V], Reflected power[W], Reflected phase[deg]'
    
    data = np.array([
                    gui.time_trace,
                    gui.cavity_gradient_trace,
                    gui.cavity_energy_trace,
                    gui.cavity_phase_trace,
                    gui.refl_power_trace,
                    gui.refl_voltage_trace,
                    gui.refl_phase_trace,
                    gui.fwd_power_trace,
                    gui.fwd_voltage_trace,
                    gui.fwd_phase_trace]).transpose()

    np.savetxt(fname, data, fmt='%.4E', delimiter=',', header=header)
