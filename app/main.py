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

    else:
        raise RuntimeError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
