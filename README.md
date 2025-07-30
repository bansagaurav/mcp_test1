# Simple MCP Server - Addition Tool

## 🎯 What This Is

This is the **simplest possible** Model Context Protocol (MCP) server. It does exactly one thing: adds two numbers together. This makes it perfect for learning how MCP works without getting distracted by complex functionality.

## 🤔 What is MCP (Model Context Protocol)?

**The Simple Explanation:**
MCP is a way for AI assistants (like Claude) to use external tools. Instead of the AI trying to do everything itself, it can ask specialized programs (like this one) to help with specific tasks.

**Think of it like this:**
- You ask Claude: "What's 15 + 27?"
- Claude thinks: "I could calculate this myself, but let me check if there's a calculator tool available"
- Claude finds our MCP server and asks it: "Can you add 15 and 27?"
- Our server responds: "The sum of 15 and 27 is 42"
- Claude tells you: "The answer is 42"

**Why Use MCP Instead of Built-in AI Math?**
- **Reliability**: External tools can be more accurate for specific tasks
- **Extensibility**: You can add custom business logic, database access, etc.
- **Transparency**: You can see exactly what calculations were performed
- **Control**: You decide what tools are available and how they work

## 📁 File Structure Explained

```
.
├── mcp_server.py      # 🧠 The main server code
├── requirements.txt   # 📦 List of needed Python packages  
├── README.md         # 📖 This instruction file
├── run_server.sh     # 🚀 Convenience script to start the server
├── venv/             # 🔒 Isolated Python environment
└── hello_world.py    # 🗑️ Can be deleted (leftover file)
```

### Why Do We Need Each File?

#### 🧠 `mcp_server.py` - The Main Server
**What it does:** Contains all the logic for our MCP server
**Why it exists:** This is where we define what tools we have and how they work
**Could we skip it?** No - this IS our server

#### 📦 `requirements.txt` - Dependencies List  
**What it does:** Lists the Python packages our server needs
**Why it exists:** So anyone can install the exact same packages with one command
**Could we skip it?** Technically yes, but then you'd have to manually install packages and might get version conflicts

**Why not just say "install mcp and pydantic"?**
- Different people might install different versions
- Some versions might not work together  
- You might forget which packages are needed
- Deployment systems expect a requirements.txt file

#### 📖 `README.md` - Instructions (This File)
**What it does:** Explains how everything works
**Why it exists:** So you (and others) can understand and use the server
**Could we skip it?** Yes, but then nobody would know how to use your server

#### 🚀 `run_server.sh` - Startup Script
**What it does:** Activates the virtual environment and starts the server
**Why it exists:** Saves you from typing multiple commands every time
**Could we skip it?** Yes, but you'd have to remember the commands to start the server

#### 🔒 `venv/` - Virtual Environment Directory
**What it does:** Contains an isolated Python environment with our packages
**Why it exists:** Prevents conflicts with other Python projects on your system
**Could we skip it?** Yes, but you might get package conflicts with other projects

## 🛠️ Installation & Setup

### Step 1: Install System Requirements
```bash
# On Ubuntu/Debian (if you don't have Python 3)
sudo apt update
sudo apt install -y python3 python3-venv python3-pip

# On macOS (if you don't have Python 3)
brew install python3

# On Windows - download Python from python.org
```

### Step 2: Set Up Virtual Environment
```bash
# Create isolated Python environment
python3 -m venv venv

# Activate it (Linux/macOS)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

**Why Virtual Environment?**
- Keeps this project's packages separate from other Python projects
- Prevents version conflicts
- Makes the project portable
- Standard practice in Python development

### Step 3: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

This installs:
- **mcp**: The Model Context Protocol library
- **pydantic**: Data validation (ensures our inputs are correct)

## 🚀 Running the Server

### Option 1: Use the Convenience Script
```bash
./run_server.sh
```

### Option 2: Manual Commands
```bash
source venv/bin/activate
python3 mcp_server.py
```

### What You'll See
```
INFO:__main__:Starting Simple Addition MCP Server...
INFO:__main__:This server provides one tool: add_numbers
INFO:__main__:Connect an MCP client to start using it!
```

The server is now running and waiting for MCP clients to connect!

## 🔌 Connecting MCP Clients

### Claude Desktop Setup

1. **Find your config file:**
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add this configuration:**
```json
{
  "mcpServers": {
    "simple-addition": {
      "command": "python3",
      "args": ["/absolute/path/to/your/mcp_server.py"],
      "env": {
        "PATH": "/absolute/path/to/your/venv/bin:/usr/bin:/bin"
      }
    }
  }
}
```

3. **Replace the paths:**
   - Change `/absolute/path/to/your/mcp_server.py` to the real path
   - Change `/absolute/path/to/your/venv/bin` to your venv path

4. **Get the absolute path:**
```bash
# In your project directory
pwd  # Shows current directory
# Then add /mcp_server.py to the end
```

### Other MCP Clients
Any program that speaks the MCP protocol can connect to this server. The server communicates through stdin/stdout using JSON messages.

## 🧮 Using the Addition Tool

Once connected to an MCP client, you can use the tool:

**Example conversation with Claude:**
```
You: "Can you add 15 and 27 for me?"

