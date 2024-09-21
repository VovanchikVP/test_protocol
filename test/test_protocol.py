import os
from pathlib import Path
from src.test_protocol import TestProtocol

LINES = [
    b'\x00\x01869586748696585\xfa\x12\xedfc.VB\xaa`EB',
    b'\x01\x01869586748696585\t\x15\xedf\x1b/VBB`EB',
    b'\x02\x02869586748696585+\x15\xedf\x9e/VB\xbe_EB\x03',
]

RESULTS = [
    {'datetime': 1726812922, 'imei': '869586748696585', 'lat': 53.5452995300293, 'lon': 49.344398498535156, 'num_pack': 0, 'type_message': 1},
    {'datetime': 1726813449, 'imei': '869586748696585', 'lat': 53.54600143432617, 'lon': 49.34400177001953, 'num_pack': 1, 'type_message': 1},
    {'code_msg': 3, 'datetime': 1726813483, 'imei': '869586748696585', 'lat': 53.54650115966797, 'lon': 49.34349822998047, 'num_pack': 2, 'type_message': 2},
]

BASE_PATH = os.path.join(Path(__file__).absolute().parents[1], Path("test/input_data.txt"))


def _comparison_results(position: int, data: dict) -> None:
    assert not set(data.keys()) - set(RESULTS[position].keys()), f"Строка {position} не соответствуют ключи"
    assert not set(RESULTS[position].keys() - data.keys()), f"Строка {position} не соответствуют ключи"
    assert not set(data.values()) - set(RESULTS[position].values()), f"Строка {position} не соответствуют значения"
    assert not set(RESULTS[position].values()) - set(data.values()), f"Строка {position} не соответствуют значения"


def test_pars_lines():
    for position, line in enumerate(LINES):
        data = TestProtocol.parse(line)
        _comparison_results(position, data)


def test_pars_file():
    with open(BASE_PATH, "rb") as f:
        for position, line in enumerate(f.readlines()):
            data = TestProtocol.parse(line.strip())
            _comparison_results(position, data)
