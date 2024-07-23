# TFT components
# Copyright (c) 2023 Petr Kracik
# Copyright (c) 2023 OctopusLAB

from . import Component
from ..types.int import Int16


class VariablesIcon(Component):
    def __init__(self, dgus, sp_address, vp_address = None):
        super().__init__(dgus, sp_address, Int16, vp_address)
