
# File with power supplies settings

settings = {
    "devices": {

        # dev_01
        "Keysight E3645A": {
            # device description
            "description": "Vendor: Agilent Technologies. Power supply parameters: 0-35V 2.2 A; 0-60V 1.3 A",

            # COM port settings for workspace
            "COM_settings": {
                "baudrate": [300, 600, 1200, 2400, 4800, 9600, ][::-1],
                "bytesize": [7, 8, ][::-1],
                "stop_bits": [2, ][::-1],
                "parity": ["None", "Odd", "Even", ],
            },

            # Power Supply parameters
            "Voltage ranges": {
                "Low": {
                    "voltage_min": 0,
                    "voltage_max": 35,
                    "current_min": 0,
                    "current_max": 2.2,
                },
                "High": {
                    "voltage_min": 0,
                    "voltage_max": 60,
                    "current_min": 0,
                    "current_max": 1.3,
                },
            },

            # Storage depth
            "storage_depth": 5,
        },

        # dev_02
        "Keysight E3644A": {
            # device description
            "description": "Vendor: Agilent Technologies. Power supply parameters: 0-8V 8 A; 0-20V 4 A",

            # COM port settings for workspace
            "COM_settings": {
                "baudrate": [300, 600, 1200, 2400, 4800, 9600, ][::-1],
                "bytesize": [7, 8, ][::-1],
                "stop_bits": [2, ][::-1],
                "parity": ["None", "Odd", "Even", ],
            },

            # Power Supply parameters
            "Voltage ranges": {
                "Low": {
                    "voltage_min": 0,
                    "voltage_max": 8,
                    "current_min": 0,
                    "current_max": 8,
                },
                "High": {
                    "voltage_min": 0,
                    "voltage_max": 20,
                    "current_min": 0,
                    "current_max": 4,
                },
            },

            # Storage depth
            "storage_depth": 5,
        },

        # dev_03
        "Keysight E3643A": {
            # device description
            "description": "Vendor: Agilent Technologies. Power supply parameters: 0-35V 1.4 A; 0-60V 0.8 A",

            # COM port settings for workspace
            "COM_settings": {
                "baudrate": [300, 600, 1200, 2400, 4800, 9600, ][::-1],
                "bytesize": [7, 8, ][::-1],
                "stop_bits": [2, ][::-1],
                "parity": ["None", "Odd", "Even", ],
            },

            # Power Supply parameters
            "Voltage ranges": {
                "Low": {
                    "voltage_min": 0,
                    "voltage_max": 35,
                    "current_min": 0,
                    "current_max": 1.4,
                },
                "High": {
                    "voltage_min": 0,
                    "voltage_max": 60,
                    "current_min": 0,
                    "current_max": 0.8,
                },
            },

            # Storage depth
            "storage_depth": 5,
        },

        # dev_04
        "Keysight E3642A": {
            # device description
            "description": "Vendor: Agilent Technologies. Power supply parameters: 0-8V 5 A; 0-20V 2.5 A",

            # COM port settings for workspace
            "COM_settings": {
                "baudrate": [300, 600, 1200, 2400, 4800, 9600, ][::-1],
                "bytesize": [7, 8, ][::-1],
                "stop_bits": [2, ][::-1],
                "parity": ["None", "Odd", "Even", ],
            },

            # Power Supply parameters
            "Voltage ranges": {
                "Low": {
                    "voltage_min": 0,
                    "voltage_max": 8,
                    "current_min": 0,
                    "current_max": 5,
                },
                "High": {
                    "voltage_min": 0,
                    "voltage_max": 20,
                    "current_min": 0,
                    "current_max": 2.5,
                },
            },

            # Storage depth
            "storage_depth": 5,
        },

        # dev_05
        "Keysight E3641A": {
            # device description
            "description": "Vendor: Agilent Technologies. Power supply parameters: 0-35V 0.8 A; 0-60V 0.5 A",

            # COM port settings for workspace
            "COM_settings": {
                "baudrate": [300, 600, 1200, 2400, 4800, 9600, ][::-1],
                "bytesize": [7, 8, ][::-1],
                "stop_bits": [2, ][::-1],
                "parity": ["None", "Odd", "Even", ],
            },

            # Power Supply parameters
            "Voltage ranges": {
                "Low": {
                    "voltage_min": 0,
                    "voltage_max": 35,
                    "current_min": 0,
                    "current_max": 0.8,
                },
                "High": {
                    "voltage_min": 0,
                    "voltage_max": 60,
                    "current_min": 0,
                    "current_max": 0.5,
                },
            },

            # Storage depth
            "storage_depth": 5,
        },

        # dev_06
        "Keysight E3640A": {
            # device description
            "description": "Vendor: Agilent Technologies. Power supply parameters: 0-8V 3 A; 0-20V 1.5 A",

            # COM port settings for workspace
            "COM_settings": {
                "baudrate": [300, 600, 1200, 2400, 4800, 9600, ][::-1],
                "bytesize": [7, 8, ][::-1],
                "stop_bits": [2, ][::-1],
                "parity": ["None", "Odd", "Even", ],
            },

            # Power Supply parameters
            "Voltage ranges": {
                "Low": {
                    "voltage_min": 0,
                    "voltage_max": 8,
                    "current_min": 0,
                    "current_max": 3,
                },
                "High": {
                    "voltage_min": 0,
                    "voltage_max": 20,
                    "current_min": 0,
                    "current_max": 1.5,
                },
            },

            # Storage depth
            "storage_depth": 5,
        },

        # dev_07
        "Keysight E3634A": {
            # device description
            "description": "Vendor: Agilent Technologies. Power supply parameters: 0-25V 7 A; 0-50V 4 A",

            # COM port settings for workspace
            "COM_settings": {
                "baudrate": [300, 600, 1200, 2400, 4800, 9600, ][::-1],
                "bytesize": [7, 8, ][::-1],
                "stop_bits": [2, ][::-1],
                "parity": ["None", "Odd", "Even", ],
            },

            # Power Supply parameters
            "Voltage ranges": {
                "Low": {
                    "voltage_min": 0,
                    "voltage_max": 25,
                    "current_min": 0,
                    "current_max": 7,
                },
                "High": {
                    "voltage_min": 0,
                    "voltage_max": 50,
                    "current_min": 0,
                    "current_max": 4,
                },
            },

            # Storage depth
            "storage_depth": 3,
        },

        # dev_08
        "Keysight E3633A": {
            # device description
            "description": "Vendor: Agilent Technologies. Power supply parameters: 0-8V 20 A; 0-20V 10 A",

            # COM port settings for workspace
            "COM_settings": {
                "baudrate": [300, 600, 1200, 2400, 4800, 9600, ][::-1],
                "bytesize": [7, 8, ][::-1],
                "stop_bits": [2, ][::-1],
                "parity": ["None", "Odd", "Even", ],
            },

            # Power Supply parameters
            "Voltage ranges": {
                "Low": {
                    "voltage_min": 0,
                    "voltage_max": 8,
                    "current_min": 0,
                    "current_max": 20,
                },
                "High": {
                    "voltage_min": 0,
                    "voltage_max": 20,
                    "current_min": 0,
                    "current_max": 10,
                },
            },

            # Storage depth
            "storage_depth": 3,
        },

        # dev_09
        "Keysight E3632A": {
            # device description
            "description": "Vendor: Agilent Technologies. Power supply parameters: 0-15V 7 A; 0-30V 4 A",

            # COM port settings for workspace
            "COM_settings": {
                "baudrate": [300, 600, 1200, 2400, 4800, 9600, ][::-1],
                "bytesize": [7, 8, ][::-1],
                "stop_bits": [2, ][::-1],
                "parity": ["None", "Odd", "Even", ],
            },

            # Power Supply parameters
            "Voltage ranges": {
                "Low": {
                    "voltage_min": 0,
                    "voltage_max": 15,
                    "current_min": 0,
                    "current_max": 7,
                },
                "High": {
                    "voltage_min": 0,
                    "voltage_max": 30,
                    "current_min": 0,
                    "current_max": 4,
                },
            },

            # Storage depth
            "storage_depth": 3,
        },

        # add new device under this line
    },
}

commands = {
    "ID": "*IDN?",
    "reset": "*RST",
    "set_current": "Current {}",
    "get_current": "Measure:Current?",
    "get_current_limit": "CURRent?",
    "set_voltage": "Volt {}",
    "get_voltage": "Measure:Volt?",
    "get_voltage_limit": "Volt?",
    "set_output": "Output {}",
    "get_voltage_range": "VOLTage:RANGe?",
    "set_voltage_high": "VOLTage:RANGe HIGH",
    "set_voltage_low": "VOLTage:RANGe LOW",
    "beep": "SYSTem:BEEPer",
    "version": "SYSTem:VERSion?",
    "get_errors": "SYSTem:ERRor?",
    "set_local_control": "SYSTem:LOCal",
    "set_remote_control": "SYSTem:REMote",
    "set_display": "DISPlay {}",
    "clear_display": "DISPlay:TEXT:CLEar",
    "display_text": "DISPlay:TEXT '{}'",
    "save_state": "*SAV {}",
    "load_state": "*RCL {}",
}


