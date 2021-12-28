from typing import List, Iterable

import pytest
from hamcrest import assert_that, equal_to, contains_inanyorder

from aoc.day19.beacon_scanner import Coordinate, find_scanner, find_beacon_coordinates, \
    max_manhattan_distance
from aoc.util.input import parse_input_file


class TestBeaconScanner:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> List[List[Coordinate]]:
        scanners = []
        scanner = []
        for line in lines:
            line = line.strip()
            if not line:
                scanners.append(scanner)
                scanner = []
            elif not line.startswith("---"):
                x, y, z = line.split(",")
                scanner.append(Coordinate(int(x), int(y), int(z)))

        scanners.append(scanner)

        return scanners

    def test_should_find_scanner_2_position(self):
        # GIVEN
        scanners = TestBeaconScanner._parse_input(
            lines="""--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390""".splitlines(keepends=True)
        )

        # WHEN
        _, scanner1_coord = find_scanner(
            scanners[0],
            scanners[1],
            number_of_beacons=12
        )

        # THEN
        assert_that(scanner1_coord, equal_to(Coordinate(68, -1246, -43)))

    @pytest.mark.slow
    def test_should_find_beacon_coordinates_for_given_sample(self):
        # GIVEN
        scanners = TestBeaconScanner._parse_input(
            lines="""--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""".splitlines(keepends=True)
        )

        # WHEN
        beacons, _ = find_beacon_coordinates(scanners)

        # THEN
        # noinspection PyTypeChecker
        assert_that(beacons, contains_inanyorder(
            Coordinate(-892, 524, 684),
            Coordinate(-876, 649, 763),
            Coordinate(-838, 591, 734),
            Coordinate(-789, 900, -551),
            Coordinate(-739, -1745, 668),
            Coordinate(-706, -3180, -659),
            Coordinate(-697, -3072, -689),
            Coordinate(-689, 845, -530),
            Coordinate(-687, -1600, 576),
            Coordinate(-661, -816, -575),
            Coordinate(-654, -3158, -753),
            Coordinate(-635, -1737, 486),
            Coordinate(-631, -672, 1502),
            Coordinate(-624, -1620, 1868),
            Coordinate(-620, -3212, 371),
            Coordinate(-618, -824, -621),
            Coordinate(-612, -1695, 1788),
            Coordinate(-601, -1648, -643),
            Coordinate(-584, 868, -557),
            Coordinate(-537, -823, -458),
            Coordinate(-532, -1715, 1894),
            Coordinate(-518, -1681, -600),
            Coordinate(-499, -1607, -770),
            Coordinate(-485, -357, 347),
            Coordinate(-470, -3283, 303),
            Coordinate(-456, -621, 1527),
            Coordinate(-447, -329, 318),
            Coordinate(-430, -3130, 366),
            Coordinate(-413, -627, 1469),
            Coordinate(-345, -311, 381),
            Coordinate(-36, -1284, 1171),
            Coordinate(-27, -1108, -65),
            Coordinate(7, -33, -71),
            Coordinate(12, -2351, -103),
            Coordinate(26, -1119, 1091),
            Coordinate(346, -2985, 342),
            Coordinate(366, -3059, 397),
            Coordinate(377, -2827, 367),
            Coordinate(390, -675, -793),
            Coordinate(396, -1931, -563),
            Coordinate(404, -588, -901),
            Coordinate(408, -1815, 803),
            Coordinate(423, -701, 434),
            Coordinate(432, -2009, 850),
            Coordinate(443, 580, 662),
            Coordinate(455, 729, 728),
            Coordinate(456, -540, 1869),
            Coordinate(459, -707, 401),
            Coordinate(465, -695, 1988),
            Coordinate(474, 580, 667),
            Coordinate(496, -1584, 1900),
            Coordinate(497, -1838, -617),
            Coordinate(527, -524, 1933),
            Coordinate(528, -643, 409),
            Coordinate(534, -1912, 768),
            Coordinate(544, -627, -890),
            Coordinate(553, 345, -567),
            Coordinate(564, 392, -477),
            Coordinate(568, -2007, -577),
            Coordinate(605, -1665, 1952),
            Coordinate(612, -1593, 1893),
            Coordinate(630, 319, -379),
            Coordinate(686, -3108, -505),
            Coordinate(776, -3184, -501),
            Coordinate(846, -3110, -434),
            Coordinate(1135, -1161, 1235),
            Coordinate(1243, -1093, 1063),
            Coordinate(1660, -552, 429),
            Coordinate(1693, -557, 386),
            Coordinate(1735, -437, 1738),
            Coordinate(1749, -1800, 1813),
            Coordinate(1772, -405, 1572),
            Coordinate(1776, -675, 371),
            Coordinate(1779, -442, 1789),
            Coordinate(1780, -1548, 337),
            Coordinate(1786, -1538, 337),
            Coordinate(1847, -1591, 415),
            Coordinate(1889, -1729, 1762),
            Coordinate(1994, -1805, 1792)
        ))

    @pytest.mark.slow
    def test_should_find_solutions_for_input(self):
        # GIVEN
        scanners = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestBeaconScanner._parse_input
        )

        # WHEN part1
        beacons, scanner_coordinates = find_beacon_coordinates(scanners)

        # THEN
        assert_that(len(beacons), equal_to(385))

        # WHEN part2
        max_distance = max_manhattan_distance(scanner_coordinates)

        # THEN
        assert_that(max_distance, equal_to(10707))
