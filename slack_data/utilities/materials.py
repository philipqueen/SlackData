from enum import Enum


class MetalMaterial(str, Enum):
    ALUMINUM = "Aluminum"
    STEEL = "Steel"
    STAINLESS_STEEL = "Stainless Steel"
    TITANIUM = "Titanium"
    OTHER = "Other"