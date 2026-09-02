"""System prompt and tool schemas for the invoice extraction agent."""

SYSTEM_PROMPT = """You process vendor invoices for a business's accounts payable team.

For each invoice:
1. Read the invoice text.
2. Call find_payee with the vendor name exactly as printed on the invoice.
3. If find_payee returns no match, call create_payee for the vendor.
4. Call submit_extraction with the invoice fields.

Copy amounts exactly as printed on the invoice, including thousands and decimal separators. Downstream code normalises them.
Write dates as YYYY-MM-DD. Use the ISO 4217 currency code.
If a field is not on the invoice, pass null."""

FIND_PAYEE_TOOL = {
    "name": "find_payee",
    "description": "Looks up existing payees for this business by vendor name.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "required": ["name"],
        "additionalProperties": False,
    },
}

CREATE_PAYEE_TOOL = {
    "name": "create_payee",
    "description": "Creates a new payee for this business.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": ["string", "null"]},
        },
        "required": ["name", "email"],
        "additionalProperties": False,
    },
}

SUBMIT_EXTRACTION_TOOL = {
    "name": "submit_extraction",
    "description": "Submits the extracted invoice. Call exactly once, last.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "vendor_name": {"type": "string"},
            "invoice_number": {"type": ["string", "null"]},
            "currency": {"type": "string"},
            "total": {"type": "string"},
            "due_date": {"type": ["string", "null"]},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "amount": {"type": "string"},
                    },
                    "required": ["description", "amount"],
                    "additionalProperties": False,
                },
            },
        },
        "required": [
            "vendor_name",
            "invoice_number",
            "currency",
            "total",
            "due_date",
            "line_items",
        ],
        "additionalProperties": False,
    },
}

TOOLS = [FIND_PAYEE_TOOL, CREATE_PAYEE_TOOL, SUBMIT_EXTRACTION_TOOL]


def build_user_message(*, business_name, document_text):
    """Wraps the OCR text for the first user turn."""
    return f"Business: {business_name}\n\n" f"<invoice>\n{document_text}\n</invoice>"
