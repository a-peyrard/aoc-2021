from typing import Iterable

from hamcrest import assert_that, equal_to

# noinspection PyProtectedMember
from aoc.day16.packet_decoder import sum_versions, DataFrame, _parse_packet, PacketType
from aoc.util.input import parse_input_file


class TestPacketDecoder:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> str:
        return next(lines.__iter__()).strip()

    def test_should_sum_versions_for_first_sample(self):
        # GIVEN
        packet = "8A004A801A8002F478"

        # WHEN
        res = sum_versions(packet)

        # THEN
        assert_that(res, equal_to(16))

    def test_should_sum_versions_for_second_sample(self):
        # GIVEN
        packet = "620080001611562C8802118E34"

        # WHEN
        res = sum_versions(packet)

        # THEN
        assert_that(res, equal_to(12))

    def test_should_sum_versions_for_third_sample(self):
        # GIVEN
        packet = "C0015000016115A2E0802F182340"

        # WHEN
        res = sum_versions(packet)

        # THEN
        assert_that(res, equal_to(23))

    def test_should_sum_versions_for_fourth_sample(self):
        # GIVEN
        packet = "A0016C880162017C3686B18A3D4780"

        # WHEN
        res = sum_versions(packet)

        # THEN
        assert_that(res, equal_to(31))

    def test_should_parse_literal_packet_with_multiple_sub_packets_for_value(self):
        # GIVEN
        data_frame = format(
            int("110100101111111000101000", 2), "x"
        ).upper()

        # WHEN
        packet, _ = _parse_packet(DataFrame(data_frame))

        # THEN
        assert_that(packet.version, equal_to(6))
        assert_that(packet.packet_type, equal_to(PacketType.literal))
        assert_that(packet.value, equal_to(2021))

    def test_should_sum_versions_for_input(self):
        # GIVEN
        packet = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestPacketDecoder._parse_input
        )

        # WHEN
        res = sum_versions(packet)

        # THEN
        assert_that(res, equal_to(967))


class TestDataFrame:
    def test_should_print_data_frame_in_binary_format(self):
        # GIVEN
        data_frame = DataFrame("8A004A801")

        # WHEN
        res = data_frame.print()

        # THEN
        assert_that(res, equal_to("100010100000000001001010100000000001"))

    def test_should_pop_bits_from_frame(self):
        # GIVEN
        data_frame = DataFrame("8A004A801")

        # WHEN
        version = data_frame.pop(3)
        rest = data_frame.print()

        # THEN
        assert_that(DataFrame.print_binary(version, 3), equal_to("100"))
        assert_that(rest, equal_to("010100000000001001010100000000001"))

    def test_should_pop_multiple_time_bits_from_frame(self):
        # GIVEN
        data_frame = DataFrame("8A004A801")

        # WHEN
        version = data_frame.pop(3)
        data_type = data_frame.pop(3)
        rest = data_frame.print()

        # THEN
        assert_that(DataFrame.print_binary(version, 3), equal_to("100"))
        assert_that(DataFrame.print_binary(data_type, 3), equal_to("010"))
        assert_that(rest, equal_to("100000000001001010100000000001"))

    def test_should_exhaust_frame(self):
        # GIVEN
        data_frame = DataFrame("8A004A801")

        # WHEN
        version = data_frame.pop(3)
        data_type = data_frame.pop(3)
        length = data_frame.pop(11)
        foo = data_frame.pop(8)
        bar = data_frame.pop(11)
        rest = data_frame.print()

        # THEN
        assert_that(DataFrame.print_binary(version, 3), equal_to("100"))
        assert_that(DataFrame.print_binary(data_type, 3), equal_to("010"))
        assert_that(DataFrame.print_binary(length, 11), equal_to("10000000000"))
        assert_that(DataFrame.print_binary(foo, 8), equal_to("10010101"))
        assert_that(DataFrame.print_binary(bar, 11), equal_to("00000000001"))
        assert_that(rest, equal_to(""))
