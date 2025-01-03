import chainlit as cl

class MessageFormatter:
    @staticmethod
    async def format_data_exploration(response):
        if response.get('status') == 'success':
            preview = response.get('preview', [])
            general_info = response.get('general_info', {})
            
            message = f"""
### Dataset Overview
- Total Rows: {general_info.get('num_rows')}
- Total Columns: {general_info.get('num_columns')}

### Preview of First {len(preview)} Rows:
"""
            for idx, row in enumerate(preview, 1):
                message += f"{idx}. {row.get('review')[:100]}...\n"
                message += f"   Sentiment: {row.get('sentiment')}\n\n"
            
            return message
        return "Error in data exploration"