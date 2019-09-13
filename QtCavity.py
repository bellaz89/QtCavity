#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from simulate import simulate

import numpy as np


class QtCavity(QtWidgets.QMainWindow):
    '''
        Main application class
    '''
    def __init__(self):
        '''
            Constructor
        '''
        super(QtCavity, self).__init__()
        
        cwidget = QtWidgets.QWidget(self)
        self.ui = uic.loadUi("QtCavity.ui", cwidget)
        ui = self.ui
        self.setCentralWidget(cwidget)
        self.show() 

        ui.fill_time.editingFinished.connect(self.basic_value_changed)
        ui.flat_time.editingFinished.connect(self.basic_value_changed)
        ui.decay_time.editingFinished.connect(self.basic_value_changed)
        ui.roq.editingFinished.connect(self.basic_value_changed)
        ui.length.editingFinished.connect(self.basic_value_changed)
        ui.qext.editingFinished.connect(self.basic_value_changed)
        ui.q0.editingFinished.connect(self.basic_value_changed)
        ui.frequency.editingFinished.connect(self.basic_value_changed)
        ui.detuning.editingFinished.connect(self.basic_value_changed)
        ui.fill_power.editingFinished.connect(self.basic_value_changed)
        ui.flat_power.editingFinished.connect(self.basic_value_changed)
        ui.line_impedance.editingFinished.connect(self.basic_value_changed)
        ui.fill_time.editingFinished.connect(self.basic_value_changed)
        ui.flat_time.editingFinished.connect(self.basic_value_changed)
        ui.decay_time.editingFinished.connect(self.basic_value_changed)

        ui.ql.editingFinished.connect(self.ql_value_changed)
        ui.bandwidth.editingFinished.connect(self.bandwidth_value_changed)
        ui.beta.editingFinished.connect(self.beta_value_changed)
        ui.decay_tau.editingFinished.connect(self.decay_tau_value_changed)
        ui.detuning_angle.editingFinished.connect(self.detuning_angle_value_changed)
        ui.fill_voltage.editingFinished.connect(self.fill_voltage_value_changed)
        ui.flat_voltage.editingFinished.connect(self.flat_voltage_value_changed)
        ui.turn_ratio.editingFinished.connect(self.turn_ratio_value_changed)
        ui.fill_gradient.editingFinished.connect(self.fill_gradient_value_changed)
        ui.flat_gradient.editingFinished.connect(self.flat_gradient_value_changed)

        ui.load.clicked.connect(self.on_load_button)
        ui.save.clicked.connect(self.on_save_button)
        ui.save_data.clicked.connect(self.on_save_data_button)
        ui.simulate.clicked.connect(self.on_simulate_button)

        ui.fill_time.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.flat_time.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.decay_time.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.roq.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.length.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.qext.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.q0.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.frequency.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.detuning.setValidator(QDoubleValidator(-1e15, 1e15, 4))
        ui.fill_power.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.flat_power.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.line_impedance.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.fill_time.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.flat_time.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.decay_time.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.ql.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.bandwidth.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.beta.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.decay_tau.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.detuning_angle.setValidator(QDoubleValidator(-179.99, 179.99, 4))
        ui.fill_voltage.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.flat_voltage.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.turn_ratio.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.fill_gradient.setValidator(QDoubleValidator(0, 1e15, 4))
        ui.flat_gradient.setValidator(QDoubleValidator(0, 1e15, 4))

        self.gradient_figure = Figure()
        self.gradient_canvas = FigureCanvas(self.gradient_figure)
        self.gradient_toolbar = NavigationToolbar(self.gradient_canvas, self)
        self.ui.gradient_layout.addWidget(self.gradient_canvas)
        self.ui.gradient_layout.addStretch(1)
        self.ui.gradient_layout.addWidget(self.gradient_toolbar)

        self.energy_figure = Figure()
        self.energy_canvas = FigureCanvas(self.energy_figure)
        self.energy_toolbar = NavigationToolbar(self.energy_canvas, self)
        self.ui.energy_layout.addWidget(self.energy_canvas)
        self.ui.energy_layout.addStretch(1)
        self.ui.energy_layout.addWidget(self.energy_toolbar)
    
        self.phase_figure = Figure()
        self.phase_canvas = FigureCanvas(self.phase_figure)
        self.phase_toolbar = NavigationToolbar(self.phase_canvas, self)
        self.ui.phase_layout.addWidget(self.phase_canvas)
        self.ui.phase_layout.addStretch(1)
        self.ui.phase_layout.addWidget(self.phase_toolbar)
        
        self.energy_ax = self.energy_figure.add_subplot(111)
        self.gradient_ax = self.gradient_figure.add_subplot(111)
        self.phase_ax = self.phase_figure.add_subplot(111)

        self.fill_time = 0.001
        self.fill_time = 0.001
        self.fill_time = 0.001
        self.flat_time = 0.001
        self.decay_time = 0.001
        self.roq = 1024
        self.length = 1
        self.qext = 5e6
        self.q0 = 1e10
        self.frequency = 1.3e9
        self.detuning = 0
        self.fill_power = 1000 
        self.flat_power = 1000 
        self.line_impedance = 1000 
        
        self.recompute_params()
        self.on_simulate_button()

    def on_load_button(self):
        fname = QFileDialog.getOpenFileName(self, 'Save file', os.getcwd(), "TOML (*.toml)")

    def on_save_button(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(), "TOML (*.toml)")

    def on_save_data_button(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(), "CSV (*.csv)")

    def on_simulate_button(self):
        simulate(self)
        self.redraw()

    def recompute_params(self):
        '''
            recompute params
        '''
        try:
            self.ql = 1/((1/self.qext)+(1/self.q0))
            self.beta = self.q0/self.qext
            self.bandwidth = self.frequency/self.ql
            self.decay_tau = 1/(2*np.pi * self.bandwidth)
            self.y = self.detuning*2/self.bandwidth
            self.detuning_angle = -np.arctan(self.y)*180/np.pi
            self.fill_voltage = np.sqrt(2*self.fill_power*self.line_impedance)
            self.flat_voltage = np.sqrt(2*self.flat_power*self.line_impedance)
            self.turn_ratio = np.sqrt(self.roq*self.qext/self.line_impedance)
            self.fill_gradient = (np.sqrt(2*self.roq*
                                         self.ql*self.fill_power)/self.length*
                                         self.gradient_fraction())
            self.flat_gradient = (np.sqrt(2*self.roq*
                                         self.ql*self.flat_power)/self.length*
                                         self.gradient_fraction())


            ui = self.ui
            self.blockSignals(True)

            ui.ql.setText('{:.4E}'.format(self.ql))
            ui.bandwidth.setText('{:.4E}'.format(self.bandwidth))
            ui.beta.setText('{:.4E}'.format(self.beta))
            ui.decay_tau.setText('{:.4E}'.format(self.decay_tau))
            ui.detuning_angle.setText('{:.4}'.format(self.detuning_angle))
            ui.fill_voltage.setText('{:.4E}'.format(self.fill_voltage))
            ui.flat_voltage.setText('{:.4E}'.format(self.flat_voltage))
            ui.turn_ratio.setText('{:.4E}'.format(self.turn_ratio))
            ui.fill_gradient.setText('{:.4E}'.format(self.fill_gradient))
            ui.flat_gradient.setText('{:.4E}'.format(self.flat_gradient))
            ui.fill_time.setText('{:.4E}'.format(self.fill_time))
            ui.flat_time.setText('{:.4E}'.format(self.flat_time))
            ui.decay_time.setText('{:.4E}'.format(self.decay_time))
            ui.roq.setText('{:.4E}'.format(self.roq))
            ui.length.setText('{:.4E}'.format(self.length))
            ui.qext.setText('{:.4E}'.format(self.qext))
            ui.q0.setText('{:.4E}'.format(self.q0))
            ui.frequency.setText('{:.4E}'.format(self.frequency))
            ui.detuning.setText('{:.4E}'.format(self.detuning))
            ui.fill_power.setText('{:.4E}'.format(self.fill_power))
            ui.flat_power.setText('{:.4E}'.format(self.flat_power))
            ui.line_impedance.setText('{:.4E}'.format(self.line_impedance))

            self.blockSignals(False)

        except ZeroDivisionError:
            pass

    def redraw(self):
        energy_ax = self.energy_ax
        gradient_ax = self.gradient_ax
        phase_ax = self.phase_ax
        
        energy_ax.clear()
        gradient_ax.clear()
        phase_ax.clear()
        
        self.energy_canvas.draw()
        self.gradient_canvas.draw()
        self.phase_canvas.draw()

        energy_ax.plot(self.time_trace, self.fwd_power_trace, 
                       label='Forward power')
        gradient_ax.plot(self.time_trace, self.fwd_voltage_trace, 
                         label='Forward voltage')
        phase_ax.plot(self.time_trace, self.fwd_phase_trace, 
                      label='Forward phase')
        
        energy_ax.set_xlabel('Time [s]')
        gradient_ax.set_xlabel('Time [s]')
        phase_ax.set_xlabel('Time [s]')

        energy_ax.legend()
        gradient_ax.legend()
        phase_ax.legend()

        self.energy_canvas.draw()
        self.gradient_canvas.draw()
        self.phase_canvas.draw()

    def blockSignals(self, val):
        ui = self.ui

        ui.ql.blockSignals(val)
        ui.bandwidth.blockSignals(val)
        ui.beta.blockSignals(val)
        ui.decay_tau.blockSignals(val)
        ui.detuning_angle.blockSignals(val)
        ui.fill_voltage.blockSignals(val)
        ui.flat_voltage.blockSignals(val)
        ui.turn_ratio.blockSignals(val)
        ui.fill_gradient.blockSignals(val)
        ui.flat_gradient.blockSignals(val)
        ui.fill_time.blockSignals(val)
        ui.flat_time.blockSignals(val)
        ui.decay_time.blockSignals(val)
        ui.roq.blockSignals(val)
        ui.length.blockSignals(val)
        ui.qext.blockSignals(val)
        ui.q0.blockSignals(val)
        ui.frequency.blockSignals(val)
        ui.detuning.blockSignals(val)
        ui.fill_power.blockSignals(val)
        ui.flat_power.blockSignals(val)
        ui.line_impedance.blockSignals(val)

    def gradient_fraction(self):
        return 1/np.sqrt(1 + np.tan(self.detuning_angle*np.pi/180)**2)

    def basic_value_changed(self):
        '''
            Called when a basic value changes
        '''
        ui = self.ui
        
        self.fill_time = float(ui.fill_time.text())
        self.flat_time = float(ui.flat_time.text())
        self.decay_time = float(ui.decay_time.text())
        self.roq = float(ui.roq.text())
        self.length = float(ui.length.text())
        self.qext = float(ui.qext.text())
        self.q0 = float(ui.q0.text())
        self.frequency = float(ui.frequency.text())
        self.detuning = float(ui.detuning.text())
        self.fill_power = float(ui.fill_power.text())
        self.flat_power = float(ui.flat_power.text())
        self.line_impedance =  float(ui.line_impedance.text())
        
        self.recompute_params()

    def ql_value_changed(self, ql=None):
        if ql == None:
            ql = self.ui.ql.text()

        try:
            qext = 1/(1/float(ql) - 1/self.q0)
            if qext > 0:
                self.qext = qext

            self.recompute_params()
        except ZeroDivisionError:
            pass

    def beta_value_changed(self, beta=None):
        if beta == None:
            beta = self.ui.beta.text()

        try:
            self.qext = self.q0/float(beta)
            self.recompute_params()
        except ZeroDivisionError:
            pass

    def bandwidth_value_changed(self, bandwidth=None):
        if bandwidth == None:
            bandwidth = self.ui.bandwidth.text()

        try:
            self.ql_value_changed(self.frequency/float(bandwidth))
        except ZeroDivisionError:
            pass

    def decay_tau_value_changed(self, decay_tau=None):
        if decay_tau == None:
            decay_tau = self.ui.decay_tau.text()

        self.ql_value_changed(2*np.pi*self.frequency*float(decay_tau))
        
    def detuning_angle_value_changed(self, detuning_angle=None):
        if detuning_angle == None:
            detuning_angle = self.ui.detuning_angle.text()

        y = np.tan(-float(detuning_angle)*np.pi/180)
        self.detuning = y*self.bandwidth*0.5
        self.recompute_params()

    def fill_voltage_value_changed(self, fill_voltage=None):
        if fill_voltage == None:
            fill_voltage = self.ui.fill_voltage.text()

        try:
            self.fill_power = float(fill_voltage)**2/self.line_impedance*0.5
            self.recompute_params()
        except ZeroDivisionError:
            pass

    def flat_voltage_value_changed(self, flat_voltage=None):
        if flat_voltage == None:
            flat_voltage = self.ui.flat_voltage.text()

        try:
            self.flat_power = float(flat_voltage)**2/self.line_impedance*0.5
            self.recompute_params()
        except ZeroDivisionError:
            pass

    def turn_ratio_value_changed(self, turn_ratio=None):
        if turn_ratio == None:
            turn_ratio = self.ui.turn_ratio.text()
        
        try:
            self.qext = float(turn_ratio)**2/self.roq*self.line_impedance
            self.recompute_params()
        except ZeroDivisionError:
            pass

    def fill_gradient_value_changed(self, fill_gradient=None):
        if fill_gradient == None:
            fill_gradient = self.ui.fill_gradient.text()

        try:
            self.fill_power = (float(fill_gradient)*self.length)**2/(self.roq*self.ql*
                                                                     self.gradient_fraction())
            self.recompute_params()
        except ZeroDivisionError:
            pass

    def flat_gradient_value_changed(self, flat_gradient=None):
        if flat_gradient == None:
            flat_gradient = self.ui.flat_gradient.text()

        try:
            self.flat_power = (float(flat_gradient)*self.length)**2/(self.roq*self.ql*
                                                                     self.gradient_fraction())
            self.recompute_params()
        except ZeroDivisionError:
            pass

def main():
    '''
        Main method
    '''
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("QtCavity")
    application = QtCavity()
    application.recompute_params()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
