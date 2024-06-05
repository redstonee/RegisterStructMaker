from argparse import ArgumentParser
from csv import DictReader


def main():
    parser = ArgumentParser(description="Generate C struct from register map")
    parser.add_argument("-n", "--name", help="Name of the struct", required=True)
    parser.add_argument("-i", "--input", help="Input CSV file", required=True)
    # Optional output filename, default is specified with '-n' argument
    parser.add_argument("-o", "--output", help="Output C file", required=False) 
    args = parser.parse_args()

    input_file = open(args.input, "r")
    if(args.output == None):
        output_file = open(args.name + ".h", "w")
    else:
        output_file = open(args.output, "w")

    reader = DictReader(input_file)
    fields = list(reader)

    reservedSpaceCount = 0  # Add reserved space if there is a gap between registers
    lastAddr = 0  # Last address of the register
    output_file.write("typedef struct\n")
    output_file.write("{\n")
    for field in fields:
        
        deltaAddr = int(field["Addr"], 0) - lastAddr
        if deltaAddr > 4:
            if deltaAddr > 8:
                # If the gap is more than 1 word, add an array of reserved space
                output_file.write(
                    "    uint32_t RESERVED{}[{}]; // {} - {} Reserved \n".format(
                        reservedSpaceCount,
                        hex(int((deltaAddr - 4) / 4)),
                        hex(lastAddr + 4),
                        hex(int(field["Addr"], 0) - 4),
                    )
                )
            else:
                # If the gap is 1 word, add a single reserved space
                output_file.write(
                    "    uint32_t RESERVED{}; // {} Reserved \n".format(
                        reservedSpaceCount,
                        hex(lastAddr + 4),
                    )
                )
            reservedSpaceCount += 1
        
        output_file.write(
            "    __IO uint32_t {}; // {} {} \n".format(
                field["Name"], field["Addr"], field["Desc"]
            )
        )
        lastAddr = int(field["Addr"], 0)

    output_file.write("} " + args.name + ";\n")
    output_file.close()
    input_file.close()

if __name__ == "__main__":
    main()
