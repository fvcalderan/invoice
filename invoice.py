import os
import sys
import json
import datetime

__author__ = "Felipe V. Calderan"
__copyright__ = "Copyright (C) 2024 Felipe V. Calderan"
__license__ = 'BSD 3-Clause "New" or "Revised" License'
__version__ = "1.0"

DISCOUNT_STR = """                <tr>
                    <td class="gray">Discount:</td>
                    <td class="td_right">[DISCOUNT]</td>
                </tr>"""

ITEM_STR = """            <tr>
                <td>&nbsp;<b>[ITEM_NAME]</b></td>
                <td>[ITEM_QUANTITY]</td>
                <td>[ITEM_RATE]</td>
                <td>[ITEM_AMOUNT]</td>
            </tr>"""


def main():

    pypath = os.path.dirname(os.path.realpath(__file__))

    # Check args
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} settings_file.json")
        exit()

    # Load template
    try:
        with open(f"{pypath}/template.html", "r") as f:
            template = f.read()
    except Exception:
        print(f"[ERROR] Failed to open template.html.")
        exit()

    # Load settings
    try:
        with open(sys.argv[1], "r") as f:
            sets_text = f.read()
            sets = json.loads(sets_text)
    except json.decoder.JSONDecodeError:
        print(f"[ERROR] {sys.argv[1]} is incorrectly formatted.")
        exit()
    except Exception:
        print(f"[ERROR] Failed to open {sys.argv[1]}")
        exit()

    # Replace several elements
    template = template.replace("[LOGO_PATH]", f"{pypath}/logo.png")
    template = template.replace("[INVOICE_NUM]", f"#{sets['invoice_num']}")
    template = template.replace("[BILL_FROM]", sets["bill_from"])
    template = template.replace("[BILL_FROM_ADDRESS]", sets["bill_from_address"])
    template = template.replace("[BILL_TO]", sets["bill_to"])
    template = template.replace("[BILL_TO_ADDRESS]", sets["bill_to_address"])
    template = template.replace("[DATE]", sets["date"])
    template = template.replace("[DUE_DATE]", sets["due_date"])
    template = template.replace("[NOTES]", sets["notes"])

    # Get currency
    cur = sets["currency"]

    # Get discount
    disc = sets.get("discount", 0)

    # Replace discount
    if disc > 0:
        template = template.replace(
            "[DISCOUNT]",
            DISCOUNT_STR.replace("[DISCOUNT]", f"{cur}{disc:.2f}"),
        )
    else:
        template = template.replace("[DISCOUNT]", "")

    # Subtotal value
    subtotal = 0

    # Items
    items = ""

    # Replace items and add subtotal
    for it in sets["items"]:
        item = ITEM_STR.replace("[ITEM_NAME]", str(it[0]))
        item = item.replace("[ITEM_QUANTITY]", str(it[1]))
        item = item.replace("[ITEM_RATE]", f"{cur}{it[2]:.2f}")
        item = item.replace("[ITEM_AMOUNT]", f"{cur}{it[1] * it[2]:.2f}")
        items += item + "\n"
        subtotal += it[1] * it[2]

    # Print items
    template = template.replace("[ITEMS]", items)

    # Calculate total
    total = subtotal - disc

    # Replace values
    template = template.replace("[SUBTOTAL]", f"{cur}{subtotal:.2f}")
    template = template.replace("[TOTAL]", f"{cur}{total:.2f}")
    template = template.replace("[BALANCE_DUE]", f"{cur}{total:.2f}")

    # Save HTML content
    try:
        with open("input_file.html", "w") as f:
            _ = f.write(template)
    except Exception:
        print("[ERROR] Failed to save HTML content.")
        exit()

    # Get today's date for filename
    today = datetime.date.today().strftime("%y-%m-%d")

    # Get invoice number for filename
    invoice_num = sets["invoice_num"]

    # Use wkhtmltopdf to generate PDF file from HTML content
    # command = f"wkhtmltopdf --page-width 110 --page-height 155 --enable-local-file-access input_file.html {invoice_num}_{today}_invoice.pdf"
    command = f"wkhtmltopdf --page-width 160 --page-height 226 --enable-local-file-access input_file.html {invoice_num}_{today}_invoice.pdf"
    ret = os.system(command)
    if ret != 0:
        print("[ERROR] Failed to convert HTML to PDF using wkhtmltopdf.")
        exit()

    # Delete HTML content
    try:
        if os.path.exists("input_file.html"):
            os.remove("input_file.html")
    except Exception:
        print("[ERROR] Failed to delete HTML content.")
        exit()


if __name__ == "__main__":
    main()
