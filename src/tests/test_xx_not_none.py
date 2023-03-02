from datclass import dataclass, DatClass, Dict


@dataclass
class Log(DatClass):
    version: str = None
    creator: Dict = None


@dataclass
class Har(DatClass):
    log: Log = None


def test_xx_not_none():
    Har(**{
        'log': None
    })
