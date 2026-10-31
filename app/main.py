import json
import os
import regex
import sys
from collections import Counter

GPT2_PATTERN = r"'(?:[sdmt]|ll|ve|re)| ?\p{L}++| ?\p{N}++| ?[^\s\p{L}\p{N}]++|\s++$|\s+(?!\S)|\s"
COMPILED_PATTERN = regex.compile(GPT2_PATTERN)

def top_pair(ids):
    counts = Counter()
    first_seen = {}

    for i in range(len(ids) - 1):
        pair = (ids[i], ids[i + 1])
        counts[pair] += 1
        if pair not in first_seen:
            first_seen[pair] = i

    best_pair = None
    best_count = 0
    for pair, count in counts.items():
        if count > best_count or (count == best_count and first_seen[pair] < first_seen[best_pair]):
            best_pair = pair
            best_count = count

    return best_pair

def merge(ids, pair, new_id):
    result = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            result.append(new_id)
            i += 2
        else:
            result.append(ids[i])
            i += 1

    return result

def train(text, num_merges):
    ids = list(text.encode("utf-8"))
    merges = []

    for n in range(num_merges):
        pair = top_pair(ids)
        new_id = 256 + n
        ids = merge(ids, pair, new_id)
        merges.append(list(pair))

    return merges

def encode_chunk(text, ranks):
    ids = list(text.encode("utf-8"))

    while len(ids) >= 2:
        # neighbouring pair with the lowest rank
        best_pair = None
        best_rank = None
        for pair in zip(ids, ids[1:]):
            if pair in ranks:
                if best_rank is None or ranks[pair] < best_rank:
                    best_pair = pair
                    best_rank = ranks[pair]

        # nothing left to merge
        if best_pair is None:
            break

        ids = merge(ids, best_pair, 256 + best_rank)

    return ids

def encode(text, merges, pretokenize):
    ids = list(text.encode("utf-8"))
    ranks = {}

    for i, pair in enumerate(merges):
        ranks[(pair[0], pair[1])] = i

    if pretokenize == "gpt2":
        chunks = COMPILED_PATTERN.findall(text)
    else:
        chunks = [text]

    ids = []
    for chunk in chunks:
        ids.extend(encode_chunk(chunk, ranks))
    return ids
    

def decode(ids, merges):
    # vocabulary id -> bytes
    vocabulary = {}
    for i in range(256):
        vocabulary[i] = bytes([i])
    for i, pair in enumerate(merges):
        vocabulary[256 + i] = vocabulary[pair[0]] + vocabulary[pair[1]]

    data = b"".join(vocabulary[token] for token in ids)

    if not data:
        return ""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")

def bytes_to_unicode():
    printable = (list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256)))
    table = {}
    for b in printable:
        table[b] = chr(b)

    extra = 0
    for b in range(256):
        if b not in table:
            table[b] = chr(256 + extra)
            extra += 1
    return table

def load_vocab(directory):
    with open(os.path.join(directory, "vocab.json"), "r", encoding="utf-8") as f:
        vocab = json.load(f)

    ranks = {}
    with open(os.path.join(directory, "merges.txt"), "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    rank = 0
    for line_number, line in enumerate(lines):
        if line_number == 0:
            continue
        if line == "":
            continue
        left, right = line.split(" ")
        ranks[(left, right)] = rank
        rank += 1

    return vocab, ranks

def encode_chunk_gpt2(chunk, vocab, ranks, byte_table):
    pieces = [byte_table[b] for b in chunk.encode("utf-8")]

    while len(pieces) >= 2:
        best_pair = None
        best_rank = None
        for pair in zip(pieces, pieces[1:]):
            if pair in ranks:
                if best_rank is None or ranks[pair] < best_rank:
                    best_pair = pair
                    best_rank = ranks[pair]
        if best_pair is None:
            break
        pieces = merge(pieces, best_pair, best_pair[0] + best_pair[1])

    return [vocab[piece] for piece in pieces]

def encode_gpt2(text, directory):
    vocab, ranks = load_vocab(directory)
    byte_table = bytes_to_unicode()

    ids = []
    for chunk in COMPILED_PATTERN.findall(text):
        ids.extend(encode_chunk_gpt2(chunk, vocab, ranks, byte_table))
    return ids


def get_option(name):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return None

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # TODO: Uncomment the code below to pass the first stage
    
    command = sys.argv[1]
    if command == "bytes":
        with open(sys.argv[2], "rb") as f:
            data = f.read()
        print(json.dumps(list(data)))

    elif command == "top-pair":
        with open(sys.argv[2], "r") as f:
            ids = json.load(f)
        pair = top_pair(ids)
        print(json.dumps(list(pair)))

    elif command == "merge":
        with open(sys.argv[2], "r") as f:
            ids = json.load(f)
        pair_text = sys.argv[4]
        a, b = pair_text.split(",")
        pair = (int(a), int(b))
        print(json.dumps(merge(ids, pair, 256)))

    elif command == "train":
        with open(sys.argv[2], "r") as f:
            text = f.read()
        num_merges = int(sys.argv[4])
        print(json.dumps(train(text, num_merges)))

    elif command == "encode":
        with open(sys.argv[2], "r") as f:
            text = f.read()
        vocab_dir = get_option("--vocab")
        if vocab_dir is not None:
            print(json.dumps(encode_gpt2(text, vocab_dir)))
        else:
            with open(get_option("--merges"), "r") as f:
                merges = json.load(f)
            print(json.dumps(encode(text, merges, get_option("--pretokenize"))))

    elif command == "decode":
        with open(sys.argv[2], "r") as f:
            ids = json.load(f)
        with open(sys.argv[4], "r") as f:
            merges = json.load(f)
        print(json.dumps(decode(ids, merges)))

    else:
        raise RuntimeError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
