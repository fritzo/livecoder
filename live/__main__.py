import sys
import live


def main():
    if len(sys.argv) != 2:
        print('Usage: live SCRIPT_PATH')
        sys.exit(1)
    script_path = sys.argv[1]
    live.main(script_path)


if __name__ == '__main__':
    main()
