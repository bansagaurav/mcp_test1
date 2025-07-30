#!/usr/bin/env python3
"""
Test Script for MCP Sum Server

This script demonstrates basic functionality testing for our MCP server.
While MCP servers are typically tested through integration with MCP clients,
this script shows how to verify the core logic works correctly.

Why do we need testing?
======================
1. CONFIDENCE: Ensures our code works as expected
2. REGRESSION PREVENTION: Catches bugs when we make changes
3. DOCUMENTATION: Tests serve as examples of how code should be used
4. REFACTORING SAFETY: Allows safe code improvements
5. DEBUGGING AID: Helps isolate problems when they occur

Note: This is a simplified test - real MCP testing would involve:
- MCP protocol message simulation
- Client-server integration testing
- Async function testing with proper event loops
- Error condition testing
"""

import asyncio
import sys
import os

# Add the current directory to Python path so we can import our server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our server components
# We import specific functions to test them in isolation
try:
    from mcp_sum_server import handle_list_tools, handle_call_tool
    print("✓ Successfully imported MCP server components")
except ImportError as e:
    print(f"✗ Failed to import MCP server components: {e}")
    print("Make sure you've installed the requirements: pip install -r requirements.txt")
    sys.exit(1)

async def test_list_tools():
    """
    Test the tool listing functionality.
    
    This verifies that our server correctly advertises its available tools.
    In a real MCP interaction, this would be called when a client connects.
    """
    print("\n=== Testing Tool Listing ===")
    
    try:
        # Call the function that lists available tools
        tools = await handle_list_tools()
        
        # Verify we got a list back
        assert isinstance(tools, list), "handle_list_tools should return a list"
        assert len(tools) == 1, "Should have exactly one tool"
        
        # Verify the tool has the expected properties
        tool = tools[0]
        assert tool.name == "sum_two_numbers", f"Expected tool name 'sum_two_numbers', got '{tool.name}'"
        assert "sum" in tool.description.lower(), "Tool description should mention 'sum'"
        assert "inputSchema" in tool.model_dump(), "Tool should have input schema"
        
        print("✓ Tool listing works correctly")
        print(f"  - Tool name: {tool.name}")
        print(f"  - Description: {tool.description}")
        print(f"  - Has input schema: {'inputSchema' in tool.model_dump()}")
        
        return True
        
    except Exception as e:
        print(f"✗ Tool listing failed: {e}")
        return False

async def test_sum_calculation():
    """
    Test the actual sum calculation functionality.
    
    This verifies that our tool correctly adds two numbers and returns
    the expected result format.
    """
    print("\n=== Testing Sum Calculation ===")
    
    test_cases = [
        # (a, b, expected_sum, description)
        (5, 3, 8, "positive integers"),
        (10.5, 2.3, 12.8, "floating point numbers"),
        (-5, 3, -2, "negative and positive"),
        (0, 0, 0, "zeros"),
        (-10, -5, -15, "negative numbers"),
    ]
    
    all_passed = True
    
    for a, b, expected, description in test_cases:
        try:
            # Prepare arguments as they would come from an MCP client
            arguments = {"a": a, "b": b}
            
            # Call the tool execution function
            result = await handle_call_tool("sum_two_numbers", arguments)
            
            # Verify the result format
            assert isinstance(result, list), "Result should be a list"
            assert len(result) == 1, "Result should have exactly one item"
            assert hasattr(result[0], 'text'), "Result should have text content"
            
            # Extract the result text
            result_text = result[0].text
            
            # Verify the result contains the expected sum
            assert str(expected) in result_text, f"Result should contain {expected}"
            assert str(a) in result_text, f"Result should contain input {a}"
            assert str(b) in result_text, f"Result should contain input {b}"
            
            print(f"✓ {description}: {a} + {b} = {expected}")
            print(f"  Result: {result_text}")
            
        except Exception as e:
            print(f"✗ {description} failed: {e}")
            all_passed = False
    
    return all_passed

