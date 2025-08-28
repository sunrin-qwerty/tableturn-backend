import hmac
import hashlib
import time
import base64
import struct
import uuid


def generate_room_code_with_timer(room_uuid: str, interval: int = 30, digits: int = 6):
    current_time = int(time.time())
    counter = current_time // interval
    elapsed_in_interval = current_time % interval
    seconds_left = interval - elapsed_in_interval

    key = base64.b32encode(room_uuid.encode())
    uuid_bytes = uuid.UUID(room_uuid).bytes
    counter_bytes = struct.pack(">Q", counter)
    msg = uuid_bytes + counter_bytes

    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    binary = (
        ((hmac_hash[offset] & 0x7F) << 24)
        | ((hmac_hash[offset + 1] & 0xFF) << 16)
        | ((hmac_hash[offset + 2] & 0xFF) << 8)
        | (hmac_hash[offset + 3] & 0xFF)
    )
    code = binary % (10**digits)
    code_str = str(code).zfill(digits)

    is_valid = seconds_left > 0

    return code_str, seconds_left, is_valid


# 사용 예시
if __name__ == "__main__":
    room_uuid = "985a4868-cbb6-42e3-8275-17db3f2dd639"
    code, remain_seconds, valid = generate_room_code_with_timer(room_uuid)
    print(f"UUID: {room_uuid}")
    print(f"생성된 방 코드: {code}")
    print(f"남은 시간(초): {remain_seconds}")
    print(f"코드 유효 여부: {valid}")
