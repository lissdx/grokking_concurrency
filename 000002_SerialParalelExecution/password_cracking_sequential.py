import time
import math
import hashlib
import typing as T

ChunkRange = T.Tuple[int, int]


def get_combinations(*, cLength: int, min_number: int = 0) -> T.List[str]:
    combinations = []
    max_number = int(math.pow(10, cLength) - 1)

    for i in range(min_number, max_number + 1):
        str_num = str(i)
        zeros = "0" * (cLength - len(str_num))
        combinations.append("".join((zeros, str_num)))

    return combinations


def get_crypto_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str, possible_password: str) -> bool:
    actual_crypto_hash = get_crypto_hash(possible_password)

    return expected_crypto_hash == actual_crypto_hash


def crack_password(cryptoHash: str, crackLength: int) -> None:
    print("Processing number combinations sequentially")
    start_time = time.perf_counter()
    combinations = get_combinations(cLength=crackLength)

    for combination in combinations:
        if check_password(cryptoHash, combination):
            print(f"PASSWORD CRACKED: {combination}")
            break

    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")


def get_chunks(num_ranges: int, chunkLength: int) -> T.Iterator[ChunkRange]:
    max_number = int(math.pow(10, chunkLength) - 1)

    chunk_starts = [int(max_number / num_ranges * i) for i in range(num_ranges)]
    chunk_ends = [start_point for start_point in chunk_starts[1:]] + [max_number]

    return zip(chunk_starts, chunk_ends)


if __name__ == "__main__":
    crypto_hash = \
        "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    length = 8
    crack_password(crypto_hash, length)
