# RegMap2Struct
This is a simple tool to generate C++ struct from register map file.

## Usage
```
python regmap2struct.py -n <struct_name> -i <input_file> [-o <output_file>]
```
* `-n` or `--name`: The name of the struct, 
* `-i` or `--input`: The input CSV file path,
* `-o` or `--output`: The output C file path, will be the same as the output file name if not specified.

For example:
```bash
python regmap2struct.py -n RegMap -i example.csv -o regmap.h
```

## Input File Format
The input file should be a CSV file with the following format:
```
Name,Addr,Desc
<name1>,<address1>,<description1>
<name2>,<address2>,<description2>
...
```
*The address is the offset from the base, should be in hexadecimal format like `0x1234`.*
