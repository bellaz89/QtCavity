#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, uic
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
        #self.ui = Ui_Form()
        self.ui = uic.loadUi("qtcavity.ui", cwidget)
        ui = self.ui
        #self.ui.setupUi(cwidget)
        self.setCentralWidget(cwidget)
        self.show() 
 
        self.fill_time = 100 
        self.flat_time = 100
        self.decay_time = 100
        self.roq = 1024
        self.length = 1
        self.qext = 5e6
        self.q0 = 1e10
        self.frequency = 1300
        self.detuning = 10
        self.fill_power = ui.fill_power.value()
        self.flat_power = ui.flat_power.value()
        self.line_impedance = ui.line_impedance.value()

    def recompute_params(self):
        '''
            recompute params
        '''
        self.ql = 1/((1/self.qext)+(1/self.q0))
        self.beta = self.q0/self.qext
        self.bandwidth = self.frequency/self.ql
        self.decay_tau = 1/(np.pi * self.bandwidth)
        self.y = self.detuning*2/self.bandwidth
        self.detuning_angle = -np.arctan(self.y)*180/np.pi
        self.fill_voltage = np.sqrt(2*self.fill_power*self.line_impedance)
        self.flat_voltage = np.sqrt(2*self.flat_power*self.line_impedance)
        self.turn_ratio = np.sqrt(self.roq*self.qext/self.line_impedance)
        self.fill_gradient = np.sqrt(2*self.roq*
                                    self.ql*self.fill_power)/self.length*1e-6
        self.flat_gradient = np.sqrt(2*self.roq*
                                    self.ql*self.flat_power)/self.length*1e-6

        self.total_time = self.fill_time + self.flat_time + self.decay_time

        ui = self.ui
        ui.ql.setValue(self.ql)
        ui.bandwidth.setValue(self.bandwidth)
        ui.beta.setValue(self.beta)
        ui.decay_tau.setValue(self.decay_tau/1000)
        ui.detuning_angle.setValue(self.detuning_angle)
        ui.fill_voltage.setValue(self.fill_voltage)
        ui.flat_voltage.setValue(self.flat_voltage)
        ui.turn_ratio.setValue(self.turn_ratio)
        ui.fill_gradient.setValue(self.fill_gradient)
        ui.flat_gradient.setValue(self.flat_gradient)
 
        ui.fill_time.setValue(self.fill_time)
        ui.flat_time.setValue(self.flat_time )
        ui.decay_time.setValue(self.decay_time )
        ui.roq.setValue(self.roq )
        ui.length.setValue(self.length )
        ui.qext.setValue(self.qext)
        ui.q0.setValue(self.q0)
        ui.frequency.setValue(self.frequency)
        ui.detuning.setValue(self.detuning)
        ui.fill_power.setValue(self.fill_power)
        ui.flat_power.setValue(self.flat_power)
        ui.line_impedance.setValue(self.line_impedance)


def main():
    '''
        Main method
    '''
    app = QtWidgets.QApplication(sys.argv)
    application = QtCavity()
    application.recompute_params()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
