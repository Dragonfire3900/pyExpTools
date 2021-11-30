import pandas as pd

class GenExp(Object):
    """
    A class which represents a general computational experiment

    Attributes
    ----------
    sourcefile: Path

    readFunc: callable(Path) -> pandas.Dataframe

    data: pandas.Dataframe

    genFunc: callable(Path, **kargs) -> Path
    """

    def __init__(self):
        pass