Claude: I'll use the addition tool to calculate that for you.
[Calls add_numbers tool with a=15, b=27]

Tool result: "The sum of 15 and 27 is 42"

Claude: The sum of 15 and 27 is 42.
```

**What happens behind the scenes:**
1. Claude recognizes this might be a math problem
2. Claude asks our server: "What tools do you have?"
3. Our server responds: "I have add_numbers tool"
4. Claude calls: `add_numbers(a=15, b=27)`
5. Our server calculates: `15 + 27 = 42`
6. Our server responds: "The sum of 15 and 27 is 42"
7. Claude shows you the result

## 🔧 How the Code Works

### The Tool Definition
```python
Tool(
    name="add_numbers",
    description="Add two numbers together and return the result",
    inputSchema={
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "The first number"},
            "b": {"type": "number", "description": "The second number"}
        },
        "required": ["a", "b"]
    }
)
```

This tells MCP clients:
- The tool is called `add_numbers`
- It needs two numbers: `a` and `b`
- Both parameters are required

### The Tool Implementation
```python
def handle_call_tool(name: str, arguments: Dict[str, Any]):
    if name == "add_numbers":
        args = AdditionArgs(**arguments)  # Validate inputs
        result = args.a + args.b           # Do the math
        return f"The sum of {args.a} and {args.b} is {result}"
```

This:
1. Checks if the requested tool is `add_numbers`
2. Validates that `a` and `b` are numbers
3. Adds them together
4. Returns a formatted result

### Input Validation with Pydantic
```python
class AdditionArgs(BaseModel):
    a: float
    b: float
```

This automatically:
- Ensures `a` and `b` are provided
- Converts them to numbers if possible
- Gives clear error messages if validation fails

**Example validation errors:**
- Missing parameter: "field required"
- Wrong type: "value is not a valid float"

## 🚨 Troubleshooting

### "Import Error: No module named 'mcp'"
**Problem:** MCP package not installed
**Solution:** 
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Permission denied" when running ./run_server.sh
**Problem:** Script not executable
**Solution:**
```bash
chmod +x run_server.sh
```

### "Command not found: python3"
**Problem:** Python not installed
**Solution:** Install Python 3 for your operating system

### "Virtual environment not activated"
**Problem:** Forgot to activate venv
**Solution:**
```bash
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Claude Desktop doesn't see the server
**Problems & Solutions:**
1. **Wrong path in config:** Use absolute paths, not relative
2. **Config file location:** Make sure you're editing the right file
3. **JSON syntax error:** Validate your JSON configuration
4. **Server not running:** Make sure the server starts without errors

### Getting absolute paths
```bash
# Show current directory
pwd

# Show full path to a file
realpath mcp_server.py

# Show full path to venv
realpath venv/bin/python3
```

## 🎓 Learning Exercises

### 1. Modify the Tool
Try changing the addition tool to:
- Subtract instead of add
- Multiply two numbers
- Calculate percentage

### 2. Add Input Validation
Try modifying the code to:
- Only allow positive numbers
- Round results to 2 decimal places
- Add minimum/maximum limits

### 3. Add More Tools
Try adding a second tool:
- Subtraction
- Multiplication
- Finding the larger of two numbers

### 4. Improve Error Messages
Try making error messages more user-friendly:
- "Please provide two numbers"
- "Numbers must be positive"
- Custom validation messages

## 🔍 Understanding MCP Protocol

### Message Flow
1. **Client connects** → Server ready
2. **Client asks for tools** → Server lists available tools
3. **Client calls tool** → Server executes and returns result
4. **Client disconnects** → Server shuts down

### JSON Messages (Behind the Scenes)
**Tool list request:**
```json
{"method": "tools/list", "params": {}}
```

**Tool list response:**
```json
{
  "tools": [{
    "name": "add_numbers",
    "description": "Add two numbers together",
    "inputSchema": {...}
  }]
}
```

**Tool call request:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "add_numbers",
    "arguments": {"a": 15, "b": 27}
  }
}
```

**Tool call response:**
```json
{
  "content": [{
    "type": "text",
    "text": "The sum of 15 and 27 is 42"
  }]
}
```

## 📚 Next Steps

### Want to Build More Complex Tools?
- **File operations:** Read/write files
- **Database access:** Query databases
- **API calls:** Fetch data from web services
- **Image processing:** Analyze or modify images
- **Custom business logic:** Implement your specific needs

### Want to Learn More About MCP?
- Read the official MCP specification
- Check out other MCP server examples
- Join the MCP community discussions

### Want to Deploy This Server?
- **Docker:** Containerize the server
- **Cloud hosting:** Deploy to AWS, Google Cloud, etc.
- **Process management:** Use systemd, PM2, or similar
- **Load balancing:** Handle multiple clients

---

## 🎉 Congratulations!

You now have a working MCP server and understand:
- What MCP is and why it's useful
- How to set up a Python development environment
- Why we need requirements.txt and virtual environments
- How MCP clients communicate with servers
- How to define and implement tools
- How to validate inputs safely
- How to troubleshoot common problems

This simple addition server is the foundation for building much more complex and useful MCP tools!
