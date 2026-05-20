from datetime import datetime
import zoneinfo

def time_converter(timezone: str) -> str:
    """Convert current datetime to the given timezone string (e.g. 'Asia/Karachi')."""
    try:
        tz = zoneinfo.ZoneInfo(timezone)
    except zoneinfo.ZoneInfoNotFoundError:
        return f"Unknown timezone: '{timezone}'"
    now = datetime.now(tz)
    return now.strftime(f"%Y-%m-%d %H:%M:%S %Z (UTC%z)")


time_converter_tool = {
    "type": "function",
    "function": {
        "name": "time_converter",
        "description": "Convert current datetime to the given timezone string (e.g. 'Asia/Karachi').",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string", 
                    "description": "The timezone to convert to (e.g. 'Asia/Karachi')"
                }
            },
            "required": ["timezone"],
        },
    },
}

# print(time_converter('Asia/Karachi')) # 2026-05-20 07:19:46 PKT (UTC+0500)
# print(time_converter('America/New_York')) # 2026-05-19 22:19:46 EDT (UTC-0400)
# print(time_converter('Invalid/Timezone')) # Unknown timezone: 'Invalid/Timezone'