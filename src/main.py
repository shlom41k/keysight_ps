import sys

from datetime import datetime
from time import sleep
from threading import Thread
from PyQt6 import uic, QtCore, QtGui, QtWidgets

from settings.settings import settings
from power_supply import PowerSupply


class MainWindow(QtWidgets.QMainWindow):

    com: PowerSupply
    auto_cur_update_thread: Thread
    params = ["voltage_min", "voltage_max", "current_min", "current_max", ]
    range_low = ["LOW", "P8V", "P15V", "P25V", "P35V", ]
    range_high = ["HIGH", "P20V", "P30V", "P50V", "P60V", ]
    cur_mult = {"A": 1, "mA": 1e3, "uA": 1e6, }
    cur_update_time = 0.01
    storage_len = 5
    storage_len_max = 5
    dev_name_info_ind = 1

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('gui/PowerSupplyControl_ui.ui', self)

        # set window name
        self.setWindowTitle("Power Supply Control")

        # Storage states radio buttons
        self.store_btn = {
            1: {"store": self.store_btn_1, "voltage": 0.0, "current": 0.0, "range": "", },
            2: {"store": self.store_btn_2, "voltage": 0.0, "current": 0.0, "range": "", },
            3: {"store": self.store_btn_3, "voltage": 0.0, "current": 0.0, "range": "", },
            4: {"store": self.store_btn_4, "voltage": 0.0, "current": 0.0, "range": "", },
            5: {"store": self.store_btn_5, "voltage": 0.0, "current": 0.0, "range": "", },
        }

        # Disabled controls panels
        self.com_group_box.setDisabled(True)
        self.device_ctrl_group_box.setDisabled(True)
        self.auto_check_ch_box.setChecked(False)
        self.auto_check_ch_box.setDisabled(True)
        self.pb_clear_hist.setEnabled(True)
        self.en_dis_output_control(False)

        self.connect_prog_bar.setMinimum(0)
        self.connect_prog_bar.setMaximum(100)

        # Set voltage range
        self.volt_range_low_btn.setChecked(True)
        self.volt_range_high_btn.setChecked(False)

        # get all devices from settings file
        self.devices = list(settings.get("devices").keys())
        # Get all COM-ports
        self.com_ports = PowerSupply.get_com_ports()

        # update groupbox
        self.update_devices_list()
        # select first device
        self.select_device_clicked()

        self.com_group_box.setEnabled(True)

        # update list of COM ports
        self.com_pb_update_clicked()

        self.cur_thread_stop = False

        # Connect events with functions
        # buttons
        self.com_pb_update.clicked.connect(self.com_pb_update_clicked)
        self.com_pb_connect.clicked.connect(self.com_pb_connect_clicked)
        self.com_pb_disconnect.clicked.connect(self.com_pb_disconnect_clicked)
        self.lim_get_btn.clicked.connect(self.get_current_limits)
        self.lim_set_btn.clicked.connect(self.set_limits)
        self.out_volt_onoff_btn.clicked.connect(self.out_volt_onoff_btn_clicked)
        self.oyt_volt_set_btn.clicked.connect(self.oyt_volt_set_btn_clicked)
        self.out_cur_get.clicked.connect(self.out_cur_get_clicked)
        self.pb_clear_hist.clicked.connect(self.clear_history)
        self.dev_beep_btn.clicked.connect(self.say_beep)
        self.dev_version_btn.clicked.connect(self.get_dev_version)
        self.dev_error_btn.clicked.connect(self.get_dev_errors)
        self.dev_hello_btn.clicked.connect(self.say_hello)
        self.dev_disp_clear_btn.clicked.connect(self.dev_clear_display)
        self.state_load_btn.clicked.connect(self.state_load_btn_clicked)
        self.state_save_btn.clicked.connect(self.state_save_btn_clicked)
        # combo boxex
        self.device_combo_box.currentTextChanged.connect(self.select_device_clicked)
        self.com_combo_box_portname.currentTextChanged.connect(self.select_com_port_clicked)
        self.combo_box_cur_mult.currentTextChanged.connect(self.out_cur_get_clicked)
        # radio buttons
        self.volt_range_low_btn.clicked.connect(self.set_voltage_range)
        self.volt_range_high_btn.clicked.connect(self.set_voltage_range)
        # check boxes
        # self.auto_check_ch_box.stateChanged.connect(self.auto_check_ch_box_clicked)
        self.dev_cntrl_ch.stateChanged.connect(self.dev_control_type_changed)

    def disp_info(self, msg_type: str, message: str):
        """Send some info into message field"""
        msg_types = {
            "INFO": "blue",
            "ERROR": "red",
        }
        msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {msg_type}: {message}"

        self.info_lbl.setText(msg)
        self.info_lbl.setStyleSheet(f"color: {msg_types.get(msg_type)}")
        self.hist_list.addItem(msg)
        self.hist_list.scrollToBottom()

    def clear_history(self):
        self.hist_list.clear()

    def update_devices_list(self):
        """Update list of power supply devices"""
        self.device_combo_box.clear()

        self.devices = list(settings.get("devices").keys())
        self.device_combo_box.addItems(self.devices)

    def select_device_clicked(self):

        # Set device info
        device = settings.get("devices").get(self.device_combo_box.currentText())
        self.device_lbl_description.setText(device.get("description"))

        # Set storage depth
        #print(device.get("storage_depth"))
        self.__class__.storage_len = device.get("storage_depth")

        # Set LOW and HIGH ranges parameters
        volt_min, volt_max, cur_min, cur_max = [self.get_voltage_settings("Low", param) for param in self.__class__.params]
        self.volt_range_low_btn.setText(f"Low: {volt_min} - {volt_max} V, {cur_min} - {cur_max} A.")
        volt_min, volt_max, cur_min, cur_max = [self.get_voltage_settings("High", param) for param in self.__class__.params]
        self.volt_range_high_btn.setText(f"High: {volt_min} - {volt_max} V, {cur_min} - {cur_max} A.")

        self.clear_com_settings()
        self.set_com_settings()

    def com_pb_update_clicked(self):
        """Update list of available COM ports"""
        self.com_combo_box_portname.clear()
        self.com_ports = PowerSupply.get_com_ports()

        if self.com_ports:
            self.com_combo_box_portname.addItems(list(self.com_ports.keys()))
            self.com_lbl_portname_2.setText(self.com_ports.get(self.com_combo_box_portname.currentText()))
            self.com_lbl_portname_2.setStyleSheet("color: blue")
            self.com_pb_connect.setEnabled(True)
            self.com_pb_disconnect.setEnabled(True)
            # self.set_com_settings()

        else:
            # self.clear_com_settings()
            self.com_lbl_portname_2.setText("No available COM ports :(")
            self.com_lbl_portname_2.setStyleSheet("color: red")
            self.com_pb_connect.setDisabled(True)
            self.com_pb_disconnect.setDisabled(True)

    def select_com_port_clicked(self):
        # Select COM port
        self.com_lbl_portname_2.setText(self.com_ports.get(self.com_combo_box_portname.currentText()))

    def get_com_settings(self, param: str):
        return settings.get("devices").get(self.device_combo_box.currentText()).get("COM_settings").get(param)

    def clear_com_settings(self):
        self.com_combo_box_baud.clear()
        self.com_combo_box_bytesize.clear()
        self.com_combo_box_stopbits.clear()
        self.com_combo_box_parity.clear()

    def set_com_settings(self):
        self.com_combo_box_baud.addItems(map(str, self.get_com_settings("baudrate")))
        self.com_combo_box_bytesize.addItems(map(str, self.get_com_settings("bytesize")))
        self.com_combo_box_stopbits.addItems(map(str, self.get_com_settings("stop_bits")))
        self.com_combo_box_parity.addItems(map(str, self.get_com_settings("parity")))

    def disable_com_settings(self):
        self.com_pb_update.setDisabled(True)
        self.com_combo_box_portname.setDisabled(True)
        self.com_combo_box_baud.setDisabled(True)
        self.com_combo_box_bytesize.setDisabled(True)
        self.com_combo_box_stopbits.setDisabled(True)
        self.com_combo_box_parity.setDisabled(True)

    def enable_com_settings(self):
        self.com_pb_update.setEnabled(True)
        self.com_combo_box_portname.setEnabled(True)
        self.com_combo_box_baud.setEnabled(True)
        self.com_combo_box_bytesize.setEnabled(True)
        self.com_combo_box_stopbits.setEnabled(True)
        self.com_combo_box_parity.setEnabled(True)

    def com_pb_connect_clicked(self):
        # create connection
        try:
            self.com = PowerSupply(
                port=self.com_combo_box_portname.currentText(),
                baudrate=int(self.com_combo_box_baud.currentText()),
                bytesize=int(self.com_combo_box_bytesize.currentText()),
                stop_bits=int(self.com_combo_box_stopbits.currentText()),
                parity=self.com_combo_box_parity.currentText(),
            )
        except:
            self.disp_info("ERROR", "Can't create serial port")
            return

        # connect
        try:
            self.com.connect()
            self.disp_info("INFO", "COM port connected")
        except:
            self.disp_info("ERROR", "Can't open serial port")
            return

        try:
            dev_id = self.com.get_info()

            if dev_id:
                self.disp_info("INFO", dev_id)
                cur_dev = dev_id.split(",")[self.__class__.dev_name_info_ind]
                print(cur_dev)

                if cur_dev not in self.device_combo_box.currentText():
                    self.disp_info("ERROR", f"It's not a {self.device_combo_box.currentText()}. Choose {cur_dev} device!")
                    self.com.disconnect()
                    return

            else:
                self.disp_info("ERROR", "No answer from device. Is it correct COM port?")
                self.com.disconnect()
                return

        except:
            self.com.disconnect()
            #print("Here")
            self.disp_info("ERROR", "No answer from device :(")
            return

        # reset device
        try:
            self.com.device_reset()
        except:
            self.disp_info("ERROR", "Something goes ne tak :(. Can't reset device. Reconnect.")
            return

        # Enable remote control
        try:
            self.com.set_remote_control()
            self.com.set_display("ON")
        except:
            self.disp_info("ERROR", "Can't set remote control!")

        # read device storage states
        try:
            self.load_storage()
        except:
            self.disp_info("ERROR", "Can't load storage states! Try again")
            return

        # set voltage range (HIGH or LOW)
        try:
            self.set_voltage_range()
        except:
            self.disp_info("ERROR", "Can't set limits values! Reconnect!")
            return

        # get current limits (voltage & current)
        try:
            self.get_current_limits()
        except:
            self.disp_info("ERROR", "Can't read limits values! Reconnect!")
            return

        # Display 'DONE' message
        try:
            self.com.display_text("CONNECTED")
            sleep(0.5)
            self.com.clear_display()

            if self.dev_cntrl_ch.isChecked():
                self.com.set_local_control()
        except:
            pass

        # GUI
        self.connect_prog_bar.setValue(self.connect_prog_bar.maximum())
        self.com_lbl_portname_2.setStyleSheet("color: green")
        self.device_combo_box.setDisabled(True)
        self.com_pb_connect.setDisabled(True)
        self.disable_com_settings()
        self.device_ctrl_group_box.setEnabled(True)

    def com_pb_disconnect_clicked(self):
        try:
            self.com.disconnect()
            self.disp_info("INFO", "COM port closed")
            self.connect_prog_bar.setValue(self.connect_prog_bar.minimum())
            self.com_lbl_portname_2.setStyleSheet("color: blue")
            self.com_pb_connect.setEnabled(True)
            self.device_combo_box.setEnabled(True)
            self.enable_com_settings()

            self.device_ctrl_group_box.setDisabled(True)
        except:
            self.disp_info("ERROR", "Can't close serial port!")
            self.com_lbl_portname_2.setStyleSheet("color: red")

    def load_storage(self):
        try:
            msg = f"WAIT "
            # self.com.set_remote_control()
            # self.com.set_display("ON")
            # self.com.display_text(msg)

            for state in range(1, self.__class__.storage_len_max + 1):
                msg += "."
                try:
                    self.com.display_text(msg)
                except:
                    pass

                if state <= self.__class__.storage_len:
                    self.com.load_state(state)

                    voltage, current = float(self.com.get_voltage_limit()), float(self.com.get_current_limit())
                    self.store_btn.get(state)["voltage"] = voltage
                    self.store_btn.get(state)["current"] = current

                    volt_range = self.com.get_voltage_range()
                    self.store_btn.get(state)["range"] = volt_range

                    self.store_btn.get(state).get("store").setText(
                        f"Storage state {state}: Voltage: {round(voltage, 3)} V, current: {round(current, 3)} A"
                    )
                    self.store_btn.get(state).get("store").setEnabled(True)
                    self.disp_info("INFO", f"Device storage state {state}: {round(voltage, 3)} V, {round(current, 3)} A, range: {volt_range}")
                else:
                    self.store_btn.get(state).get("store").setText(f"Storage state {state} does not available")
                    self.store_btn.get(state).get("store").setDisabled(True)
                    self.disp_info("INFO", f"Device storage state {state} does not available")

                self.connect_prog_bar.setValue(self.connect_prog_bar.value() + int(
                    round(self.connect_prog_bar.maximum() / self.__class__.storage_len_max + 1)))

        except:
            self.disp_info("ERROR", "Can't read device storage states!")

    def state_load_btn_clicked(self):
        for state in range(1, self.__class__.storage_len + 1):
            # get selected state
            if self.store_btn.get(state).get("store").isChecked():

                # set voltage range from store
                volt_range = self.store_btn.get(state).get("range")

                if volt_range in self.__class__.range_low:
                    self.volt_range_low_btn.setChecked(True)
                    self.volt_range_high_btn.setChecked(False)
                elif volt_range in self.__class__.range_high:
                    self.volt_range_high_btn.setChecked(True)
                    self.volt_range_low_btn.setChecked(False)
                else:
                    self.disp_info("ERROR", f"Unknown voltage range value '{volt_range}'")
                    return

                try:
                    self.set_voltage_range()
                except:
                    self.disp_info("ERROR", "Can't set voltage range!")
                    return

                volt = self.store_btn.get(state).get("voltage")
                cur = self.store_btn.get(state).get("current")

                try:
                    self.set_default_limits(volt=volt, cur=cur)
                except:
                    self.disp_info("ERROR", "Can't set limits from this state!")

                self.disp_info("INFO", f"Load state {state}")
                break

    def state_save_btn_clicked(self):
        for state in range(1, self.__class__.storage_len + 1):
            # get selected state

            if self.store_btn.get(state).get("store").isChecked():

                # save voltage range
                if self.volt_range_low_btn.isChecked():
                    self.store_btn.get(state)["range"] = "LOW"
                elif self.volt_range_high_btn.isChecked():
                    self.store_btn.get(state)["range"] = "HIGH"
                else:
                    pass

                # save voltage and current values
                voltage, current = float(self.com.get_voltage_limit()), float(self.com.get_current_limit())

                self.store_btn.get(state)["voltage"] = float(voltage)
                self.store_btn.get(state)["current"] = float(current)

                # update selected state label
                self.store_btn.get(state).get("store").setText(
                    f"Storage state {state}: Voltage: {round(voltage, 3)} V, current: {round(current, 3)} A"
                )

                # save current parameters into device memory
                try:
                    self.com.save_state(state)
                    self.disp_info("INFO", f"Current device parameters saved into state {state}")
                except:
                    self.disp_info("ERROR", "Can't save state into device memory")
                    return

                break

    def say_beep(self):
        try:
            self.com.beep()
            self.disp_info("INFO", "Beeeeeeeeeeeep!")
        except:
            self.disp_info("ERROR", "Can't write command to device")

    def say_hello(self):
        try:
            self.com.set_remote_control()
            self.com.set_display("on")
            # self.com.clear_display()
            self.com.display_text("HELLO WORLD")
            sleep(1)
            self.com.clear_display()

            if self.dev_cntrl_ch.isChecked():
                self.com.set_local_control()

        except:
            self.disp_info("ERROR", "Can't display some text")

    def get_dev_version(self):
        try:
            ver = self.com.get_dev_version()
            self.disp_info("INFO", f"Device version: {ver}")
        except:
            self.disp_info("ERROR", "Can't get device version!")

    def get_dev_errors(self):
        try:
            err = self.com.get_dev_errors()
            self.disp_info("INFO", f"{err}")
        except:
            self.disp_info("ERROR", "Can't read device errors!")

    def dev_clear_display(self):
        try:
            self.com.clear_display()
        except:
            self.disp_info("ERROR", "Can't clear device display!")

    def dev_control_type_changed(self):
        if self.dev_cntrl_ch.isChecked():
            try:
                self.com.set_local_control()
                self.disp_info("INFO", f"Device place in local mode control!")
            except:
                self.disp_info("ERROR", f"Can't place device into a local mode control!")
        else:
            try:
                self.com.set_remote_control()
                self.disp_info("INFO", f"Device place in remote mode control!")
            except:
                self.disp_info("ERROR", f"Can't place device into a remote mode control!")

    def get_voltage_settings(self, range: str, param: str):
        return settings.get("devices").get(self.device_combo_box.currentText()).get("Voltage ranges").get(range).get(param)

    def set_voltage_range(self):

        if self.volt_range_low_btn.isChecked():

            volt_min, volt_max, cur_min, cur_max = [self.get_voltage_settings("Low", param) for param in self.__class__.params]
            # print(volt_min, volt_max, cur_min, cur_max)
            self.set_max_voltage_limits(volt_min, volt_max, cur_min, cur_max)

            self.disp_info("INFO", f"Low voltage range: "
                                   f"{volt_min} - {volt_max} V, {cur_min} - {cur_max} A")

            # if not self.dbspin_box_cur_lim.value():
            self.set_default_limits(volt_min, cur_max)

            # send to device
            self.com.set_voltage_low()
        else:

            volt_min, volt_max, cur_min, cur_max = [self.get_voltage_settings("High", param) for param in self.__class__.params]
            # print(volt_min, volt_max, cur_min, cur_max)
            self.set_max_voltage_limits(volt_min, volt_max, cur_min, cur_max)

            self.disp_info("INFO", f"High voltage range: "
                                   f"{volt_min} - {volt_max} V, {cur_min} - {cur_max} A")

            # if not self.dbspin_box_cur_lim.value():
            self.set_default_limits(volt_min, cur_max)

            # send to device
            self.com.set_voltage_high()

    def set_max_voltage_limits(self, volt_min: float, volt_max: float, cur_min: float, cur_max: float):
        # limits fields
        self.dbspin_box_volt_lim.setRange(volt_min, volt_max)
        self.dbspin_box_cur_lim.setRange(cur_min, cur_max)
        # voltage fiels
        self.dbspin_box_out_volt.setRange(volt_min, volt_max)

    def set_default_limits(self, volt: float, cur: float):
        try:

            self.com.set_voltage(volt)
            self.com.set_current(cur)

            self.dbspin_box_volt_lim.setValue(volt)
            self.dbspin_box_cur_lim.setValue(cur)
            self.dbspin_box_out_volt.setValue(volt)
        except:
            self.disp_info("ERROR", "Can't write default limits values")

    def get_current_limits(self):
        try:
            self.com.send_message("Volt?")
            volt = float(self.com.get_message())
            self.dbspin_box_volt_lim.setValue(volt)
            self.dbspin_box_out_volt.setValue(volt)

            self.com.send_message("Current?")
            cur = float(self.com.get_message())
            self.dbspin_box_cur_lim.setValue(cur)

            self.disp_info("INFO", f"Voltage: {volt} V, current: {cur} A")

        except:
            self.disp_info("ERROR", "Can't read voltage and current limits from device!")

    def set_limits(self):
        # self.cur_check_sleep()

        try:
            # get voltage and current from user interface
            volt = self.dbspin_box_volt_lim.value()
            cur = self.dbspin_box_cur_lim.value()

            # set output voltage
            # if not self.out_volt_onoff_btn.isChecked():
            self.dbspin_box_out_volt.setValue(volt)
        except:
            self.disp_info("ERROR", "Can't get limits from user interface :(")
            return

        try:
            self.com.set_voltage(volt)
            self.com.set_current(cur)

            self.disp_info("INFO", f"Output limits: voltage - {volt} V, current - {cur} A")
        except:
            self.disp_info("ERROR", "Can't set this limits parameters")

        # self.cur_check_run()

    def en_dis_output_control(self, cmd: bool):
        self.dbspin_box_out_volt.setEnabled(True) if cmd else self.dbspin_box_out_volt.setDisabled(True)
        self.out_volt_lbl.setEnabled(True) if cmd else self.out_volt_lbl.setDisabled(True)
        self.oyt_volt_set_btn.setEnabled(True) if cmd else self.oyt_volt_set_btn.setDisabled(True)
        self.out_cur_lbl.setEnabled(True) if cmd else self.out_cur_lbl.setDisabled(True)
        self.out_cur_ed.setEnabled(True) if cmd else self.out_cur_ed.setDisabled(True)
        self.combo_box_cur_mult.setEnabled(True) if cmd else self.combo_box_cur_mult.setDisabled(True)
        self.out_cur_get.setEnabled(True) if cmd else self.out_cur_get.setDisabled(True)
        # self.auto_check_ch_box.setEnabled(True) if cmd else self.auto_check_ch_box.setDisabled(True)

    def out_volt_onoff_btn_clicked(self):
        """Output ON/OFF control"""
        if self.out_volt_onoff_btn.isChecked():

            # get limits from device
            try:
                self.com.send_message("Volt?")
                dev_volt = float(self.com.get_message())
                user_volt = self.dbspin_box_volt_lim.value()

                self.com.send_message("Current?")
                dev_cur = float(self.com.get_message())
                user_cur = self.dbspin_box_cur_lim.value()

                if dev_volt != user_volt or dev_cur != user_cur:
                    self.disp_info("ERROR", f"User voltage: {user_volt} V, device voltage: {dev_volt} V; "
                                            f"user current: {user_cur} A, device current: {dev_cur} A. "
                                            f"Press 'Get' to update actual device limits")
                    self.out_volt_onoff_btn.setChecked(False)
                    return
            except:
                self.disp_info("ERROR", "Can't read voltage and current limits from device!")
                self.out_volt_onoff_btn.setChecked(False)
                return

            try:
                self.com.set_output("ON")
                self.disp_info("INFO", "Output ON")
            except:
                self.disp_info("ERROR", "Can't enable device output")
                return

            self.out_volt_onoff_btn.setText("ON")
            self.out_volt_onoff_btn.setStyleSheet(f"background-color: rgb(74, 255, 80)")
            self.volt_range_group_box.setDisabled(True)
            self.com_pb_disconnect.setDisabled(True)
            self.store_group_box.setDisabled(True)

            self.en_dis_output_control(True)

        else:

            try:
                self.com.set_output("OFF")
                self.disp_info("INFO", "Output OFF")
            except:
                self.disp_info("ERROR", "Can't disable device output")
                return

            self.out_volt_onoff_btn.setText("OFF")
            self.out_volt_onoff_btn.setStyleSheet(f"background-color: rgb(255, 119, 119)")
            self.volt_range_group_box.setEnabled(True)
            self.com_pb_disconnect.setEnabled(True)
            self.store_group_box.setEnabled(True)

            self.en_dis_output_control(False)

    def oyt_volt_set_btn_clicked(self):
        volt = self.dbspin_box_out_volt.value()

        self.dbspin_box_volt_lim.setValue(volt)
        self.set_limits()

        # self.cur_check_sleep()
        try:
            self.com.set_voltage(volt)
            self.disp_info("INFO", f"Output voltage: {volt} V!")
        except:
            self.disp_info("ERROR", f"Can't set output voltage {volt} V!")

        # self.cur_check_run()

    def out_cur_get_clicked(self):
        # self.cur_check_sleep()

        try:
            cur = round(float(self.com.get_current()), 3)
            self.out_cur_ed.setText(str(cur * self.get_current_mult()))
        except:
            self.disp_info("ERROR", "Can't read current measure from device")

        # self.cur_check_run()

    def auto_check_ch_box_clicked(self):
        if self.auto_check_ch_box.isChecked() and self.out_volt_onoff_btn.isChecked() and not self.cur_thread_stop:
            self.auto_cur_update_thread = Thread(target=self.out_cur_auto_check, daemon=True)
            self.auto_cur_update_thread.start()
            print("Started")

    def out_cur_auto_check(self):
        while self.auto_check_ch_box.isChecked() and self.out_volt_onoff_btn.isChecked() and not self.cur_thread_stop:
            self.out_cur_get_clicked()
            sleep(self.__class__.cur_update_time)
        print("Stopped")

    def get_current_mult(self) -> float:
        return self.__class__.cur_mult.get(self.combo_box_cur_mult.currentText())

    def cur_check_sleep(self):
        """Stop current check thread"""
        self.cur_thread_stop = True
        # sleep(0.1)

        try:
            if self.auto_cur_update_thread.is_alive():
                print("ALIVE")
                sleep(0.1)
            else:
                print("Not alive")
        except:
            print("No thread")

    def cur_check_run(self):
        self.cur_thread_stop = False

        try:
            if not self.auto_cur_update_thread.is_alive():
                self.auto_check_ch_box_clicked()
        except:
            print("Already exist")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
