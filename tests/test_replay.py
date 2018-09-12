import datetime as dt
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from replay import ReplayData, PlayerData, FrameData, ActionType, Action, Character, StageType, Stage


SAMPLE_REPLAY_DATA = '''001030521211831072018SAMPLE REPLAY                   This is a replay I recorded to use as a sample in my replay parser.                                                                         0000022740
11501082000000000
HPlayer 1                              10000010004F2EAFCFCEDFC45FF405CCBF0FFC72038                  
1Z101zy327R102y333103y338I104y341I105y344106y345108y346109y349110y354111y358112y359115y  0119y  6120Zy 90r121y  0128zRI129I130y360I131y354I132y346133y344142y345143y346148C150y345151y344152y350153y  2154Zy  0rc181y180182y166183zy162L184y160186y156187y153U188y155189y156u190y157191y159C192y163193y176194y182195Zy192l196y  0c213A221a242y 78243y 75244zy 83UM245PM246y 79PM247y 78M248y 77249y 76251A257a281y 69282Zy 73u283y  0298y237299y252300zy258DO301O302y252LO303y250A310y252311y253a312y255l313y256317y257318y258319y259321y260323y261324y263325y264326y266327y267328y269329y270331y267332Zy201d333y180334y  0352zR353y346I354y345I355y344I356y342357y339359C360y341361y342362y343363y344364c365y345366y347367y358368Zy 28r369y 90370y  0412y 57413zy 69RUPM414y 67PM415y 65PM416PAM426y 63427y 59428y 54429y 46430y 37431y 23u432y  8433y360434y350435y344436y340437y339444y343445y351446y  0a447y 17448y 68rU449y 90450Zu451y  0479zy341R480y334DI481y340dI482y343I483y344484B490b492y342493y354494Zy  0r525y 69526zy 66U527y 69RPBM528y 66PM529y 64PM530M533b538y 65539y 68542y 69550y 70B551y 71553y 72555y 74r556y 87b557y 91558y107L559y121560y129561y135E562y140563y144564y145565y147567y148568y149569y151570y156u571y161572y170573y180574Zl575y  0604y219605y247606zy261DO607y262O608y259OB609y258O614y260615y263b616y264620B626b633B635y266637y267b643y268644y269649y270655C663c670C677c692C699c709C711y273712y275713Zy285d714y 76c715zy 73UM716y 76PM717y 69RPM718y 68PM723C730y 63c731y 59732y 54733y 52734y 49735y 48740y 49741y 50742y 52743y 53748C755c760y 52765y 38766y 10u767y353768Zy  0r780y270781zD782O783O784y263O785y258786y256788y255791y257792y260793y263796y262802y261813y262814y263815y262816Zy224d817zy180L818Zl819y  0826zy 67U827y 71RPCM828y 69PM829PM830M833y 63834y 32u835y  2c836Zy360r837y  0886y265887zy267DO888O889y263O916y265917y268918y270921y266922Zy247d923y192924y  0929zy 82U930y 79PM931y 73PCM932y 74PM933y 73M935y 74936y 73938y 72Rc940Zy  0ru1018y2701019zy278D1020y285O1021y284O1022y276O1023y2721024y2711026y2731027y2801028y289R1029y2971030y3071031y317I1032y3251033y3341034y340d1035y3421038y3431067y3421068y3391069y336D1070y3331071y3321075y3331076y3341077y337d1078y3411079y3461080y3511081y  01082y 101083y 26U1084y 39M1085y 45PM1086y 49PM1087y 50M1088y 531089y 541090y 571091y 631092y 711093y 721094y 701095y 63J1103y 60j1104y 551105y 531106y 491107y 431108y 391109y 381112y 391114y 401118y 381119y 311120y 22u1121y 111122y  31123y  01124y3571125y3541126y3511127y3501129y3491132y  01133y159Lr1134y156E1135y162E1136E1138C1142y1611143y1581144y1571145y155Uc1146y1521147y1481148y1441149y1411150y1401151y1451152y1491153y156u1154y1621155y174C1156Zy180l1158y  01161c1172C1175c1192y3601193zy340R1194y335DI1195y342dI1196y346I1199A1203a1205y3451206y3431207y3441208y  01209Zy 81r1210y  01234zy180L1235y162E1236y159E1237E1243y1601244y162C1245y1651246y1661247Zy  0l1251c1262C1266zy150L1267y1521268y1511269c1270y1501271y1511273y1551274y1601275Zy  0l1292y1491293zy143LU1294y146EM1295y151E1296y154E1297y156u1298y1571299y1601300y1631301y1661302y1711303y1801305y1791306y1681307y1621315y1691316Zy180l1317y  01319zy359R1320y342I1321y344I1322y341I1323y3361324y334D1325y333C1328y3341329y3351331y3361333d1335y353c1336Zy  0r1350C1354c1381y1751382zy156L1383y151UE1384y152E1385E1386y1541388y1561389y157uB1392y158A1393y1641394y1691395y1731396y180a1397Zlb1398y  01421zy351R1422y344I1423y342I1424y344I1428y3431430y3421440y3411442y3401443y3391444y3381446y3371450y3361452D1453y3341454y3321455y3341456Zy353rd1457zy158L1458y153UE1459y154E1460y153E1461y147M1462y1411463y129BM1464y115M1465y 98lM1466y 901467y 881468y 871475b1482y 881483y 901485Zu1486y  01495y2701496zD1497y284O1498O1499y279O1500y2761501A1503y2751504y2731505y2721509a1511y2731512y2751513y2781514y2831515y2851516y290R1517y2961518y2991519y3061520y3131521y3211522y3251523y3271525y3291526y343d1527y 221528Zy 59r1529y 521530zy 35R1531y 211532I1533y 221534y 26U1535y 36M1536y 39M1537y 40M1538y 41M1539y 441540y 48A1541y 531542y 571543y 611544y 631548a1562y 651563y 731564y 90r1565y114L1566y135E1567y146E1568y150E1569y1541570y157u1571y1591572y1601574y1611575y1601576y1611577y1621578y1631587C1592y1681593y1801594Zy  0lc1624zy179L1625y159E1626y160E1627y161E1645y1681646y1761647Zy  0l1651zy169L1652y154UE1653y161uE1654y162E1659y1601660y1591663y1621664y1631665Zy180l1666y  01669zy360R1670y345I1671y350I1672y349I1674y3481677y3491678JC1679y3471680y  01681Zrj1685c1701y1801702zy158L1703y153UE1704y154E1705y156E1706y157u1727y1561730U1731y1551733y1541734y1521735y1501736y148u1737Zy125l1738y  01739y 291740zy 11R1741y  51742y  01743y3541744y3421745y3311746Zy  0r1754zy162L1755y1591756y156E1757y157E1758y1581768y1571769y1561771Zy  0l1773zy  2R1774y360I1775y353I1776I1777y3511778y3491780y3591781Zy  0r1790C1848y1801849zL1850y1751853y174c1854y1781855Zy180l1856y  01880y1801881zy170L1882y1691884y1701885y1691915y1681916y1651917y1631918y1621924y1661927y1651928y1631938y1661939y1671943y1661949y1651950Zy170l1951y  01953y  61954C1955y  01962c1998y1801999zy165L2000y162E2001EC2002E2003y1652004y1752005Zy  0l2008c2041zR2042y357I2043y354I2044I2046y3512049Zy  0rC2056c2071zR2072y349I2073y342I2074I2075y3412076y3422077y351C2078Zy  0r2085c2129y1802130zy205L2131y237D2132y255lO2133y257O2134O2143C2146y259Ac2147y2632148y2652149y2662150y2672154a2158y2662243y2652244y2642249y2632250y2622251y2572252y2442253y227Ld2254Zy195l2255y  02258y 902262y 852263zU2264y 86M2265y 87PM2266y 86PM2267y 84M2268y 832272y 88C2273y 902274y1012275y1052276y1062279y107L2280y1122281y1162282y1172287y1182288y1222289y1252290y1302291y1342292y1362293y1382295y1392297c2299y1442300Zy  0lu2363y2702366zD2384Zy180d2385y  0
5Player 2                              060101100043170907F5F1BA9FFDA3FB1EA002F770E3043FFFFE456      

5Player 3                              02020220004CE2F2FFCF623FFB986FF5E5EA0012979                  

0
'''

