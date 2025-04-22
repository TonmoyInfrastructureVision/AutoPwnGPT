# API Documentation

This documentation covers the AutoPwnGPT API, which allows programmatic access to the framework's functionality.

## API Overview

AutoPwnGPT provides a RESTful API that enables integration with other security tools and automation workflows. The API follows standard REST conventions and uses JSON for data exchange.

## Authentication

API requests must be authenticated using an API key. You can generate an API key in the settings menu of the AutoPwnGPT GUI or using the CLI:

```bash
python src/cli.py --generate-api-key
```

Include the API key in the `X-API-Key` header with all requests:

```
X-API-Key: your-api-key-here
```

## API Endpoints

### Session Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/sessions` | GET | List all sessions |
| `/api/v1/sessions` | POST | Create a new session |
| `/api/v1/sessions/{session_id}` | GET | Get session details |
| `/api/v1/sessions/{session_id}` | DELETE | Delete a session |

### Module Operations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/modules` | GET | List all available modules |
| `/api/v1/modules/{module_name}` | GET | Get module details |
| `/api/v1/modules/{module_name}/run` | POST | Execute a module |

### Command Interface

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/sessions/{session_id}/command` | POST | Execute a natural language command |
| `/api/v1/sessions/{session_id}/history` | GET | Get command history |

### Results and Reports

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/sessions/{session_id}/results` | GET | Get session results |
| `/api/v1/sessions/{session_id}/report` | GET | Generate a report |

## Request and Response Examples

### Creating a Session

**Request:**

```http
POST /api/v1/sessions HTTP/1.1
Host: localhost:8080
Content-Type: application/json
X-API-Key: your-api-key-here

{
  "name": "Target Network Assessment",
  "description": "Security assessment of the target network",
  "scope": ["192.168.1.0/24"]
}
```

**Response:**

```json
{
  "session_id": "s12345",
  "name": "Target Network Assessment",
  "description": "Security assessment of the target network",
  "scope": ["192.168.1.0/24"],
  "created_at": "2025-04-22T10:00:00Z",
  "status": "active"
}
```

### Running a Module

**Request:**

```http
POST /api/v1/modules/network_scanner/run HTTP/1.1
Host: localhost:8080
Content-Type: application/json
X-API-Key: your-api-key-here

{
  "session_id": "s12345",
  "parameters": {
    "target": "192.168.1.0/24",
    "ports": "1-1000",
    "timeout": 30
  }
}
```

**Response:**

```json
{
  "task_id": "t67890",
  "status": "running",
  "estimated_completion": "2025-04-22T10:05:00Z"
}
```

### Executing a Command

**Request:**

```http
POST /api/v1/sessions/s12345/command HTTP/1.1
Host: localhost:8080
Content-Type: application/json
X-API-Key: your-api-key-here

{
  "command": "scan network 192.168.1.0/24 for web servers"
}
```

**Response:**

```json
{
  "command_id": "c24680",
  "status": "processing",
  "parsed_intent": {
    "action": "scan",
    "target_type": "network",
    "target": "192.168.1.0/24",
    "filter": "web servers"
  }
}
```

## Error Handling

The API uses standard HTTP status codes to indicate success or failure:

- `200 OK`: The request was successful
- `201 Created`: A resource was successfully created
- `400 Bad Request`: The request was invalid
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: The request is not allowed
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

Error responses include a JSON body with details:

```json
{
  "error": {
    "code": "invalid_parameter",
    "message": "The parameter 'target' is required",
    "details": {
      "parameter": "target"
    }
  }
}
```

## Rate Limiting

API requests are rate-limited to prevent abuse. The current limits are:

- 100 requests per minute per API key
- 1000 requests per hour per API key

The response headers include rate limit information:

```
X-Rate-Limit-Limit: 100
X-Rate-Limit-Remaining: 95
X-Rate-Limit-Reset: 1650960000
```

## API Client Libraries

We provide client libraries for various programming languages:

- [Python Client](https://github.com/TonmoyInfrastructureVision/autopwngpt-python-client)
- [JavaScript Client](https://github.com/TonmoyInfrastructureVision/autopwngpt-js-client)

## Webhooks

You can configure webhooks to receive notifications about events in your sessions:

- Module completion
- Vulnerability discovery
- Report generation

Configure webhooks in the API settings or using the API itself.

---

Author: Eshan Roy  
Email: m.eshanized@gmail.com  
GitHub: https://github.com/TonmoyInfrastructureVision
