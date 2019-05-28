import inputs

EVENT_ABB = (
    ('ABS_X', 'LSX'),
    ('ABS_Y', 'LSY'),
    ('ABS_RX', 'RSX'),
    ('ABS_RY', 'RSY'),

    ('BTN_START', 'START'),
    ('BTN_SELECT', 'SELECT'),

    ('BTN_NORTH', 'Y'),
    ('BTN_EAST', 'B'),
    ('BTN_SOUTH', 'A'),
    ('BTN_WEST', 'X'),

    ('ABS_HAT0X', 'HX'),
    ('ABS_HAT0Y', 'HY'),

    ('BTN_THUMBL', 'LS'),
    ('BTN_THUMBR', 'RS'),

    ('BTN_TL', 'LB'),
    ('BTN_TR', 'RB'),

    ('ABS_Z', 'LT'),
    ('ABS_RZ', 'RT')

)


class XBoxController(object):
    def __init__(self, gamepad=None, abbrevs=EVENT_ABB):
        self.states = {}
        self.abbrevs = dict(abbrevs)
        for _, value in self.abbrevs.items():
            self.states[value] = 0

        self.gamepad = gamepad
        if not gamepad:
            self._get_gamepad()

    def _get_gamepad(self):
        try:
            self.gamepad = inputs.devices.gamepads[0]
        except IndexError:
            raise inputs.UnpluggedError("No gamepad found.")

    def process_event(self, event):
        if event.ev_type == 'Absolute' or event.ev_type == 'Key':
            abbv = self.abbrevs[event.code]
            self.states[abbv] = event.state

            # self.output_state()

    def output_state(self):
        output_string = ""
        for key, value in self.states.items():
            output_string += key + ':' + str(value) + ' '
        print(output_string)

    def process_events(self):
        try:
            events = self.gamepad.read()
        except EOFError:
            events = []
        for event in events:
            self.process_event(event)


def main():
    controller = XBoxController()
    while 1:
        controller.process_events()


if __name__ == "__main__":
    main()
