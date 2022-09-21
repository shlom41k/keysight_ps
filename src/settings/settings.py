settings = {
    "devices": {
        "Keysight E3645A": {
            # device description
            "description": "Vendor: Agilent Technologies. Power supply parameters: 0-35V 2.2 A; 0-60V 1.3 A",

            # COM port settings for workspace
            "COM_settings": {
                "baudrate": [300, 600, 1200, 2400, 4800, 9600, ][::-1],
                "bytesize": [7, 8, ][::-1],
                "stop_bits": [0, 1, 2, ][::-1],
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
        },
        # add new device under this line
    },
}

commands = {
    "ID": "*IDN?",
    "reset": "*RST",
    "set_current": "Current {}",
    "get_current": "Measure:Current?",
    "set_voltage": "Volt {}",
    "get_voltage": "Measure:Volt?",
    "set_output": "Output {}",
    "get_voltage_range": "VOLTage:RANGe?",
    "set_voltage_high": "VOLTage:RANGe HIGH",
    "set_voltage_low": "VOLTage:RANGe LOW",
}

