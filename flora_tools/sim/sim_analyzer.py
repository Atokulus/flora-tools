import cairo

import flora_tools.lwb_round as lwb_round


class SimAnalyzer:
    def __init__(self, surface: cairo.SVGSurface):
        self.surface = surface

        if self.surface is not None:
            self.context = cairo.Context(self.surface)

    def draw_round(self, round: 'lwb_round.LWBRound'):
        pass
