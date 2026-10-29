# 🐳 Docker Lifecycle Manager & Observability MCP Server

A production-ready **Model Context Protocol (MCP)** server built with Python (`FastMCP`) and the official Docker SDK. This project bridges LLM clients (such as Claude Desktop and Cursor) with your local Docker daemon, allowing AI agents to securely query container states, spin up services, inspect logs, and manage container lifecycles through natural language.

---

## 🚀 Features

* **Container Fleet Auditing:** Inspect running and stopped containers, image tags, status, and port bindings.
* **Automated Container Provisioning:** Dynamically pull and spin up new Docker containers on demand.
* **Lifecycle Management:** Gracefully start, stop, and restart containers via structured tool calls.
* **Real-time Log Extraction:** Fetch tail logs from containers to let AI agents debug stack traces and runtime errors.
* **Cross-Platform Transport:** Built using standard input/output (`stdio`) transport for seamless integration with local developer LLM environments.

---

## 🛠️ Tech Stack & Requirements

* **Python 3.10+**
* **FastMCP** (MCP Python framework)
* **Docker SDK for Python** (`docker`)
* **Docker Desktop** (Running locally with Windows named pipe or Unix socket access)

---

## 📂 Project Structure

```text
docker-mcp-observability/
├── .venv/               # Python virtual environment
├── server.py            # Core FastMCP server implementation
└── README.md            # Project documentation