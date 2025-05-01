#!/usr/bin/env python3
"""
excel2ofx_argentina.py
----------------------

Convert an Argentinian‑peso bank statement saved as an Excel file into
an OFX 1.0 statement ready for KMyMoney 5.0.8.

Changes compared with the first script
--------------------------------------
* **Payee (`<NAME>`) is now ALWAYS "Argentina".**
* **The merchant / operation text now goes in `<MEMO>`.**

That lets you create one single KMyMoney payee called *Argentina*,
attach a default category to it, and have every import auto‑categorise.

Usage
-----
$ python excel2ofx_argentina.py Extracto_00095716476.xlsx \
      --acctid 00095716476 --bankid 285 --accttype CHECKING \
      -o salida.ofx

Dependencies
------------
pip install pandas openpyxl
"""

from __future__ import annotations
import argparse
import textwrap
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _parse_amount(cell) -> float:
    """
    Convert Argentinian‑style numbers ('-8.037,00') to floats.
    Blank cells → 0.0.
    """
    if pd.isna(cell) or cell == "":
        return 0.0
    if isinstance(cell, (int, float)):
        return float(cell)
    normalised = cell.replace(".", "").replace(",", ".").strip()
    return float(normalised)


def _extract_merchant(movimiento_text: str) -> str:
    """
    Bank exports often have multi‑line Movimiento strings, e.g.:

        COMPRA DEBITO
        SUPERMERCADO EL BALCON
        4517XXXX

    This takes the **first non‑blank line AFTER the operation type**
    (line 1 if present, else line 0) as the merchant description.
    """
    lines = [l.strip() for l in movimiento_text.replace("\r", "\n").split("\n")
             if l.strip()]
    return lines[1] if len(lines) > 1 else lines[0]


# ----------------------------------------------------------------------
# Main OFX builder
# ----------------------------------------------------------------------
def build_ofx(df: pd.DataFrame, *, acctid: str, bankid: str,
              accttype: str = "CHECKING",
              fixed_payee: str = "Argentina") -> str:
    """Return an OFX string representing the DataFrame's transactions."""
    # Parse and enrich the DataFrame
    df["debit"]   = df["Débito"].apply(_parse_amount)
    df["credit"]  = df["Crédito"].apply(_parse_amount)
    df["amount"]  = df["credit"] + df["debit"]
    df["date"]    = (pd.to_datetime(df["Fecha"], dayfirst=True)
                       .dt.strftime("%Y%m%d"))
    df["merchant"] = df["Movimiento"].apply(_extract_merchant)

    # Build transaction blocks
    stmt_blocks: list[str] = []
    for idx, row in df.iterrows():
        trntype = "CREDIT" if row["amount"] >= 0 else "DEBIT"
        fitid   = f"{row['date']}{idx:04d}"             # unique ID
        stmt_blocks.append(textwrap.dedent(f"""\
            <STMTTRN>
            <TRNTYPE>{trntype}
            <DTPOSTED>{row['date']}
            <TRNAMT>{row['amount']:.2f}
            <FITID>{fitid}
            <NAME>{fixed_payee}
            <MEMO>{row['merchant'][:250]}
            </STMTTRN>""").strip())

    # Statement‑level metadata
    dt_start = df["date"].iloc[-1]            # oldest txn
    dt_end   = df["date"].iloc[0]             # newest txn
    bal_amt  = _parse_amount(df["Saldo Parcial"].iloc[0])
    dt_asof  = dt_end
    now      = datetime.now().strftime("%Y%m%d%H%M%S")

    # Assemble the OFX document
    header = textwrap.dedent(f"""\
        OFXHEADER:100
        DATA:OFXSGML
        VERSION:102
        SECURITY:NONE
        ENCODING:USASCII
        CHARSET:1252
        COMPRESSION:NONE
        OLDFILEUID:NONE
        NEWFILEUID:{uuid.uuid4().hex}

        <OFX>
        <SIGNONMSGSRSV1>
          <SONRS>
            <STATUS>
              <CODE>0</CODE>
              <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <DTSERVER>{now}</DTSERVER>
            <LANGUAGE>ENG</LANGUAGE>
          </SONRS>
        </SIGNONMSGSRSV1>
        <BANKMSGSRSV1>
          <STMTTRNRS>
            <TRNUID>1</TRNUID>
            <STATUS>
              <CODE>0</CODE>
              <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <STMTRS>
              <CURDEF>ARS</CURDEF>
              <BANKACCTFROM>
                <BANKID>{bankid}</BANKID>
                <ACCTID>{acctid}</ACCTID>
                <ACCTTYPE>{accttype}</ACCTTYPE>
              </BANKACCTFROM>
              <BANKTRANLIST>
                <DTSTART>{dt_start}</DTSTART>
                <DTEND>{dt_end}</DTEND>
    """).lstrip()

    footer = textwrap.dedent(f"""\
              </BANKTRANLIST>
              <LEDGERBAL>
                <BALAMT>{bal_amt:.2f}</BALAMT>
                <DTASOF>{dt_asof}</DTASOF>
              </LEDGERBAL>
            </STMTRS>
          </STMTTRNRS>
        </BANKMSGSRSV1>
        </OFX>
    """)

    return "\n".join([header, *stmt_blocks, footer])


# ----------------------------------------------------------------------
# CLI wrapper
# ----------------------------------------------------------------------
def main() -> None:
    p = argparse.ArgumentParser(description="Convert Argentinian bank "
                                            "statement (Excel) → OFX "
                                            "with fixed payee 'Argentina'.")
    p.add_argument("xlsx", type=Path, help="Input Excel file")
    p.add_argument("-o", "--output", type=Path, default="statement.ofx",
                   help="Destination OFX file (default: statement.ofx)")
    p.add_argument("--acctid", required=True,
                   help="Account number as it should appear in OFX")
    p.add_argument("--bankid", default="0000",
                   help="Bank routing code / CBUI (default: 0000)")
    p.add_argument("--accttype", default="CHECKING",
                   choices=["CHECKING", "SAVINGS", "CREDITLINE"],
                   help="KMyMoney account type (default: CHECKING)")
    args = p.parse_args()

    # Read workbook and build OFX
    df = pd.read_excel(args.xlsx)
    ofx_text = build_ofx(df,
                         acctid=args.acctid,
                         bankid=args.bankid,
                         accttype=args.accttype)

    args.output.write_text(ofx_text, encoding="utf‑8")
    print(f"✓ Wrote {len(df)} transactions to {args.output}")


if __name__ == "__main__":
    main()