SAMPLE_PLAYER_DATA = '''HPlayer 1                              10000010004F2EAFCFCEDFC45FF405CCBF0FFC72038                  
1Z101zy327R102y333103y338I104y341I105y344106y345108y346109y349110y354111y358112y359115y  0119y  6120Zy 90r121y  0128zRI129I130y360I131y354I132y346133y344142y345143y346148C150y345151y344152y350153y  2154Zy  0rc181y180182y166183zy162L184y160186y156187y153U188y155189y156u190y157191y159C192y163193y176194y182195Zy192l196y  0c213A221a242y 78243y 75244zy 83UM245PM246y 79PM247y 78M248y 77249y 76251A257a281y 69282Zy 73u283y  0298y237299y252300zy258DO301O302y252LO303y250A310y252311y253a312y255l313y256317y257318y258319y259321y260323y261324y263325y264326y266327y267328y269329y270331y267332Zy201d333y180334y  0352zR353y346I354y345I355y344I356y342357y339359C360y341361y342362y343363y344364c365y345366y347367y358368Zy 28r369y 90370y  0412y 57413zy 69RUPM414y 67PM415y 65PM416PAM426y 63427y 59428y 54429y 46430y 37431y 23u432y  8433y360434y350435y344436y340437y339444y343445y351446y  0a447y 17448y 68rU449y 90450Zu451y  0479zy341R480y334DI481y340dI482y343I483y344484B490b492y342493y354494Zy  0r525y 69526zy 66U527y 69RPBM528y 66PM529y 64PM530M533b538y 65539y 68542y 69550y 70B551y 71553y 72555y 74r556y 87b557y 91558y107L559y121560y129561y135E562y140563y144564y145565y147567y148568y149569y151570y156u571y161572y170573y180574Zl575y  0604y219605y247606zy261DO607y262O608y259OB609y258O614y260615y263b616y264620B626b633B635y266637y267b643y268644y269649y270655C663c670C677c692C699c709C711y273712y275713Zy285d714y 76c715zy 73UM716y 76PM717y 69RPM718y 68PM723C730y 63c731y 59732y 54733y 52734y 49735y 48740y 49741y 50742y 52743y 53748C755c760y 52765y 38766y 10u767y353768Zy  0r780y270781zD782O783O784y263O785y258786y256788y255791y257792y260793y263796y262802y261813y262814y263815y262816Zy224d817zy180L818Zl819y  0826zy 67U827y 71RPCM828y 69PM829PM830M833y 63834y 32u835y  2c836Zy360r837y  0886y265887zy267DO888O889y263O916y265917y268918y270921y266922Zy247d923y192924y  0929zy 82U930y 79PM931y 73PCM932y 74PM933y 73M935y 74936y 73938y 72Rc940Zy  0ru1018y2701019zy278D1020y285O1021y284O1022y276O1023y2721024y2711026y2731027y2801028y289R1029y2971030y3071031y317I1032y3251033y3341034y340d1035y3421038y3431067y3421068y3391069y336D1070y3331071y3321075y3331076y3341077y337d1078y3411079y3461080y3511081y  01082y 101083y 26U1084y 39M1085y 45PM1086y 49PM1087y 50M1088y 531089y 541090y 571091y 631092y 711093y 721094y 701095y 63J1103y 60j1104y 551105y 531106y 491107y 431108y 391109y 381112y 391114y 401118y 381119y 311120y 22u1121y 111122y  31123y  01124y3571125y3541126y3511127y3501129y3491132y  01133y159Lr1134y156E1135y162E1136E1138C1142y1611143y1581144y1571145y155Uc1146y1521147y1481148y1441149y1411150y1401151y1451152y1491153y156u1154y1621155y174C1156Zy180l1158y  01161c1172C1175c1192y3601193zy340R1194y335DI1195y342dI1196y346I1199A1203a1205y3451206y3431207y3441208y  01209Zy 81r1210y  01234zy180L1235y162E1236y159E1237E1243y1601244y162C1245y1651246y1661247Zy  0l1251c1262C1266zy150L1267y1521268y1511269c1270y1501271y1511273y1551274y1601275Zy  0l1292y1491293zy143LU1294y146EM1295y151E1296y154E1297y156u1298y1571299y1601300y1631301y1661302y1711303y1801305y1791306y1681307y1621315y1691316Zy180l1317y  01319zy359R1320y342I1321y344I1322y341I1323y3361324y334D1325y333C1328y3341329y3351331y3361333d1335y353c1336Zy  0r1350C1354c1381y1751382zy156L1383y151UE1384y152E1385E1386y1541388y1561389y157uB1392y158A1393y1641394y1691395y1731396y180a1397Zlb1398y  01421zy351R1422y344I1423y342I1424y344I1428y3431430y3421440y3411442y3401443y3391444y3381446y3371450y3361452D1453y3341454y3321455y3341456Zy353rd1457zy158L1458y153UE1459y154E1460y153E1461y147M1462y1411463y129BM1464y115M1465y 98lM1466y 901467y 881468y 871475b1482y 881483y 901485Zu1486y  01495y2701496zD1497y284O1498O1499y279O1500y2761501A1503y2751504y2731505y2721509a1511y2731512y2751513y2781514y2831515y2851516y290R1517y2961518y2991519y3061520y3131521y3211522y3251523y3271525y3291526y343d1527y 221528Zy 59r1529y 521530zy 35R1531y 211532I1533y 221534y 26U1535y 36M1536y 39M1537y 40M1538y 41M1539y 441540y 48A1541y 531542y 571543y 611544y 631548a1562y 651563y 731564y 90r1565y114L1566y135E1567y146E1568y150E1569y1541570y157u1571y1591572y1601574y1611575y1601576y1611577y1621578y1631587C1592y1681593y1801594Zy  0lc1624zy179L1625y159E1626y160E1627y161E1645y1681646y1761647Zy  0l1651zy169L1652y154UE1653y161uE1654y162E1659y1601660y1591663y1621664y1631665Zy180l1666y  01669zy360R1670y345I1671y350I1672y349I1674y3481677y3491678JC1679y3471680y  01681Zrj1685c1701y1801702zy158L1703y153UE1704y154E1705y156E1706y157u1727y1561730U1731y1551733y1541734y1521735y1501736y148u1737Zy125l1738y  01739y 291740zy 11R1741y  51742y  01743y3541744y3421745y3311746Zy  0r1754zy162L1755y1591756y156E1757y157E1758y1581768y1571769y1561771Zy  0l1773zy  2R1774y360I1775y353I1776I1777y3511778y3491780y3591781Zy  0r1790C1848y1801849zL1850y1751853y174c1854y1781855Zy180l1856y  01880y1801881zy170L1882y1691884y1701885y1691915y1681916y1651917y1631918y1621924y1661927y1651928y1631938y1661939y1671943y1661949y1651950Zy170l1951y  01953y  61954C1955y  01962c1998y1801999zy165L2000y162E2001EC2002E2003y1652004y1752005Zy  0l2008c2041zR2042y357I2043y354I2044I2046y3512049Zy  0rC2056c2071zR2072y349I2073y342I2074I2075y3412076y3422077y351C2078Zy  0r2085c2129y1802130zy205L2131y237D2132y255lO2133y257O2134O2143C2146y259Ac2147y2632148y2652149y2662150y2672154a2158y2662243y2652244y2642249y2632250y2622251y2572252y2442253y227Ld2254Zy195l2255y  02258y 902262y 852263zU2264y 86M2265y 87PM2266y 86PM2267y 84M2268y 832272y 88C2273y 902274y1012275y1052276y1062279y107L2280y1122281y1162282y1172287y1182288y1222289y1252290y1302291y1342292y1362293y1382295y1392297c2299y1442300Zy  0lu2363y2702366zD2384Zy180d2385y  0
'''


