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
from .exhibition.songshanculturalpark.script import SongShanCulturalParkRunner
from .exhibition.tfam.script import TFamRunner
from .platform.bookstickets.script import BooksTicketsRunner
from .platform.ibon.script import IBonRunner
from .platform.kkday.script import KKDayRunner
from .platform.kktix.script import KKTixRunner
from .platform.klook.script import KLookRunner
from .platform.opentix.script import OpenTixRunner
from .platform.udnfunlife.script import UdnFunLifeRunner

PY_CLASS_SCRIPT = {
    BooksTicketsRunner,
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
    SongShanCulturalParkRunner,
    TFamRunner,
    UdnFunLifeRunner,
}
