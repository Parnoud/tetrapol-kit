#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Tetrapol demod
# Author: parnoud
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import network
import cmath
import osmosdr
import time
import sip
import threading



class tetrapol_demod(gr.top_block, Qt.QWidget):

    def __init__(self, bit_rate=8000):
        gr.top_block.__init__(self, "Tetrapol demod", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Tetrapol demod")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "tetrapol_demod")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Parameters
        ##################################################
        self.bit_rate = bit_rate

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2000000
        self.var_signal_prob = var_signal_prob = 0
        self.my_freq = my_freq = 0
        self.first_decim = first_decim = int(samp_rate/bit_rate/2)
        self.xlate_offset_fine1 = xlate_offset_fine1 = 0
        self.xlate_offset1 = xlate_offset1 = 0
        self.options_low_pass = options_low_pass = 12500/2
        self.in_samp_rate = in_samp_rate = samp_rate/first_decim
        self.freq = freq = my_freq + var_signal_prob * 0.2
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = (int(freq)+xlate_offset_fine1)
        self.sps = sps = int(in_samp_rate/bit_rate)
        self.ppm_corr = ppm_corr = 0
        self.out_samp_rate = out_samp_rate = 8000
        self.low_pass_filter_taps = low_pass_filter_taps = firdes.low_pass(1.0, samp_rate, options_low_pass, options_low_pass*0.2, window.WIN_BLACKMAN, 6.76)
        self.freq_with_offset = freq_with_offset = freq-xlate_offset1
        self.bw = bw = (9200+100)/2
        self.afc_decimation = afc_decimation = 32000

        ##################################################
        # Blocks
        ##################################################

        self._ppm_corr_range = qtgui.Range(-100, 100, 0.5, 0, 200)
        self._ppm_corr_win = qtgui.RangeWidget(self._ppm_corr_range, self.set_ppm_corr, "ppm", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._ppm_corr_win, 0, 10, 1, 6)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(10, 16):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.afc_probe = blocks.probe_signal_f()
        self._xlate_offset_fine1_range = qtgui.Range(-5e3, +5e3, 1, 0, 200)
        self._xlate_offset_fine1_win = qtgui.RangeWidget(self._xlate_offset_fine1_range, self.set_xlate_offset_fine1, "'xlate_offset_fine1'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._xlate_offset_fine1_win, 0, 4, 1, 6)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 10):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if lambda x: f'{x/1000000:.4f} MHz':
            self._variable_qtgui_label_0_formatter = lambda x: f'{x/1000000:.4f} MHz'
        else:
            self._variable_qtgui_label_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("Receive frequency: "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_layout.addWidget(self._variable_qtgui_label_0_tool_bar)
        def _var_signal_prob_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.afc_probe.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_var_signal_prob,val))
              except AttributeError:
                self.set_var_signal_prob(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (2))
        _var_signal_prob_thread = threading.Thread(target=_var_signal_prob_probe)
        _var_signal_prob_thread.daemon = True
        _var_signal_prob_thread.start()
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            in_samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 1, 12, 1, 6)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(12, 18):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "BASE", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(True)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_1_win, 1, 0, 1, 6)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            in_samp_rate, #bw
            "IN", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.01)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), (-30))
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 6, 1, 6)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 12):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq((freq-xlate_offset1), 0)
        self.osmosdr_source_0.set_freq_corr(ppm_corr, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(38, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_char, 1, '127.0.0.1', 42000, 0, 8, False)
        self._my_freq_tool_bar = Qt.QToolBar(self)
        self._my_freq_tool_bar.addWidget(Qt.QLabel("Frequency" + ": "))
        self._my_freq_line_edit = Qt.QLineEdit(str(self.my_freq))
        self._my_freq_tool_bar.addWidget(self._my_freq_line_edit)
        self._my_freq_line_edit.editingFinished.connect(
            lambda: self.set_my_freq(eng_notation.str_to_num(str(self._my_freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._my_freq_tool_bar, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(first_decim, low_pass_filter_taps, 0, samp_rate)
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=sps,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,log=False)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(32000, 1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rate/first_decim/(2*math.pi*afc_decimation)))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.afc_probe, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_freq_sink_x_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "tetrapol_demod")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate
        self.set_first_decim(int(self.samp_rate/self.bit_rate/2))
        self.set_sps(int(self.in_samp_rate/self.bit_rate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_first_decim(int(self.samp_rate/self.bit_rate/2))
        self.set_in_samp_rate(self.samp_rate/self.first_decim)
        self.set_low_pass_filter_taps(firdes.low_pass(1.0, self.samp_rate, self.options_low_pass, self.options_low_pass*0.2, window.WIN_BLACKMAN, 6.76))
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/self.first_decim/(2*math.pi*self.afc_decimation)))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)

    def get_var_signal_prob(self):
        return self.var_signal_prob

    def set_var_signal_prob(self, var_signal_prob):
        self.var_signal_prob = var_signal_prob
        self.set_freq(self.my_freq + self.var_signal_prob * 0.2)

    def get_my_freq(self):
        return self.my_freq

    def set_my_freq(self, my_freq):
        self.my_freq = my_freq
        self.set_freq(self.my_freq + self.var_signal_prob * 0.2)
        Qt.QMetaObject.invokeMethod(self._my_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.my_freq)))

    def get_first_decim(self):
        return self.first_decim

    def set_first_decim(self, first_decim):
        self.first_decim = first_decim
        self.set_in_samp_rate(self.samp_rate/self.first_decim)
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/self.first_decim/(2*math.pi*self.afc_decimation)))

    def get_xlate_offset_fine1(self):
        return self.xlate_offset_fine1

    def set_xlate_offset_fine1(self, xlate_offset_fine1):
        self.xlate_offset_fine1 = xlate_offset_fine1
        self.set_variable_qtgui_label_0((int(self.freq)+self.xlate_offset_fine1))

    def get_xlate_offset1(self):
        return self.xlate_offset1

    def set_xlate_offset1(self, xlate_offset1):
        self.xlate_offset1 = xlate_offset1
        self.set_freq_with_offset(self.freq-self.xlate_offset1)
        self.osmosdr_source_0.set_center_freq((self.freq-self.xlate_offset1), 0)

    def get_options_low_pass(self):
        return self.options_low_pass

    def set_options_low_pass(self, options_low_pass):
        self.options_low_pass = options_low_pass
        self.set_low_pass_filter_taps(firdes.low_pass(1.0, self.samp_rate, self.options_low_pass, self.options_low_pass*0.2, window.WIN_BLACKMAN, 6.76))

    def get_in_samp_rate(self):
        return self.in_samp_rate

    def set_in_samp_rate(self, in_samp_rate):
        self.in_samp_rate = in_samp_rate
        self.set_sps(int(self.in_samp_rate/self.bit_rate))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.in_samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.in_samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_with_offset(self.freq-self.xlate_offset1)
        self.set_variable_qtgui_label_0((int(self.freq)+self.xlate_offset_fine1))
        self.osmosdr_source_0.set_center_freq((self.freq-self.xlate_offset1), 0)

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0))))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_ppm_corr(self):
        return self.ppm_corr

    def set_ppm_corr(self, ppm_corr):
        self.ppm_corr = ppm_corr
        self.osmosdr_source_0.set_freq_corr(self.ppm_corr, 0)

    def get_out_samp_rate(self):
        return self.out_samp_rate

    def set_out_samp_rate(self, out_samp_rate):
        self.out_samp_rate = out_samp_rate

    def get_low_pass_filter_taps(self):
        return self.low_pass_filter_taps

    def set_low_pass_filter_taps(self, low_pass_filter_taps):
        self.low_pass_filter_taps = low_pass_filter_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.low_pass_filter_taps)

    def get_freq_with_offset(self):
        return self.freq_with_offset

    def set_freq_with_offset(self, freq_with_offset):
        self.freq_with_offset = freq_with_offset

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw

    def get_afc_decimation(self):
        return self.afc_decimation

    def set_afc_decimation(self, afc_decimation):
        self.afc_decimation = afc_decimation
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/self.first_decim/(2*math.pi*self.afc_decimation)))



def argument_parser():
    parser = ArgumentParser()
    return parser


def main(top_block_cls=tetrapol_demod, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
