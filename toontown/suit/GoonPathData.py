from panda3d.core import *
from panda3d.direct import *
from toontown.toonbase import ToontownGlobals
taskZoneId2pathId = {ToontownGlobals.SellbotFactoryInt: 'sellbotFactory',
 ToontownGlobals.CashbotMintIntA: 'cashbotMint',
 ToontownGlobals.CashbotMintIntB: 'cashbotMint',
 ToontownGlobals.CashbotMintIntC: 'cashbotMint',
 ToontownGlobals.LawbotOfficeInt: 'lawOfficeStage',
 ToontownGlobals.LawbotStageIntA: 'lawOfficeStage',
 ToontownGlobals.LawbotStageIntB: 'lawOfficeStage',
 ToontownGlobals.LawbotStageIntC: 'lawOfficeStage',
 ToontownGlobals.LawbotStageIntD: 'lawOfficeStage'}
Paths = {'sellbotFactory': {0: [Vec3(10.0, 0.0, 0.0),
                        Vec3(10.0, 10.0, 0.0),
                        Vec3(-10.0, 10.0, 0.0),
                        Vec3(-10.0, 0.0, 0.0)],
                    1: [Vec3(10.0, 5.0, 0.0), Vec3(10.0, 0.0, 0.0), Vec3(-10.0, -5.0, 0.0)],
                    2: [Vec3(-48.31, -0.001, 0),
                        Vec3(-48.0, -3.709, 0),
                        Vec3(35.041, -3.27, 0),
                        Vec3(34.751, -91.376, 0),
                        Vec3(39.869, -91.248, 0),
                        Vec3(39.93, -0.022, 0)],
                    3: [Vec3(-47.9110107422, -6.86798095703, 0.0),
                        Vec3(27.691986084, -5.68200683594, 0.0),
                        Vec3(34.049987793, 3.55303955078, 0.0),
                        Vec3(-39.983001709, 3.68499755859, 0.0)],
                    4: [Vec3(3.5649, 35.397, 0),
                        Vec3(-5.335, 36.067, 0),
                        Vec3(-4.605, -69.67, 0),
                        Vec3(17.815, -70.577, 0),
                        Vec3(17.4979, -50.997, 0),
                        Vec3(3.479, -46.775, 0)],
                    5: [Vec3(-2.993, -21.085, 0),
                        Vec3(5.209, -20.966, 0),
                        Vec3(2.164, 74.742, 0),
                        Vec3(-50.439, 78.55, 0),
                        Vec3(-52.042, 58.831, 0),
                        Vec3(-3.549, 57.295, 0)],
                    6: [Vec3(31.627, 2.093, 0.0), Vec3(4, 43, 0)],
                    7: [Vec3(34.627, 2.093, 0.0), Vec3(32, 43, 0)],
                    8: [Vec3(64.0, 43.0, 0.0), Vec3(59.5, 1.8, 0.0)],
                    9: [Vec3(84.0, 43.0, 0.0), Vec3(93.0, 25.0, 0.0), Vec3(66.0, 2.0, 0.0)],
                    10: [Vec3(85.0, 43.0, 0.0),
                         Vec3(66.0, 47.0, 0.0),
                         Vec3(53.0, 49.0, 0.0),
                         Vec3(71.0, 22.0, 0.0)],
                    11: [Vec3(63.0, 43.0, 0.0), Vec3(33.0, 47.0, 0.0)],
                    12: [Vec3(10.5139980316, 73.4393844604, 0.0), Vec3(-10.0053958893, 72.9239883423, 0.0), Vec3(5.55112314224, 90.2847213745, 0.0)],
                    13: [Vec3(-2.62728261948, 50.5329399109, 0.0), Vec3(-2.21770620346, 3.07684659958, 0.0)],
                    14: [Vec3(-15.9598636627, -15.0503959656, 0.0),
                         Vec3(8.35170555115, -17.5856513977, 0.0),
                         Vec3(8.34984397888, 3.9258685112, 0.0),
                         Vec3(-11.5888309479, 7.29379606247, 0.0)],
                    15: [Vec3(-25.7975006104, 18.4752807617, 0.0), Vec3(12.6321563721, 19.1084594727, 0.0), Vec3(24.8442764282, -4.62582397461, 0.0)],
                    16: [Vec3(6.70755004883, -4.16766357422, 0.0),
                         Vec3(-24.5565567017, -6.02560424805, 0.0),
                         Vec3(-24.4623031616, 15.6810913086, 0.0),
                         Vec3(3.93852233887, 17.1640014648, 0.0)],
                    17: [Vec3(0.474000930786, -29.1558818817, 0.0),
                         Vec3(0.460096359253, -16.5713024139, 0.0),
                         Vec3(27.9419631958, -16.0025310516, 0.0),
                         Vec3(28.3607826233, -38.4133338928, 0.0),
                         Vec3(27.2721481323, 0.622072696686, 0.0),
                         Vec3(-29.8864364624, 2.13151788712, 0.0),
                         Vec3(-28.907831192, -38.875164032, 0.0),
                         Vec3(-26.5185241699, -16.1851940155, 0.0),
                         Vec3(0.0833129882813, -16.7483196259, 0.0)],
                    18: [Vec3(-37.6936645508, 4.92616510391, 0.0),
                         Vec3(-6.09254932404, 3.79619073868, 0.0),
                         Vec3(-5.81788635254, 16.4960193634, 0.0),
                         Vec3(6.79872131348, 17.3943042755, 0.0),
                         Vec3(6.47452545166, 6.80963373184, 0.0),
                         Vec3(29.4301567078, 4.76448297501, 0.0)],
                    19: [Vec3(-11.6953277588, -13.8257198334, -0.00400207517669),
                         Vec3(-26.5939941406, -38.6423110962, -0.00400207517669),
                         Vec3(-12.9963378906, -54.1221084595, -0.00400207517669),
                         Vec3(5.45291900635, -50.0818252563, -0.00400207517669),
                         Vec3(0.500541687012, -27.6731319427, -0.00400207517669),
                         Vec3(10.6271972656, -16.9095211029, -0.00400207517669),
                         Vec3(3.95051574707, -11.6894283295, -0.00400207517669)],
                    20: [Vec3(1.44152832031, -18.6059322357, -0.00400207517669),
                         Vec3(-0.327140808105, -38.2261734009, -0.00400207517669),
                         Vec3(19.4757766724, -20.1440181732, -0.00400207517669),
                         Vec3(-13.617980957, -38.8843765259, -0.00400207517669),
                         Vec3(9.44762420654, -28.4113521576, -0.00400207517669)],
                    21: [Vec3(26.8655929565, -13.403295517, -0.00400207517669),
                         Vec3(32.0896224976, -27.145483017, -0.00400207517669),
                         Vec3(23.4544830322, -40.3218765259, -0.00400207517669),
                         Vec3(14.4268798828, -42.4280166626, -0.00400207517669),
                         Vec3(6.38285827637, -40.3579483032, -0.00400207517669),
                         Vec3(-2.16972351074, -26.8708248138, -0.00400207517669),
                         Vec3(-3.16332244873, -17.7787837982, -0.00400207517669),
                         Vec3(-3.16332244873, -17.7787837982, -0.00400207517669),
                         Vec3(2.0150680542, -5.54251718521, -0.00400207517669),
                         Vec3(7.65352630615, -5.11417245865, -0.00400207517669)],
                    22: [Vec3(-4.81932353973, 4.0960521698, 0.0),
                         Vec3(-37.2935218811, -35.963394165, 0.0),
                         Vec3(-32.3968849182, -49.8670196533, 0.0),
                         Vec3(-52.6336708069, -33.5889434814, 0.0),
                         Vec3(-53.0538520813, -21.5930957794, 0.0),
                         Vec3(-44.2506980896, -27.3775806427, 0.0),
                         Vec3(-1.58745121956, 3.91203117371, 0.0)],
                    23: [Vec3(5.80584430695, 1.62095463276, 0.0),
                         Vec3(-10.3068342209, -10.9403858185, 0.0),
                         Vec3(-27.9555549622, 11.9806346893, 0.0),
                         Vec3(-2.36316990852, -15.246049881, 0.0),
                         Vec3(-12.8535642624, -3.13337898254, 0.0)],
                    24: [Vec3(-12.7202939987, 15.884016037, 0.0), Vec3(16.7396354675, -14.0337085724, 0.0)],
                    25: [Vec3(-17.7801113129, -8.74084472656, 0.0), Vec3(-13.1200618744, -9.26202392578, -0.0)],
                    26: [Vec3(8.624584198, -10.9699707031, 0.0), Vec3(3.29245567322, -2.59405517578, 0.0)],
                    27: [Vec3(12.3031358719, 7.98439788818, 0.0), Vec3(-13.3801307678, 7.98439788818, 0.0)],
                    28: [Vec3(-32.1953697205, -85.9077148438, 0.0),
                         Vec3(-33.518032074, -60.6316223145, 0.0),
                         Vec3(-25.2015018463, -34.200378418, 0.0),
                         Vec3(-0.624415278435, -24.7206726074, 0.0)],
                    29: [Vec3(2.76529407501, -19.7032775879, 0.0),
                         Vec3(12.5924119949, -5.15737915039, 0.0),
                         Vec3(1.32620728016, 16.3902587891, 0.0),
                         Vec3(-13.4380140305, 18.5373535156, 0.0),
                         Vec3(-9.65627574921, -6.18496704102, 0.0),
                         Vec3(-24.4610538483, -31.9492492676, 0.0),
                         Vec3(-14.1554517746, -43.6148376465, 0.0)],
                    30: [Vec3(-0.175471186638, 24.0636901855, 0.0),
                         Vec3(-18.316400528, 61.1733856201, 0.0),
                         Vec3(-34.2972984314, 58.8515930176, 0.0),
                         Vec3(-18.7033634186, 27.5550231934, 0.0)],
                    31: [Vec3(25.8017997742, 73.792678833, 0.0), Vec3(11.0946779251, 51.4213256836, 0.0), Vec3(31.6651115417, 43.7239074707, 0.0)],
                    32: [Vec3(4.61576557159, 31.6040344238, 0.0),
                         Vec3(-10.1993589401, -7.03125, 0.0),
                         Vec3(-4.72947978973, -29.3165893555, 0.0),
                         Vec3(22.23179245, -28.7750854492, 0.0),
                         Vec3(11.0534486771, 0.391784667969, 0.0),
                         Vec3(18.2302970886, 28.4787597656, 0.0)],
                    33: [Vec3(8.04011249542, -51.311706543, 0.0),
                         Vec3(25.7791862488, -46.4603881836, 0.0),
                         Vec3(42.3690605164, -57.4282226563, 0.0),
                         Vec3(34.1978569031, -77.1849365234, 0.0)],
                    34: [Point3(2.75689697266, -21.3427124023, 0.0), Point3(2.78796386719, 37.0751342773, 0.000232696533203)],
                    35: [Point3(7.67395019531, 40.565612793, -0.000492095947266), Point3(78.0889282227, 39.3659667969, -0.00810623168945)],
                    36: [Point3(98.1296081543, 38.8174743652, -0.0102634429932),
                         Point3(104.098999023, 38.9267272949, -0.0109195709229),
                         Point3(105.774627686, 243.011169434, -0.0125999450684),
                         Point3(100.351745605, 242.852386475, -0.0125999450684)],
                    37: [Point3(152.121673584, 222.440261841, -5.0125999450684),
                         Point3(249.456481934, 223.478790283, -5.01259994507),
                         Point3(247.701660156, 233.899627686, -5.01259994507),
                         Point3(247.01550293, 224.162445068, -5.01259994507)],
                    38: [Point3(-1.65826416016, 25.0982055664, 0.025),
                         Point3(-1.44326782227, 9.02752685547, 0.025),
                         Point3(-8.76708984375, 11.2831420898, 0.025),
                         Point3(11.4426574707, 7.11584472656, 0.025),
                         Point3(2.77236938477, 7.02355957031, 0.025)],
                    39: [Point3(-3.69488525391, -1.89245605469, 0.025),
                         Point3(-5.73229980469, -9.62658691406, 0.025),
                         Point3(4.14199829102, -10.7971191406, 0.025),
                         Point3(7.77349853516, 1.58245849609, 0.025)],
                    40: [Point3(1.67153930664, 18.4436645508, 0.025), Point3(-7.59463500977, 18.5286254883, 0.025)],
                    41: [Point3(0.726699829102, -48.1898803711, -4.99999809265),
                         Point3(0.787185668945, -74.4460754395, -4.99999809265),
                         Point3(39.1846923828, -76.5356445313, -4.99999809265),
                         Point3(0.787185668945, -74.4460754395, -4.99999809265)],
                    42: [Vec3(6.0, -6.0, 0.0),
                         Vec3(6.0, 6.0, 0.0),
                         Vec3(-6.0, 6.0, 0.0),
                         Vec3(-6.0, -6.0, 0.0)]},
 'cashbotMint': {28: [Vec3(-32.1953697205, -85.9077148438, 0.0),
                      Vec3(-33.518032074, -60.6316223145, 0.0),
                      Vec3(-25.2015018463, -34.200378418, 0.0),
                      Vec3(-0.624415278435, -24.7206726074, 0.0)],
                 29: [Vec3(2.76529407501, -19.7032775879, 0.0),
                      Vec3(12.5924119949, -5.15737915039, 0.0),
                      Vec3(1.32620728016, 16.3902587891, 0.0),
                      Vec3(-13.4380140305, 18.5373535156, 0.0),
                      Vec3(-9.65627574921, -6.18496704102, 0.0),
                      Vec3(-24.4610538483, -31.9492492676, 0.0),
                      Vec3(-14.1554517746, -43.6148376465, 0.0)],
                 30: [Vec3(-0.175471186638, 24.0636901855, 0.0),
                      Vec3(-18.316400528, 61.1733856201, 0.0),
                      Vec3(-34.2972984314, 58.8515930176, 0.0),
                      Vec3(-18.7033634186, 27.5550231934, 0.0)],
                 0: [Vec3(-5, 0.0, 0.0),
                     Vec3(-5, 10.0, 0.0),
                     Vec3(5.0, 10.0, 0.0),
                     Vec3(5.0, 0.0, 0.0)],
                 1: [Vec3(0.0, 0.0, 0.0), Vec3(-5.77, 10.0, 0.0), Vec3(5.77, 10.0, 0.0)],
                 2: [Vec3(-5.77, 10.0, 0.0),
                     Vec3(5.77, 10.0, 0.0),
                     Vec3(-5.77, -10.0, 0.0),
                     Vec3(5.77, -10.0, 0.0)],
                 3: [Vec3(-10, 0, 0), Vec3(10, 0, 0)]},
 'lawOfficeStage': {28: [Vec3(-32.1953697205, -85.9077148438, 0.0),
                         Vec3(-33.518032074, -60.6316223145, 0.0),
                         Vec3(-25.2015018463, -34.200378418, 0.0),
                         Vec3(-0.624415278435, -24.7206726074, 0.0)],
                    29: [Vec3(2.76529407501, -19.7032775879, 0.0),
                         Vec3(12.5924119949, -5.15737915039, 0.0),
                         Vec3(1.32620728016, 16.3902587891, 0.0),
                         Vec3(-13.4380140305, 18.5373535156, 0.0),
                         Vec3(-9.65627574921, -6.18496704102, 0.0),
                         Vec3(-24.4610538483, -31.9492492676, 0.0),
                         Vec3(-14.1554517746, -43.6148376465, 0.0)],
                    30: [Vec3(-0.175471186638, 24.0636901855, 0.0),
                         Vec3(-18.316400528, 61.1733856201, 0.0),
                         Vec3(-34.2972984314, 58.8515930176, 0.0),
                         Vec3(-18.7033634186, 27.5550231934, 0.0)],
                    0: [Vec3(-5, 0.0, 0.0),
                        Vec3(-5, 10.0, 0.0),
                        Vec3(5.0, 10.0, 0.0),
                        Vec3(5.0, 0.0, 0.0)],
                    1: [Vec3(0.0, 0.0, 0.0), Vec3(-5.77, 10.0, 0.0), Vec3(5.77, 10.0, 0.0)],
                    2: [Vec3(-5.77, 10.0, 0.0),
                        Vec3(5.77, 10.0, 0.0),
                        Vec3(-5.77, -10.0, 0.0),
                        Vec3(5.77, -10.0, 0.0)],
                    3: [Vec3(-10, 0, 0), Vec3(10, 0, 0)]}}
