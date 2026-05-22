This is a simple Python Script that compares two bin files and outputs the resulting differences in the target file as a json file in the same format as the Preset writes for the Randomizer.

Usage:
```
python diff.py <source_file> <target_file> <output_file>
```
Example:
```
python diff.py source.bin target.bin output.json
```

The resulting file will follow this format:
```json
[
    {
        "type": "word",
        "address": "0x491586E",
        "value": "0x00000000"
    },
    {
        "type": "word",
        "address": "0x4915872",
        "value": "0x00005102"
    },
    {
        "type": "word",
        "address": "0x491592E",
        "value": "0x00000000"
    }
]
```

You may also choose to format it as CSV or as Randomizer write operations by adding the format flag:

JSON Format: `-f json`
CSV Format: `-f csv` 
Randomizer Writes Format: `-f randomizer`

CSV Example:
```
python diff.py <source_file> <target_file> <output_file> -f csv
```

Result:
```csv
address,value,type
0x18,0x77777777,word
0x1C,0x77777777,word
0x20,0x77777777,word
0x24,0x77777777,word
0x28,0x77777777,word
0x2C,0x77777777,word
```

Randomizer Writes Example:
```
python diff.py <source_file> <target_file> <output_file> -f randomizer
```

Result:
```csv
offset = data.writeWord(0x18, 0x77777777)
offset = data.writeWord(0x1C, 0x77777777)
offset = data.writeWord(0x20, 0x77777777)
offset = data.writeWord(0x24, 0x77777777)
offset = data.writeWord(0x28, 0x77777777)
offset = data.writeWord(0x2C, 0x77777777)
```