import sys, unicodedata
import vigenere
import codebreaker

def remove_accents(s: str) -> str:
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def usage() -> None:
    print("python3 program.py <command> <input>")
    print("commands:")
    print("     encrypt <password>")
    print("     decrypt <password>")
    print("     break <input>")

def next_arg(args: list[str]) -> str:
    if len(args) == 0:
        usage()
        exit(1)
    argument = args[0]
    args.pop(0)
    return argument

def read_from_stdin() -> str:
    text = open(0).read()
    return text

def print_to_stdout(*a) -> None:
    print(*a, file=sys.stdout)

def main() -> None:
    args = sys.argv
    program = next_arg(args)
    command = next_arg(args)
    text = remove_accents(read_from_stdin())
    if command == "encrypt":
        password = next_arg(args)
        result = vigenere.encrypt(text, password)
        print_to_stdout(result)

    elif command == "decrypt":
        password = next_arg(args)
        result = vigenere.decrypt(text, password)
        print_to_stdout(result)

    elif command == "break":
        key = codebreaker.break_cipher(text)
        print_to_stdout(f"KEY: {key}\n")
        print_to_stdout(vigenere.decrypt(text, key))

    else:
        usage()
        exit(1)

if __name__ == "__main__":
    main()
