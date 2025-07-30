# Basic MCP Server

A simple Model Context Protocol (MCP) server implementation in Python that provides basic tools for file operations, text processing, and calculations.

## Features

This MCP server provides the following tools:

### File Operations
- **read_file**: Read the contents of a file
- **write_file**: Write content to a file (creates directories if needed)
- **list_directory**: List contents of a directory with file types and sizes

### Text Processing
- **text_process**: Process text with various operations:
  - `uppercase`: Convert text to uppercase
  - `lowercase`: Convert text to lowercase
  - `reverse`: Reverse the text
  - `word_count`: Count words and characters

### Calculations
- **calculate**: Perform basic mathematical calculations (supports +, -, *, /, parentheses)

## Installation

1. **Clone or set up the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install mcp>=1.0.0 pydantic>=2.0.0
   ```

## Usage

### Running the Server

The MCP server uses stdio for communication. Run it directly:

```bash
python mcp_server.py
```

### Integration with MCP Clients

To use this server with an MCP client (like Claude Desktop), you need to configure it in the client's settings.

#### Claude Desktop Configuration

Add this to your Claude Desktop configuration file:

**On macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**On Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "basic-mcp-server": {
      "command": "python",
      "args": ["/absolute/path/to/your/mcp_server.py"]
    }
  }
}
```

Replace `/absolute/path/to/your/mcp_server.py` with the actual absolute path to your `mcp_server.py` file.

## Tools Reference

### read_file
Read the contents of a file.

**Parameters:**
- `path` (string, required): Path to the file to read

**Example:**
```json
{
  "name": "read_file",
  "arguments": {
    "path": "example.txt"
  }
}
```

### write_file
Write content to a file. Creates parent directories if they don't exist.

**Parameters:**
- `path` (string, required): Path to the file to write
- `content` (string, required): Content to write to the file

**Example:**
```json
{
  "name": "write_file",
  "arguments": {
    "path": "output/example.txt",
    "content": "Hello, World!"
  }
}
```

### list_directory
List the contents of a directory with file types and sizes.

**Parameters:**
- `path` (string, required): Path to the directory to list

**Example:**
```json
{
  "name": "list_directory",
  "arguments": {
    "path": "."
  }
}
```

### text_process
Process text with various operations.

**Parameters:**
- `text` (string, required): Text to process
- `operation` (string, optional): Operation to perform. Options: `uppercase`, `lowercase`, `reverse`, `word_count`. Default: `uppercase`

**Examples:**
```json
{
  "name": "text_process",
  "arguments": {
    "text": "Hello World",
    "operation": "uppercase"
  }
}
```

```json
{
  "name": "text_process",
  "arguments": {
    "text": "Count these words",
    "operation": "word_count"
  }
}
```

### calculate
Perform basic mathematical calculations.

**Parameters:**
- `expression` (string, required): Mathematical expression to evaluate

**Example:**
```json
{
  "name": "calculate",
  "arguments": {
    "expression": "2 + 3 * 4"
  }
}
```

## Development

### Project Structure
```
.
├── mcp_server.py      # Main MCP server implementation
├── requirements.txt   # Python dependencies
├── README.md         # This file
└── hello_world.py    # Example file (can be removed)
```

### Adding New Tools

To add a new tool:

1. Add the tool definition to the `handle_list_tools()` function
2. Add the tool implementation to the `handle_call_tool()` function
3. Create appropriate Pydantic models for argument validation if needed

### Error Handling

The server includes comprehensive error handling:
- File not found errors
- Invalid directory paths
- Mathematical expression errors
- Invalid characters in calculations
- General exception handling with logging

## Security Notes

- The `calculate` tool uses Python's `eval()` function with character filtering for simplicity
- In production environments, consider using a safer expression evaluator like `ast.literal_eval()` or a dedicated math parser
- File operations are not sandboxed - ensure proper access controls in production

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **Path issues**: Use absolute paths in client configurations
3. **Permission errors**: Ensure the server has read/write permissions for target directories

### Logging

The server logs to stdout at INFO level. To see debug information, modify the logging level in `mcp_server.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## License

This is a basic example implementation. Feel free to modify and extend for your needs.