from typing import Union
from src.struc2 import Struct, Tag, LittleEndian


class StandardPack(Struct):
    num_pack: Tag[int, "u8"]
    type_message: Tag[int, "u8"]
    imei: Tag[bytes, 15, "cstring"]
    datetime: Tag[int, LittleEndian, 'u32']
    lat: Tag[float, LittleEndian, "f32"]
    lon: Tag[float, LittleEndian, "f32"]


class ExtendedPack(Struct):
    num_pack: Tag[int, "u8"]
    type_message: Tag[int, "u8"]
    imei: Tag[bytes, 15, "cstring"]
    datetime: Tag[int, LittleEndian, 'u32']
    lat: Tag[float, LittleEndian, "f32"]
    lon: Tag[float, LittleEndian, "f32"]
    code_msg: Tag[int, "u8"]


class TestProtocol:

    TYPE_MESSAGE = {
        1: StandardPack,
        2: ExtendedPack,
    }

    @staticmethod
    def parse(data: bytes) -> dict:
        """Парсинг byte строки"""
        message = StandardPack.unpack_b(data)
        type_message = TestProtocol.TYPE_MESSAGE.get(message.type_message)
        if type_message is not None and not isinstance(message, type_message):
            message = ExtendedPack.unpack_b(data)
        return TestProtocol._create_result(message)

    @staticmethod
    def _create_result(message: Union[StandardPack, ExtendedPack]) -> dict:
        """Формирование результата"""
        result = {}
        for key, value in message.__dict__.items():
            if isinstance(value, bytes):
                value = value.decode()
            result[key] = value
        return result
