from .galleries.capitalart import CapitalArtRunner
from .galleries.cg1839 import CG1839Runner
from .galleries.dac99 import Dac99Runner
from .galleries.mindsetart import MindSetArtRunner
from .galleries.ruomu import RuoMuRunner
from .galleries.sokaart import SoKaArtRunner
from .galleries.whitestone import WhiteStoneRunner
from .galleries.xizhitang import XiZhiTangRunner
from .galleries.yiyun import YiYunRunner
from .museums.afmc.script import (
    AfmcHall1Runner,
    AfmcHall2Runner,
    AfmcHall3Runner,
    AfmcHall4Runner,
    AfmcHall5Runner,
    AfmcHall6Runner,
)
from .museums.aaaarchives import AAAArchivesRunner
from .museums.alien import AlienRunner
from .museums.artistvillage import ArtistVillageRunner
from .museums.as241.script import AS241Runner
from .museums.bopiliao.script import BoPiLiaoRunner
from .museums.ccam.script import CCAMRunner
from .museums.chcsec import ChCsEcRunner
from .museums.chiayiam import ChiayiAMRunner
from .museums.chiayimm import ChiayiMMRunner
from .museums.chipolin import ChiPoLinRunner
from .museums.cksmh.script import CKSMHRunner
from .museums.clab.script import CLabRunner
from .museums.culture435 import Culture435Runner
from .museums.elandam.script import ELandAMRunner
from .museums.fubonartmuseum.script import FuBonArtMuseumRunner
from .museums.hcam.script import HCAMRunner
from .museums.hcccart.script import HcccArtRunner
from .museums.historysinica import HistorySinicaRunner
from .museums.hkm import HKMRunner
from .museums.hong_gah.script import HongGahRunner
from .museums.huashan1914.script import HuaShan1914Runner
from .museums.ioesinica import IOESinicaRunner
from .museums.jam.script import JamRunner
from .museums.juming import JuMingRunner
from .museums.kdmofa.script import KdMoFaRunner
from .museums.khm import KhmRunner
from .museums.kingcarart.script import KingCarArtRunner
from .museums.kishuan import KiShuAnRunner
from .museums.kmfa import KmFaRunner
from .museums.kmoa import KmoaRunner
from .museums.mocataipei.script import MoCaTaipeiRunner
from .museums.mofia import MofiaRunner
from .museums.montue import MoNTUERunner
from .museums.museumpost.script import MuseumPostRunner
from .museums.mwr.script import MwrRunner
from .museums.n228mm.script import N228MMRunner
from .museums.ncpi.script import NCPIRunner
from .museums.nhclac import NhClAcRunner
from .museums.nhrm.script import NHRMRunner
from .museums.nmh.script import NmhRunner
from .museums.nmth import NMTHRunner
from .museums.nmtl import NMTLRunner
from .museums.npm.script import NpmRunner
from .museums.nrm import NrmRunner
from .museums.ntaec import NTAECRunner
from .museums.ntc_art_museum.script import NtcArtMuseumRunner
from .museums.ntcri.script import NTCRIRunner
from .museums.ntm.script import NtmRunner
from .museums.ntmofa import NtMofaRunner
from .museums.ntnu_art_museum.script import NTNUArtMuseumRunner
from .museums.ntpc.script import NTPCRunner
from .museums.ntsec.script import NtSecRunner
from .museums.ocam.script import OCAMRunner
from .museums.pact import PactRunner
from .museums.pier2 import Pier2Runner
from .museums.pt1936.script import PT1936Runner
from .museums.ptam.script import PTAMRunner
from .museums.ptcam.script import PTCAMRunner
from .museums.redhouse import RedHouseRunner
from .museums.shungyeart.script import ShungYeArtRunner
from .museums.songshanculturalpark.script import SongShanCulturalParkRunner
from .museums.taipeiexpopark.script import TaipeiExPoParkRunner
from .museums.taipeizoo.script import TaipeiZooRunner
from .museums.tam.script import TAMRunner
from .museums.tcam.script import TcamRunner
from .museums.tcm import TcmRunner
from .museums.tfam.script import TFamRunner
from .museums.tmc.script import TmcRunner
from .museums.tnammuseum import TnamMuseumRunner
from .museums.tncmmm.script import TncMMMRunner
from .museums.tncsec import TnCsEcRunner
from .museums.ttcsec import TtCsEcRunner
from .museums.twtc.script import TwTcRunner
from .museums.tycg import TyCgRunner
from .museums.yatsen import YatsenRunner
from .museums.yochangart import YoChangArtRunner
from .platform.artemperor import ArtEmperorRunner
from .platform.bookstickets.script import BooksTicketsRunner
from .platform.cultureexpress import CultureExpressRunner
from .platform.gacc import GaCcRunner
from .platform.ibon.script import IBonRunner
from .platform.iculture import ICultureRunner
from .platform.kkday.script import KKDayRunner
from .platform.kktix.script import KKTixRunner
from .platform.klook.script import KLookRunner
from .platform.ntt import NTTRunner
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
    ArtEmperorRunner,
    NTTRunner,
    ICultureRunner,
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
    TaipeiZooRunner,
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
    AfmcHall1Runner,
    AfmcHall2Runner,
    AfmcHall3Runner,
    AfmcHall4Runner,
    AfmcHall5Runner,
    AfmcHall6Runner,
    AAAArchivesRunner,
    ArtistVillageRunner,
    KiShuAnRunner,
    NMTLRunner,
    NMTHRunner,
    ChiayiMMRunner,
    ChiayiAMRunner,
    NtMofaRunner,
    ChCsEcRunner,
    NhClAcRunner,
    TtCsEcRunner,
    AlienRunner,
    MofiaRunner,
    IOESinicaRunner,
    HistorySinicaRunner,
    HKMRunner,
    JuMingRunner,
    TyCgRunner,
    PTAMRunner,
    HcccArtRunner,
    TcamRunner,
    TAMRunner,
    CCAMRunner,
    ELandAMRunner,
    HCAMRunner,
    AS241Runner,
    PT1936Runner,
    PTCAMRunner,
}

GALLERIES_RUNNERS = {
    CapitalArtRunner,
    RuoMuRunner,
    YiYunRunner,
    MindSetArtRunner,
    Dac99Runner,
    WhiteStoneRunner,
    XiZhiTangRunner,
    CG1839Runner,
    SoKaArtRunner,
}

ALL_RUNNERS = list(PLATFORM_RUNNERS) + list(MUSEUMS_RUNNERS) + list(GALLERIES_RUNNERS)
