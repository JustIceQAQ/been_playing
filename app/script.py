from .exhibition.cksmh.script import CKSMHRunner
from .exhibition.clab.script import CLabRunner
from .exhibition.fubonartmuseum.script import FuBonArtMuseumRunner
from .exhibition.huashan1914.script import HuaShan1914Runner
from .exhibition.jam.script import JamRunner
from .exhibition.kingcarart.script import KingCarArtRunner
from .platform.ibon.script import IBonRunner
from .platform.kkday.script import KKDayRunner
from .platform.kktix.script import KKTixRunner

PY_CLASS_SCRIPT = {
    CKSMHRunner,
    CLabRunner,
    FuBonArtMuseumRunner,
    HuaShan1914Runner,
    JamRunner,
    IBonRunner,
    KingCarArtRunner,
    KKDayRunner,
    KKTixRunner,
}
