# WineDbg MCP Server

This project provides a server that wraps the Wine Debugger (`winedbg`) and exposes its functionality through a simple API. This allows you to debug Windows applications running under Wine from a remote client.

## Installation

1.  Install Wine and `winedbg`.
2.  Create a Python virtual environment and install the required dependencies:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

1.  Start the server:

    ```bash
    python -m src.mcp_server
    ```

2.  Run the test client to see the server in action:

    ```bash
    python tests/test_client.py
    ```

## Testing with the Test App

This project includes a simple C application that can be used for testing the server.

1.  Compile the test application for 32-bit Windows:

    ```bash
    i686-w64-mingw32-gcc -o tests/test_app.exe tests/test_app.c
    ```

    If you don't have the MinGW-w64 cross-compiler, you can install it on Debian/Ubuntu with:
    `sudo apt-get install gcc-mingw-w64-i686`

2.  Run the test client:

    ```bash
    python tests/test_client.py
    ```

    The test client will automatically use the `test_app.exe` to test the server's functionality.

## MCP Server Configuration

If you are using a client that supports launching MCP servers, you can configure it with the following JSON. This tells the client how to start the `winedbg` server.

**Note:** Make sure to replace `/ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp-winedbg` with the actual absolute path to this project directory on your system.

```json
{
  "mcpServers": {
    "winedbg": {
      "command": "/ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp-winedbg/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp-winedbg/src/mcp_server.py"
      ]
    }
  }
}
```

## Available Tools

The server exposes the following tools:

*   `run`: Run an executable in `winedbg`.
*   `attach`: Attach to a process.
*   `quit`: Quit `winedbg`.
*   `detach`: Detach from the process.
*   `kill`: Kill the process.
*   `cont`: Continue execution.
*   `break_at`: Set a breakpoint.
*   `watch`: Set a watchpoint.
*   `info_break`: Get breakpoint info.
*   `delete_breakpoint`: Delete a breakpoint.
*   `backtrace`: Get a backtrace.
*   `frame`: Select a stack frame.
*   `up`: Move up the stack.
*   `down`: Move down the stack.
*   `step`: Step execution.
*   `next`: Next execution.
*   `stepi`: Step instruction.
*   `nexti`: Next instruction.
*   `finish`: Finish execution of the current function.
*   `print_var`: Print a variable.
*   `examine_memory`: Examine memory.
*   `info_locals`: Get local variables.
*   `info_args`: Get function arguments.
*   `info_proc`: Get process info.
*   `info_threads`: Get thread info.
*   `info_share`: Get shared library info.
*   `set_debug_channel`: Set the `WINEDEBUG` environment variable.
*   `get_debug_channels`: Get the `WINEDEBUG` environment variable.
