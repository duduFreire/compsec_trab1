import sys
import vigenere
import codebreaker
from string_processing import remove_accents

def usage() -> None:
    print("python3 program.py <command>")
    print()
    print("commands:")
    print("     encrypt <password>")
    print("     decrypt <password>")
    print("     break <language>")
    print()
    print("language:")
    print("     en")
    print("     pt")
    print()
    print("Examples:")
    print("cat text.txt | python3 main.py encrypt arara")
    print()
    print("""cat text.txt | python3 main.py encrypt arara \\
             | python3 main.py decrypt arara""")
    print()
    print("""cat text.txt | python3 main.py encrypt arara \\
             | python3 main.py break""")
    print()
    print("""cat text.txt | python3 main.py encrypt arara \\
             | python3 main.py break pt""")

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
    text_normal_case = remove_accents(read_from_stdin())
    text = text_normal_case.lower()

    if command == "encrypt":
        password = next_arg(args).lower()
        result = vigenere.encrypt(text_normal_case, password)
        print_to_stdout(result)

    elif command == "decrypt":
        password = next_arg(args).lower()
        result = vigenere.decrypt(text_normal_case, password)
        print_to_stdout(result)

    elif command == "break":
        key = ""
        if (len(args) > 0):
            language = next_arg(args)
            if language == "pt":
                key = codebreaker.break_cipher_in_pt(text)
            elif language == "en":
                key = codebreaker.break_cipher_in_en(text)
            else:
                usage()
                exit(1)
        else:
            key = codebreaker.break_cipher_in_all_languages(text)

        print_to_stdout(f"KEY: {key}\n")
        print_to_stdout(vigenere.decrypt(text_normal_case, key))

    else:
        usage()
        exit(1)

if __name__ == "__main__":
    main()
