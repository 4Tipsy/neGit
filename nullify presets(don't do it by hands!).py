# nullify presets.json

import json
with open("presets.json", "w") as write_file:
    json.dump({}, write_file)

input("presets.json was nullified")
