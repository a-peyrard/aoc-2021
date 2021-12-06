def get_bit_at(num: int, pos: int) -> int:
    return 1 if num & (1 << pos) > 0 else 0


def turn_on_bit_at(num: int, pos: int) -> int:
    return num | (1 << pos)
