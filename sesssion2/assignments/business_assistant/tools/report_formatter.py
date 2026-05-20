import json
from datetime import datetime

def format_report(report_type, data, period):
    """ Format business report with structure """
    template = {
        "sales": {
            "sections": ["Executive Summary" , "Key Metrics" ,"Analysis" , "Recommendations" ],
            "header": f"{period} Sales Performance Report "
        },
        "quarterly": {
            "sections": ["Overview" , "Financial Highlights" ,
            "Operational Updates" , "Next Steps "] ,
            "header": f"{period} Quarterly Report "
        },
        "annual": {
            "sections": ["Year in Review" , "Financial Summary" ,
            "Strategic Initiatives" , "Outlook for Next Year "] ,
            "header": f"{period} Annual Report "
        }
    }
    
    report_template = template.get(report_type, template["sales"])

    return json.dumps({
        "header": report_template["header"],
        "sections": report_template["sections"],
        "timestamp": datetime.now().strftime("%B %d, %Y"),
    })

report_formatter_tool = {
    "type": "function",
    "function": {
        "name": "format_report",
        "description": "Format a business report",
        "parameters": {
            "type": "object",
            "properties": {
                "report_type": {
                    "type": "string",
                    "enum": ["sales", "quarterly", "annual"],
                },
                "data": {"type": "string"},
                "period": {"type": "string"},
            },
            "required": ["report_type", "data", "period"],
        },
    },
}