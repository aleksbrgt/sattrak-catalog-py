
class SatcatParser():
    """
        Tools for satellite catalog parsing
    """

    CELESTRAK = 1

    # Describe the CatalogEntries from Celestrak
    CELESTRAK_BP = {
        'international_designator': {
            'start': 0,
            'end': 12,
        },
        'norad_catalog_number': {
            'start': 13,
            'end': 18,
        },
        'names': {
            'start': 23,
            'end': 47,
        },
        'has_payload': {
            'start': 20,
            'end': 21,
        },
        'multiple_flag': {
            'start': 19,
            'end': 20,
        },
        'operational_status': {
            'start': 21,
            'end': 22,
        },
        'owner': {
            'start': 49,
            'end': 54,
        },
        'launch_date': {
            'start': 56,
            'end': 66,
        },
        'launch_site': {
            'start': 68,
            'end': 73,
        },
        'decay_date': {
            'start': 75,
            'end': 85,
        },
        'orbital_period': {
            'start': 87,
            'end': 94,
        },
        'inclination': {
            'start': 96,
            'end': 101,
        },
        'apogee': {
            'start': 103,
            'end': 109,
        },
        'perigee': {
            'start': 111,
            'end': 117,
        },
        'radar_cross_section': {
            'start': 119,
            'end': 127,
        },
        'orbital_status': {
            'start': 129,
            'end': 132,
        },
    }

    def __init__(self, format=CELESTRAK):
        self.format = format

        if self.format == SatcatParser.CELESTRAK:
            self.structure = SatcatParser.CELESTRAK_BP

    def parse_line(self, line):
        line = line.decode("utf-8")
        return self.explode(line)

    def explode(self, line):
        blacklist = ['N/A', '']

        exploded_line = {}
        for e in self.structure:
            start = self.structure[e]['start']
            end = self.structure[e]['end']
            value = line[start:end].strip()

            if value in blacklist:
                value = None

            exploded_line[e] = value
        return exploded_line