async def test_error_handling():
    """
    Test error handling for invalid inputs.
    
    This ensures our server properly handles edge cases and invalid inputs
    without crashing, providing helpful error messages instead.
    """
    print("\n=== Testing Error Handling ===")
    
    error_test_cases = [
        # (tool_name, arguments, expected_error_type, description)
        ("unknown_tool", {"a": 1, "b": 2}, "Unknown tool", "unknown tool name"),
        ("sum_two_numbers", None, "Arguments are required", "no arguments"),
        ("sum_two_numbers", {}, "Both 'a' and 'b' parameters are required", "empty arguments"),
        ("sum_two_numbers", {"a": 5}, "Both 'a' and 'b' parameters are required", "missing b parameter"),
        ("sum_two_numbers", {"b": 3}, "Both 'a' and 'b' parameters are required", "missing a parameter"),
        ("sum_two_numbers", {"a": "not_a_number", "b": 5}, "must be numbers", "non-numeric input"),
        ("sum_two_numbers", {"a": 5, "b": "also_not_a_number"}, "must be numbers", "non-numeric input"),
    ]
    
    all_passed = True
    
    for tool_name, arguments, expected_error, description in error_test_cases:
        try:
            # This should raise an exception
            result = await handle_call_tool(tool_name, arguments)
            
            # If we get here, the test failed (should have raised an exception)
            print(f"✗ {description}: Expected error but got result: {result}")
            all_passed = False
            
        except Exception as e:
            # Verify we got the expected type of error
            error_message = str(e)
            if expected_error.lower() in error_message.lower():
                print(f"✓ {description}: Correctly raised error")
                print(f"  Error: {error_message}")
            else:
                print(f"✗ {description}: Wrong error type")
                print(f"  Expected: {expected_error}")
                print(f"  Got: {error_message}")
                all_passed = False
    
    return all_passed

async def run_all_tests():
    """
    Run all test functions and report overall results.
    
    This function orchestrates all our tests and provides a summary
    of what passed and what failed.
    """
    print("Starting MCP Sum Server Tests")
    print("=" * 50)
    
    # Run all test functions
    test_results = []
    
    test_results.append(await test_list_tools())
    test_results.append(await test_sum_calculation())
    test_results.append(await test_error_handling())
    
    # Report overall results
    print("\n" + "=" * 50)
    print("Test Summary:")
    
    passed = sum(test_results)
    total = len(test_results)
    
    if passed == total:
        print(f"✓ All {total} test categories passed!")
        print("Your MCP server appears to be working correctly.")
        return True
    else:
        print(f"✗ {total - passed} out of {total} test categories failed.")
        print("Please review the errors above and fix any issues.")
        return False

def main():
    """
    Main function to run the tests.
    
    This handles the async event loop setup and provides a clean
    entry point for running the tests.
    """
    print("MCP Sum Server Test Suite")
    print("This script tests the core functionality of the MCP server.")
    print("Note: This tests the logic, not the full MCP protocol integration.\n")
    
    try:
        # Run all tests in an async context
        success = asyncio.run(run_all_tests())
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
How to use this test script:
===========================

1. Make sure you've installed the requirements:
   pip install -r requirements.txt

2. Run the tests:
   python test_server.py

3. Interpret the results:
   - ✓ marks indicate successful tests
   - ✗ marks indicate failed tests
   - The script will exit with code 0 if all tests pass, 1 if any fail

What this script tests:
======================

1. TOOL LISTING: Verifies the server can list its available tools
2. CALCULATION LOGIC: Tests the actual sum calculation with various inputs
3. ERROR HANDLING: Ensures proper error responses for invalid inputs

What this script DOESN'T test:
==============================

1. MCP PROTOCOL: This doesn't test the actual MCP message format
2. ASYNC COMMUNICATION: Doesn't test real client-server communication
3. STDIO TRANSPORT: Doesn't test the stdin/stdout communication
4. CONCURRENT REQUESTS: Doesn't test handling multiple simultaneous requests

For complete testing, you would need:
- An MCP client to test protocol compliance
- Integration tests with real MCP communication
- Performance tests under load
- Security tests with malicious inputs
"""