class TestFrameData:
    @pytest.fixture
    def lookup_table(self):
        return FrameData.get_lookup_table(PlayerData.get_frame_data(SAMPLE_PLAYER_DATA))

    @pytest.fixture
    def raw_lookup_table(self):
        return FrameData.get_lookup_table(PlayerData.get_frame_data(SAMPLE_PLAYER_DATA), raw=True)

    @pytest.fixture(params=list(range(1, 2385, 159)) + [9999])
    def frame_n(self, request):
        return request.param

    @pytest.fixture(params=list(range(1, 360, 15)))
    def angle_n(self, request):
        return request.param

    def test_convert_token_to_action(self):
        assert FrameData.convert_token_to_action('Z') == Action.ANGLES_ENABLED
        assert FrameData.convert_token_to_action('y327') == 327
        assert FrameData.convert_token_to_action('R') == Action.RIGHT_PRESS

    def test_convert_multiple_tokens_to_actions(self):
        assert FrameData.convert_multiple_tokens_to_actions(['Z']) == [Action.ANGLES_ENABLED]
        assert FrameData.convert_multiple_tokens_to_actions(['z', 'y327', 'R']) == [Action.ANGLES_DISABLED, 327, Action.RIGHT_PRESS]
        assert FrameData.convert_multiple_tokens_to_actions(['C']) == [Action.STRONG_PRESS]
        assert FrameData.convert_multiple_tokens_to_actions(['Z', 'y  0', 'r', 'c']) == [Action.ANGLES_ENABLED, 0, Action.RIGHT_RELEASE, Action.STRONG_RELEASE]
        assert FrameData.convert_multiple_tokens_to_actions(['z', 'y143', 'L', 'U']) == [Action.ANGLES_DISABLED, 143, Action.LEFT_PRESS, Action.UP_PRESS]
        assert FrameData.convert_multiple_tokens_to_actions(['y  0']) == [0]
        assert FrameData.convert_multiple_tokens_to_actions(['Z', 'y180', 'd']) == [Action.ANGLES_ENABLED, 180, Action.DOWN_RELEASE]
        assert FrameData.convert_multiple_tokens_to_actions(['z', 'D']) == [Action.ANGLES_DISABLED, Action.DOWN_PRESS]

    def test_split_frames_into_tokens(self):
        split_frames = FrameData.split_frames_into_tokens(PlayerData.get_frame_data(SAMPLE_PLAYER_DATA))
        assert split_frames[0] == ['1', 'Z']
        assert split_frames[1] == ['101', 'z', 'y327', 'R']
        assert split_frames[-2] == ['2384', 'Z', 'y180', 'd']
        assert split_frames[-1] == ['2385', 'y  0']

    def test_get_lookup_table(self, lookup_table):
        assert len(lookup_table.keys()) == 717
        assert lookup_table[1] == [Action.ANGLES_ENABLED]
        assert lookup_table[101] == [Action.ANGLES_DISABLED, 327, Action.RIGHT_PRESS]
        assert lookup_table[148] == [Action.STRONG_PRESS]
        assert lookup_table[154] == [Action.ANGLES_ENABLED, 0, Action.RIGHT_RELEASE, Action.STRONG_RELEASE]
        assert lookup_table[1293] == [Action.ANGLES_DISABLED, 143, Action.LEFT_PRESS, Action.UP_PRESS]
        assert lookup_table[2366] == [Action.ANGLES_DISABLED, Action.DOWN_PRESS]
        assert lookup_table[2384] == [Action.ANGLES_ENABLED, 180, Action.DOWN_RELEASE]
        assert lookup_table[2385] == [0]

    def test_get_lookup_table_raw(self, raw_lookup_table):
        assert len(raw_lookup_table.keys()) == 717
        assert raw_lookup_table[1] == ['Z']
        assert raw_lookup_table[101] == ['z', 'y327', 'R']
        assert raw_lookup_table[148] == ['C']
        assert raw_lookup_table[154] == ['Z', 'y  0', 'r', 'c']
        assert raw_lookup_table[1293] == ['z', 'y143', 'L', 'U']
        assert raw_lookup_table[2366] == ['z', 'D']
        assert raw_lookup_table[2384] == ['Z', 'y180', 'd']
        assert raw_lookup_table[2385] == ['y  0']

    def test_get_state_table(self):
        state_p1 = FrameData.get_state_table(PlayerData.get_frame_data(SAMPLE_PLAYER_DATA))
        state = [False]*18
        state[ActionType.ANGLES] = True
        assert state_p1[1] == state
        state[ActionType.ANGLES] = False
        state[ActionType.ANGLE_RIGHT] = True
        state[ActionType.ANGLE_DOWN] = True
        state[ActionType.RIGHT] = True
        assert state_p1[101] == state
        state[-4:] = [False]*4
        state[ActionType.ANGLE_RIGHT] = False
        state[ActionType.STRONG] = True
        assert state_p1[148] == state
        state[-4:] = [False]*4
        state[ActionType.ANGLES] = True
        state[ActionType.ANGLE_RIGHT] = True
        state[ActionType.RIGHT] = False
        state[ActionType.STRONG] = False
        assert state_p1[154] == state

    def test_snap_frame(self, lookup_table):
        assert FrameData.snap_frame(lookup_table, 1) == 1
        assert FrameData.snap_frame(lookup_table, 100) == 1
        assert FrameData.snap_frame(lookup_table, 101) == 101
        assert FrameData.snap_frame(lookup_table, 112) == 112
        assert FrameData.snap_frame(lookup_table, 114) == 112
        assert FrameData.snap_frame(lookup_table, 115) == 115
        assert FrameData.snap_frame(lookup_table, 118) == 115
        assert FrameData.snap_frame(lookup_table, 2385) == 2385
        assert FrameData.snap_frame(lookup_table, 9999) == 2385

    def test_snap_frame_error(self, lookup_table):
        with pytest.raises(ValueError): FrameData.snap_frame(lookup_table, -1)

    def test_snap_frame_transitive(self, raw_lookup_table):
        assert raw_lookup_table[FrameData.snap_frame(raw_lookup_table, 100)] == ['Z']
        assert raw_lookup_table[FrameData.snap_frame(raw_lookup_table, 101)] == ['z', 'y327', 'R']

    def test_snap_multiple_frames(self, lookup_table):
        snapped = FrameData.snap_multiple_frames(lookup_table, [1, 100, 101, 112, 114, 115, 118, 2385, 9999])
        assert snapped == [1, 1, 101, 112, 112, 115, 115, 2385, 2385]

    def test_snap_angle(self):
        assert FrameData.snap_angle(0) == 0
        assert FrameData.snap_angle(23) == 45
        assert FrameData.snap_angle(45) == 45
        assert FrameData.snap_angle(67) == 45
        assert FrameData.snap_angle(68) == 90
        assert FrameData.snap_angle(180) == 180
        assert FrameData.snap_angle(360) == 0

    def test_get_closest_frame(self, raw_lookup_table):
        assert FrameData.get_closest_action(raw_lookup_table, 100) == ['Z']
        assert FrameData.get_closest_action(raw_lookup_table, 101) == ['z', 'y327', 'R']

    def test_snap_angle_error(self):
        with pytest.raises(ValueError): FrameData.snap_angle(-1)
        with pytest.raises(ValueError): FrameData.snap_angle(361)

    def test_get_lookup_table_performance(self, benchmark):
        result = benchmark(FrameData.get_lookup_table, PlayerData.get_frame_data(ReplayData.get_player_data(SAMPLE_REPLAY_DATA)[0]))
        assert isinstance(result, dict)
        assert len(result.keys()) == 717
        assert result[1] == [Action.ANGLES_ENABLED]
        assert result[2385] == [0]

    def test_get_state_table_performance(self, benchmark):
        result = benchmark(FrameData.get_state_table, PlayerData.get_frame_data(ReplayData.get_player_data(SAMPLE_REPLAY_DATA)[0]))
        assert isinstance(result, dict)
        assert len(result.keys()) == 717
        assert isinstance(result[1], list)
        assert result[1][0] == False

    def test_snap_frame_performance(self, benchmark, lookup_table, frame_n):
        benchmark.pedantic(FrameData.snap_frame, args=(lookup_table, frame_n), iterations=1, rounds=1)

    def test_snap_angle_performance(self, benchmark, angle_n):
        benchmark.pedantic(FrameData.snap_angle, args=(angle_n,), iterations=1, rounds=1)


