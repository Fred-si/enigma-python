from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from enum import Enum
from secrets import randbelow
from typing import TypeVar

from enigma import AvailableReflector, AvailableRotor, Enigma, EnigmaConfig

T = TypeVar("T")


def parse_args(argv: Sequence[str]) -> Namespace:
    parser = ArgumentParser("Emulate Enigma encryption")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "list",
        help="List available rotors and reflectors",
    )

    random_command = subparsers.add_parser(
        "random",
        help="Generate random config",
    )
    random_command.add_argument(
        "--plug-count",
        "-p",
        action="store",
        type=int,
        default=None,
        help="The plug count in plugin board. Between 0 and 10 includes",
    )
    random_command.add_argument(
        "--count",
        "-c",
        action="store",
        type=int,
        default=1,
        help="The number of configuration to generate",
    )

    encode_command = subparsers.add_parser("encode", help="Encode message")

    encode_command.add_argument(
        "--rotors",
        "-r",
        help="Provide rotors configuration",
        action="store",
        type=lambda v: v.upper(),
        required=True,
    )

    encode_command.add_argument(
        "--reflector",
        "-s",
        help="Provide reflector configuration",
        action="store",
        type=lambda v: v.upper(),
        required=True,
    )

    encode_command.add_argument(
        "--plugs",
        "-p",
        help="Provide plugs configuration",
        action="store",
        default="",
        type=lambda v: v.upper(),
    )

    encode_command.add_argument("message", type=lambda v: v.upper())
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> None:
    args = parse_args(argv[1:])

    match args.command:
        case "list":
            print(
                "Available rotors:",
                enum_to_string(AvailableRotor, "    "),
                "",
                "Available reflectors:",
                enum_to_string(AvailableReflector, "    "),
                sep="\n",
            )

        case "encode":
            config = EnigmaConfig.parse(args.rotors, args.reflector, args.plugs)
            print(Enigma(config).encode_message(args.message))

        case "random":
            configs = (
                EnigmaConfig.generate_random_config(
                    args.plug_count
                    if args.plug_count is not None
                    else randbelow(11),
                ).as_dict()
                for _ in range(args.count)
            )

            for c in configs:
                print(
                    f"rotors: '{c['rotors']}'",
                    f"reflector: '{c['reflector']}'",
                    f"plugs: '{c['plugin_board']}'",
                    "",
                    sep="\n",
                )


def enum_to_string(enum: type[Enum], line_prefix: str) -> str:
    return "\n".join(f"{line_prefix}{e.name}: {e.value}" for e in enum)


if __name__ == "__main__":
    import sys

    main(sys.argv)
