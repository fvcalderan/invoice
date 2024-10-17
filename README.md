# invoice
Generate PDF invoices using JSON files as input

```
  __                _     _                      
 / _|_   _____ __ _| | __| | ___ _ __ __ _ _ __  
| |_\ \ / / __/ _` | |/ _` |/ _ \ '__/ _` | '_ \ 
|  _|\ V / (_| (_| | | (_| |  __/ | | (_| | | | |
|_|   \_/ \___\__,_|_|\__,_|\___|_|  \__,_|_| |_|

BSD 3-Clause License
Copyright (c) 2024, Felipe V. Calderan
All rights reserved.
Read the full license inside LICENSE file
```

## Requirements
You need `Python3` and `wkhtmltopdf` installed on your system.

## How to use

Write a JSON file with the necessary information, such as the `example.json` provided. Then, run:
```sh
python3 invoice.py example.json
```

and the program will generate a PDF file named `NUMBER_YY-MM-DD_invoice.pdf`. See `1_24-10-17_invoice.pdf` for an example.

## Customize

To further customize the invoice, edit `logo.png` and `template.html` files.