class TestPlayerData:
    def test_is_human(self):
        assert PlayerData.is_human(SAMPLE_PLAYER_DATA) == True
    
    def test_get_name(self):
        assert PlayerData.get_name(SAMPLE_PLAYER_DATA) == 'Player 1'

    def test_get_tag(self):
        assert PlayerData.get_tag(SAMPLE_PLAYER_DATA) == ''

    def test_get_character(self):
        assert PlayerData.get_character(SAMPLE_PLAYER_DATA) == Character.ORI

    def test_get_frame_data(self):
        actions_p1 = PlayerData.get_frame_data(SAMPLE_PLAYER_DATA)
        assert len(actions_p1) == 717
        assert actions_p1[0] == '1Z'
        assert actions_p1[1] == '101zy327R'
        assert actions_p1[24] == '148C'
        assert actions_p1[29] == '154Zy  0rc'
        assert actions_p1[394] == '1293zy143LU'
        assert actions_p1[714] == '2366zD'
        assert actions_p1[715] == '2384Zy180d'
        assert actions_p1[716] == '2385y  0'

    def test_get_frame_data_performance(self, benchmark):
        result = benchmark(PlayerData.get_frame_data, SAMPLE_PLAYER_DATA)
        assert len(result) == 717
        assert result[0] == '1Z'
        assert result[716] == '2385y  0'


