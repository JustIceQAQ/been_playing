from .museums.aaaarchives import AAAArchivesRunner
from .museums.artistvillage import ArtistVillageRunner
from .museums.bopiliao.script import BoPiLiaoRunner
from .museums.chipolin import ChiPoLinRunner
from .museums.cksmh.script import CKSMHRunner
from .museums.clab.script import CLabRunner
from .museums.culture435 import Culture435Runner
from .museums.fubonartmuseum.script import FuBonArtMuseumRunner
from .museums.hong_gah.script import HongGahRunner
from .museums.huashan1914.script import HuaShan1914Runner
from .museums.jam.script import JamRunner
from .museums.kdmofa.script import KdMoFaRunner
from .museums.khm import KhmRunner
from .museums.kingcarart.script import KingCarArtRunner
from .museums.kishuan import KiShuAnRunner
from .museums.kmfa import KmFaRunner
from .museums.kmoa import KmoaRunner
from .museums.mocataipei.script import MoCaTaipeiRunner
from .museums.montue import MoNTUERunner
from .museums.museumpost.script import MuseumPostRunner
from .museums.mwr.script import MwrRunner
from .museums.n228mm.script import N228MMRunner
from .museums.ncpi.script import NCPIRunner
from .museums.nhrm.script import NHRMRunner
from .museums.nmh.script import NmhRunner
from .museums.npm.script import NpmRunner
from .museums.nrm import NrmRunner
from .museums.ntaec import NTAECRunner
from .museums.ntc_art_museum.script import NtcArtMuseumRunner
from .museums.ntcri.script import NTCRIRunner
from .museums.ntm.script import NtmRunner
from .museums.ntnu_art_museum.script import NTNUArtMuseumRunner
from .museums.ntpc.script import NTPCRunner
from .museums.ntsec.script import NtSecRunner
from .museums.ocam.script import OCAMRunner
from .museums.pact import PactRunner
from .museums.pier2 import Pier2Runner
from .museums.redhouse import RedHouseRunner
from .museums.shungyeart.script import ShungYeArtRunner
from .museums.songshanculturalpark.script import SongShanCulturalParkRunner
from .museums.taipeiexpopark.script import TaipeiExPoParkRunner
from .museums.tcm import TcmRunner
from .museums.tfam.script import TFamRunner
from .museums.tmc.script import TmcRunner
from .museums.tnammuseum import TnamMuseumRunner
from .museums.tncmmm.script import TncMMMRunner
from .museums.tncsec import TnCsEcRunner
from .museums.twtc.script import TwTcRunner
from .museums.yatsen import YatsenRunner
from .museums.yochangart import YoChangArtRunner
from .platform.bookstickets.script import BooksTicketsRunner
from .platform.cultureexpress import CultureExpressRunner
from .platform.gacc import GaCcRunner
from .platform.ibon.script import IBonRunner
from .platform.kkday.script import KKDayRunner
from .platform.kktix.script import KKTixRunner
from .platform.klook.script import KLookRunner
from .platform.opentix.script import OpenTixRunner
from .platform.udnfunlife.script import UdnFunLifeRunner

PLATFORM_RUNNERS = {
    BooksTicketsRunner,
    CultureExpressRunner,
    GaCcRunner,
    IBonRunner,
    KKDayRunner,
    KKTixRunner,
    KLookRunner,
    OpenTixRunner,
    UdnFunLifeRunner,
}

MUSEUMS_RUNNERS = {
    CKSMHRunner,
    CLabRunner,
    FuBonArtMuseumRunner,
    HuaShan1914Runner,
    JamRunner,
    KingCarArtRunner,
    MoCaTaipeiRunner,
    MuseumPostRunner,
    MwrRunner,
    NCPIRunner,
    NmhRunner,
    NpmRunner,
    NtcArtMuseumRunner,
    NtmRunner,
    NtSecRunner,
    SongShanCulturalParkRunner,
    TFamRunner,
    TmcRunner,
    TwTcRunner,
    NTCRIRunner,
    TaipeiExPoParkRunner,
    NHRMRunner,
    NTNUArtMuseumRunner,
    BoPiLiaoRunner,
    OCAMRunner,
    NTPCRunner,
    TncMMMRunner,
    KdMoFaRunner,
    N228MMRunner,
    HongGahRunner,
    ShungYeArtRunner,
    YatsenRunner,
    NrmRunner,
    ChiPoLinRunner,
    PactRunner,
    RedHouseRunner,
    YoChangArtRunner,
    KhmRunner,
    KmFaRunner,
    Pier2Runner,
    TcmRunner,
    KmoaRunner,
    NTAECRunner,
    Culture435Runner,
    TnamMuseumRunner,
    TnCsEcRunner,
    MoNTUERunner,
    AAAArchivesRunner,
    ArtistVillageRunner,
    KiShuAnRunner,
}

ALL_RUNNERS = PLATFORM_RUNNERS | MUSEUMS_RUNNERS
