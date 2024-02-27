import sys
import xxhash


def main():
    path = sys.argv[1]
    with open(path) as f:
        s = f.read()
        x = xxhash.xxh64(s)
        print(x.intdigest())


if __name__ == "__main__":
    main()
