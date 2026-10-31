import json
import sys
from collections import Counter

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

def encode(text, merges):
    ids = list(text.encode("utf-8"))
    ranks = {}

    for i, pair in enumerate(merges):
        ranks[(pair[0], pair[1])] = i

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
        with open(sys.argv[4], "r") as f:
            merges = json.load(f)
        print(json.dumps(encode(text, merges)))

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
