import json
import sys


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # TODO: Uncomment the code below to pass the first stage
    #
    # command = sys.argv[1]
    # if command == "bytes":
    #     with open(sys.argv[2], "rb") as f:
    #         data = f.read()
    #     print(json.dumps(list(data)))
    # else:
    #     raise RuntimeError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