class TestReplayData:
    @pytest.mark.skip
    def test_is_starred_true(self):
        pytest.fail('Test case not covered')

    def test_is_starred_false(self):
        assert ReplayData.is_starred(SAMPLE_REPLAY_DATA) == False

    def test_get_version(self):
        assert ReplayData.get_version(SAMPLE_REPLAY_DATA) == (1, 3, 5)

    def test_get_date(self):
        assert ReplayData.get_date(SAMPLE_REPLAY_DATA) == dt.datetime(
            year=2018, month=7, day=31,
            hour=21, minute=21, second=18)

    def test_get_name(self):
        assert ReplayData.get_name(SAMPLE_REPLAY_DATA) == 'SAMPLE REPLAY'

    def test_get_description(self):
        assert ReplayData.get_description(SAMPLE_REPLAY_DATA) == 'This is a replay I recorded to use as a sample in my replay parser.'

    def test_get_stage_type(self):
        assert ReplayData.get_stage_type(SAMPLE_REPLAY_DATA) == StageType.AETHER

    def test_get_stage(self):
        assert ReplayData.get_stage(SAMPLE_REPLAY_DATA) == Stage.SPIRIT_TREE

    def test_get_stock(self):
        assert ReplayData.get_stock(SAMPLE_REPLAY_DATA) == 1

    def test_get_time(self):
        assert ReplayData.get_time(SAMPLE_REPLAY_DATA) == 8

    def test_is_teams_enabled_true(self):
        assert ReplayData.is_teams_enabled(SAMPLE_REPLAY_DATA) == False
    
    @pytest.mark.skip
    def test_is_teams_enabled_false(self):
        pytest.fail('Test case not covered')

    def test_is_friendly_fire_enabled_true(self):
        assert ReplayData.is_friendly_fire_enabled(SAMPLE_REPLAY_DATA) == False

    @pytest.mark.skip
    def test_is_friendly_fire_enabled_false(self):
        pytest.fail('Test case not covered')

    @pytest.mark.skip
    def test_is_online_true(self):
        pytest.fail('Test case not covered')

    def test_is_online_false(self):
        assert ReplayData.is_online(SAMPLE_REPLAY_DATA) == False

    def test_get_player_data(self):
        players = ReplayData.get_player_data(SAMPLE_REPLAY_DATA)
        assert len(players) == 1
        assert players[0] == SAMPLE_PLAYER_DATA

    def test_get_frame_data_all_players(self):
        actions_all_players = ReplayData.get_frame_data_all_players(SAMPLE_REPLAY_DATA)
        assert len(actions_all_players) == 1
        actions_p1 = actions_all_players[0]
        assert len(actions_p1) == 717
        assert actions_p1[0] == '1Z'
        assert actions_p1[1] == '101zy327R'
        assert actions_p1[24] == '148C'
        assert actions_p1[29] == '154Zy  0rc'
        assert actions_p1[394] == '1293zy143LU'
        assert actions_p1[716] == '2385y  0'
        assert actions_p1[715] == '2384Zy180d'
        assert actions_p1[714] == '2366zD'

    def test_get_duration(self):
        assert ReplayData.get_duration(ReplayData.get_frame_data_all_players(SAMPLE_REPLAY_DATA)) == 2385

    def test_get_player_data_performance(self, benchmark):
        result = benchmark(ReplayData.get_player_data, SAMPLE_REPLAY_DATA)
        assert len(result) == 1
        assert result[0] == SAMPLE_PLAYER_DATA
