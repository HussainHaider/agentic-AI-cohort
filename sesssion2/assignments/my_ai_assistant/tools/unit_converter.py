def unit_converter(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a value from one unit to another. Supported units: 'meters', 'feet', 'kilograms', 'pounds'."""
    conversions = {
        ('meters', 'feet'): 3.28084,
        ('feet', 'meters'): 0.3048,
        ('kilograms', 'pounds'): 2.20462,
        ('pounds', 'kilograms'): 0.453592
    }
    
    key = (from_unit, to_unit)
    if key in conversions:
        return str(value * conversions[key])
    else:
        raise ValueError(f"Conversion from {from_unit} to {to_unit} is not supported.")
    
unit_converter_tool = {
    "type": "function",
    "function": {
        "name": "unit_converter",
        "description": "Convert a value from one unit to another. Supported units: 'meters', 'feet', 'kilograms', 'pounds'.",
        "parameters": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "number",
                    "description": "The numeric value to convert."
                },
                "from_unit": {
                    "type": "string",
                    "description": "The unit to convert from (e.g. 'meters')."
                },
                "to_unit": {
                    "type": "string",
                    "description": "The unit to convert to (e.g. 'feet')."
                }
            },
            "required": ["value", "from_unit", "to_unit"],
        },
    },
}