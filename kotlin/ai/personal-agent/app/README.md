setx OPENAI_API_KEY "your_api_key_here"



Add this to the claude_desktop_config.json file in C:\Users\vedicmonk\AppData\Roaming\Claude

```json
{
  "mcpServers": {
    "todoist": {
      "command": "java",
      "args": [
        "-jar",
        "C:\\ssd_cache\\mcp\\app-all.jar"
      ]
    }
  }
}
```


Doesn't work
```json
{
  "mcpServers": {
    "todoist": {
      "url": "http://localhost:8090/mcp"
    }
  }
}
```