import argparse
import json
import sys


def read_binary_file(filepath):
    with open(filepath, "rb") as f:
        return f.read()


def is_valid_sector(address: int) -> bool:
    """
    Returns whether or nor an address is within the user data sector
    :param address: Current Hex address
    :return: True if it's between the user data sector, false if it's not.
    """
    sector = address % 0x930
    return 0x18 <= sector <= 0x817


def addresses_left_in_sector(address: int) -> int:
    """
    Returns the amount of valid addresses left within the user data sector.
    This function is not valid outside that sector.
    :param address: Current Hex address
    :return: The amount of addresses until 0x817.
    """
    sector = address % 0x930
    return 0x817 - sector


def get_differences(file1, file2):
    differences = []
    min_length = min(len(file1), len(file2))
    i = 0
    last_percentage = -1  # To avoid redundant prints

    while i < min_length:
        # Calculate progress percentage
        percentage = (i * 100) // min_length

        # Only update if percentage changes to avoid excessive prints
        if percentage != last_percentage:
            last_percentage = percentage
            sys.stdout.write(f"\rProcessing: {percentage}%")
            sys.stdout.flush()

        if file1[i] != file2[i] and is_valid_sector(i):
            hex_address = f"0x{i:X}"
            entry_type = "char"
            length = 1
            sectors_left = addresses_left_in_sector(i)

            if i + 1 < min_length and file1[i:i + 1] != file2[i:i + 1] and sectors_left >= 1:
                length = 2
                entry_type = "short"

            if i + 3 < min_length and file1[i:i + 2] != file2[i:i + 2] and sectors_left >= 3:
                length = 4
                entry_type = "word"

            if i + length > min_length:
                length = min_length - i
                if length <= 1:
                    length = 1
                    entry_type = "char"
                elif length <= 2:
                    length = 2
                    entry_type = "short"
                else:
                    length = 4
                    entry_type = "word"

            hex_value = "0x" + file2[i:i+length].hex().upper()

            differences.append({
                "type": entry_type,
                "address": hex_address,
                "value": hex_value
            })

            i += length
        else:
            i += 1

    print("\rProcessing: 100%")
    return differences


def format_output(differences, output_format):
    if output_format == "json":
        return json.dumps(differences, indent=4)
    if output_format == "csv":
        lines = ["address,value,type"]
        for entry in differences:
            lines.append(f"{entry['address']},{entry['value']},{entry['type']}")
        return "\n".join(lines) + "\n"
    if output_format == "randomizer":
        write_methods = {
            "char": "writeChar",
            "short": "writeShort",
            "word": "writeWord",
        }
        lines = []
        for entry in differences:
            method = write_methods[entry["type"]]
            lines.append(
                f"offset = data.{method}({entry['address']}, {entry['value']})"
            )
        return "\n".join(lines) + "\n"
    raise ValueError(f"Unsupported output format: {output_format}")


def main():
    parser = argparse.ArgumentParser(description="Compare hex addresses of two binary files.")
    parser.add_argument("file1", help="Path to the first binary file")
    parser.add_argument("file2", help="Path to the second binary file")
    parser.add_argument("output", help="Path to save the differences output file")
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv", "randomizer"],
        default="json",
        help="Output format: json (default), csv, or randomizer",
    )
    args = parser.parse_args()

    file1_data = read_binary_file(args.file1)
    file2_data = read_binary_file(args.file2)

    differences = get_differences(file1_data, file2_data)

    with open(args.output, "w") as f:
        f.write(format_output(differences, args.format))

    print(f"Differences saved to {args.output} ({args.format})")


if __name__ == "__main__":
    main()
