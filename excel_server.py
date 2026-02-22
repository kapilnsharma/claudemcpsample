from mcp.server.fastmcp import FastMCP
import pandas as pd
import os

# Initialize FastMCP
mcp = FastMCP("ExcelReader")

@mcp.tool()
def read_excel_data(file_path: str, sheet: str = "Sheet1"):
    """
    Reads an Excel file and returns the data for analysis.
    Provide the full absolute path to the file.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet)
        # We'll return the first 100 rows to avoid hitting context limits
        return df.head(100).to_csv(index=False)
    except Exception as e:
        return f"Error reading Excel: {str(e)}"

if __name__ == "__main__":
    mcp.run()