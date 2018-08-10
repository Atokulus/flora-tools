import datetime
import json
import ntpath
import os
import os.path
import re
from datetime import timedelta
from pathlib import Path
from threading import Timer

import dateutil
import pandas as pd
import requests

FLOCKLAB_ADDRESS = 'https://www.flocklab.ethz.ch/user'
FLOCKLAB_SERIAL_ADDRESS = "whymper.ee.ethz.ch"
FLOCKLAB_SERIAL_BASE_PORT = 50100

FLOCKLAB_TARGET_ID_LIST = [
    1, 3, 4, 8, 10, 13, 15, 20, 22, 23, 24, 25, 26, 28, 32, 33  # 11, 7 not working?
]

FLOCKLAB_TARGET_POSITIONS = {
    1: (110, -149), 3: (188, -359), 4: (171, -182), 7: (778, -237), 8: (166, -248), 10: (457, -323),
    11: (657, -240), 13: (711, -423), 15: (216, -246), 20: (579, -441), 22: (257, -461), 23: (397, -420),
    24: (424, -512), 25: (682, -353), 26: (538, -334), 28: (240, -425), 32: (289, -318), 33: (163, -306)
}

START_TIME_OFFSET = 60


class WindowsInhibitor:
    '''Prevent OS sleep/hibernate in windows; code from:
    https://github.com/h3llrais3r/Deluge-PreventSuspendPlus/blob/master/preventsuspendplus/core.py
    API documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx'''
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001

    def __init__(self):
        pass

    def inhibit(self):
        import ctypes
        print("Preventing Windows from going to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS |
            WindowsInhibitor.ES_SYSTEM_REQUIRED)

    def uninhibit(self):
        import ctypes
        print("Allowing Windows to go to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS)


class FlockLab:
    def __init__(self):
        self.callback = None
        self.osSleep = None

        self.auth = self.parse_auth()

    def parse_auth(self):
        home_auth = os.path.join(str(Path.home()), '.flocklabauth')

        if os.path.isfile('.flocklabauth'):
            authfile = '.flocklabauth'
        elif os.path.isfile(home_auth):
            authfile = home_auth
        else:
            raise Exception("Error. No auth information given!")

        envre = re.compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''')
        result = {}
        with open(authfile) as ins:
            for line in ins:
                match = envre.match(line)
                if match is not None:
                    result[match.group(1)] = match.group(2)

        if 'USER' not in result or 'PASSWORD' not in result:
            raise Exception("Error. Auth information not in correct format! "
                            "You have to place the file '.flocklabauth' under your home or working directory."
                            "See https://gitlab.ethz.ch/tec/public/flocklab/wikis/Man/Tutorials/Tutorial7")

        return result

    def schedule_test(self, xmlfile, callback=None):
        self.callback = callback

        url = "{}/{}".format(FLOCKLAB_ADDRESS, '/newtest.php')

        files = {'xmlfile': (ntpath.basename(xmlfile), open(xmlfile, 'rb'), 'application/xml')}

        r = requests.post(url,
                          data={'username': self.auth['USER'],
                                'password': self.auth['PASSWORD'],
                                'first': 'no',
                                },
                          files=files)

        success_regex = '<!-- cmd --><p>Test \(Id [0-9]*\) successfully added\.</p><!-- cmd -->'

        if re.search(success_regex, r.text):
            regex = '.*<!-- flocklabscript,([0-9]*),([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{4}),([0-9]*)-->.*'

            m = re.search(regex, r.text)

            test = {
                'id': m.group(1),
                'start_time': dateutil.parser.parse(m.group(2))
            }

            print(
                "Test successfully added to FlockLab. Test (ID {}) starts on {}".format(test['id'], test['start_time']))

            if self.callback is not None:
                delta = test['start_time'] - datetime.datetime.now(datetime.timezone.utc) + timedelta(
                    seconds=START_TIME_OFFSET)
                print("Experiment callback will start in {} at {}.".format(delta, test['start_time'] + timedelta(
                    seconds=START_TIME_OFFSET)))

                self.osSleep = None
                # in Windows, prevent the OS from sleeping while we run
                if os.name == 'nt':
                    self.osSleep = WindowsInhibitor()
                    self.osSleep.inhibit()

                t = Timer(delta.seconds, self.handle_test_callback)
                t.start()  # Start after delta time
        else:
            print(r.text)
            raise Exception("Error. Auth information wrong, file not validated or connected via IPv6!")

    def handle_test_callback(self):
        self.callback()

        if self.osSleep:
            self.osSleep.uninhibit()

    @staticmethod
    def parse_serial_log(file):
        with open(file) as f:
            lines = f.readlines()

            logs = [pd.DataFrame(columns=['timestamp', 'observer_id', 'node_id', 'rx', 'output'])]

            total_lines = len(lines)

            print("# lines to process: {}".format(total_lines))

            for i, line in enumerate(lines[1:-1]):
                line = line.rstrip()
                values = line.split(',', maxsplit=4)

                if len(values) is 5:

                    try:
                        parsed_content = json.loads(values[4])
                    except ValueError as e:
                        parsed_content = values[4]

                    parsed = {
                        'timestamp': [float(values[0])],
                        'observer_id': [int(values[1])],
                        'node_id': [int(values[2])],
                        'rx': [(True if values[3] == 'r' else False)],
                        'output': [parsed_content],
                    }

                    logs.append(pd.DataFrame(parsed))

                    if (i % 1000) == 0:
                        print(i, end=',')

            print("Parsing finished!")
            return pd.concat(logs, ignore_index=True)
