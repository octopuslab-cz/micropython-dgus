# TFT components
# Copyright (c) 2026 Petr Kracik
# Copyright (c) 2026 OctopusLAB

from dgus.components import Component
from dgus.types.int import Int16


class VariablesIcon(Component):
    def __init__(self, dgus, sp_address, vp_address = None):
        super().__init__(dgus, sp_address, Int16, vp_address)
