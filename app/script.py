from .exhibition.cksmh.script import CKSMHRunner
from .exhibition.clab.script import CLabRunner
from .exhibition.fubonartmuseum.script import FuBonArtMuseumRunner
from .exhibition.huashan1914.script import HuaShan1914Runner
from .exhibition.jam.script import JamRunner
from .exhibition.kingcarart.script import KingCarArtRunner
from .exhibition.mocataipei.script import MoCaTaipeiRunner
from .exhibition.museumpost.script import MuseumPostRunner
from .exhibition.mwr.script import MwrRunner
from .exhibition.ncpi.script import NCPIRunner
from .exhibition.nmh.script import NmhRunner
from .exhibition.npm.script import NpmRunner
from .exhibition.ntc_art_museum.script import NtcArtMuseumRunner
from .exhibition.ntm.script import NtmRunner
from .exhibition.ntsec.script import NtSecRunner
from .platform.ibon.script import IBonRunner
from .platform.kkday.script import KKDayRunner
from .platform.kktix.script import KKTixRunner
from .platform.klook.script import KLookRunner
from .platform.opentix.script import OpenTixRunner

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
    KLookRunner,
    MoCaTaipeiRunner,
    MuseumPostRunner,
    MwrRunner,
    NCPIRunner,
    NmhRunner,
    NpmRunner,
    NtcArtMuseumRunner,
    NtmRunner,
    NtSecRunner,
    OpenTixRunner,
}
