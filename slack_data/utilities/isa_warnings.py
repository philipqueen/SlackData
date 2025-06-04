from enum import Enum

class ISAWarning(str, Enum):
    """
    ISA Warning Classifications

    database found here: https://data.slacklineinternational.org/safety/isa-gear-warnings/
    """

    RECALL = "Recall"
    WARNING = "Warning"
    NOTICE = "Notice"
    NO_WARNING = "No Warning"