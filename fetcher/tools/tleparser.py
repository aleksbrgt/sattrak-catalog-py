class TleParser:

    CELESTRAK = 1

    # Describe a TLE structure
    CELESTRAK_BP = {
        0: {
            'name': {
                'start': 0,
                'end': 23,
            }
        },
        1: {
            'line_number': {
                'start': 0,
                'end': 1,
            },
            'satellite_number': {
                'start': 2,
                'end': 7
            },
            'classification': {
                'start': 7,
                'end': 8,
            },
            'international_designator_year': {
                'start': 9,
                'end': 11,
            },
            'international_designator_number': {
                'start': 11,
                'end': 14,
            },
            'international_designator_piece': {
                'start': 14,
                'end': 16,
            },
            'epoch_year': {
                'start': 18,
                'end': 20,
            },
            'epoch_day': {
                'start': 20,
                'end': 32,
            },
            'first_derivative_mean_motion': {
                'start': 34,
                'end': 43,
            },
            'second_derivative_mean_motion': {
                'start': 44,
                'end': 52,
            },
            'drag': {
                'start': 53,
                'end': 62,
            },
            'set_number': {
                'start': 63,
                'end': 68,
            },
            'first_checksum': {
                'start': 68,
                'end': 69,
            },
        },
        2: {
            'inclination': {
                'start': 8,
                'end': 16,
            },
            'ascending_node': {
                'start': 17,
                'end': 25,
            },
            'eccentricity': {
                'start': 26,
                'end': 33,
            },
            'perigee_argument': {
                'start': 34,
                'end': 42,
            },
            'mean_anomaly': {
                'start': 43,
                'end': 51,
            },
            'mean_motion': {
                'start': 52,
                'end': 63,
            },
            'revolution_number': {
                'start': 63,
                'end': 68,
            },
            'second_checksum': {
                'start': 68,
                'end': 69,
            }
        }
    }

    def __init__(self, format=CELESTRAK):
        self.format = format

        if self.format == TleParser.CELESTRAK:
            self.structure = TleParser.CELESTRAK_BP

    def parse(self, tle):
        for line in tle:
            tle[line] = tle[line].decode("utf-8")
        return self.explode(tle)

    def explode(self, tle):
        """
            Extract data from TLE into a dict
        """
        blacklist = ['']

        exploded = {}

        for n in self.structure:
            exploded["line_%i_full" % n] = tle[n].strip()

            for e in self.structure[n]:
                start = self.structure[n][e]['start']
                end = self.structure[n][e]['end']
                value = tle[n][start:end].strip()

                if value in blacklist:
                    value = None
                    next

                if e == 'first_derivative_mean_motion':
                    value = "0%s" % value

                if e == 'second_derivative_mean_motion':
                    value = '0'

                if e == 'drag':
                    value = self.format_drag(value)

                if e == 'eccentricity':
                    value = '0.%s' % value

                exploded[e] = value

        return exploded

    def format_drag(self, raw_drag):
        """
            Format a drag value from a raw value in a TLE to a readable number
        """
        if raw_drag[0] == '-':
            raw_drag = raw_drag[1:]

        # Separate the two parts of iiiii-i
        raw_drag = raw_drag.replace('+', '-')
        parts = raw_drag.split('-')
        ending = parts[0]

        power = 0
        if (len(parts) != 1):
            power = parts[1]

        # Generate zeros depending on size of the power
        # try:
        zeros = ''.join(['0' for x in range(0, int(parts[1])-1)])
        # except ValueError:
            # return 0

        # Concatenate values, ending up with a value like 0.000iiiii
        return float('0.%s%s' % (zeros, ending))

