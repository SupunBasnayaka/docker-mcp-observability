import os
import docker
from fastmcp import FastMCP

# Initialize FastMCP server instance
mcp = FastMCP("Docker Lifecycle Manager 🐳")

# Initialize Docker client with explicit Windows named pipe support
try:
    if os.name == 'nt':
        # Explicitly configure the Windows named pipe for Docker Desktop
        docker_client = docker.DockerClient(base_url='npipe:////./pipe/docker_engine')
    else:
        docker_client = docker.from_env()
except Exception as e:
    docker_client = None

@mcp.tool()
def list_containers(all_containers: bool = True) -> list:
    """List Docker containers, their current status, and image details. 
    Set all_containers to True to see stopped containers as well."""
    if not docker_client:
        return [{"error": "Docker daemon is not accessible or running."}]
    
    try:
        containers = docker_client.containers.list(all=all_containers)
        summary = []
        for c in containers:
            summary.append({
                "id": c.short_id,
                "name": c.name,
                "status": c.status,
                "image": c.image.tags[0] if c.image.tags else "unknown",
                "ports": c.ports
            })
        return summary
    except Exception as e:
        return [{"error": f"Failed to list containers: {str(e)}"}]

@mcp.tool()
def run_container(image_name: str, container_name: str = None, detach: bool = True) -> dict:
    """Pull (if needed) and run a new Docker container from a specified image."""
    if not docker_client:
        return {"error": "Docker daemon is not accessible or running."}
    
    try:
        # Check if image exists locally, pull if not
        try:
            docker_client.images.get(image_name)
        except docker.errors.ImageNotFound:
            docker_client.images.pull(image_name)
            
        # Run the container
        container = docker_client.containers.run(
            image=image_name,
            name=container_name,
            detach=detach
        )
        return {
            "success": True,
            "message": f"Container successfully started.",
            "id": container.short_id,
            "name": container.name,
            "status": container.status
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def stop_container(container_id_or_name: str) -> dict:
    """Gracefully stop a running Docker container using its name or ID."""
    if not docker_client:
        return {"error": "Docker daemon is not accessible or running."}
    
    try:
        container = docker_client.containers.get(container_id_or_name)
        container.stop()
        return {
            "success": True,
            "message": f"Container '{container.name}' ({container.short_id}) has been stopped."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def restart_container(container_id_or_name: str) -> dict:
    """Restart a Docker container using its name or ID."""
    if not docker_client:
        return {"error": "Docker daemon is not accessible or running."}
    
    try:
        container = docker_client.containers.get(container_id_or_name)
        container.restart()
        return {
            "success": True,
            "message": f"Container '{container.name}' ({container.short_id}) has been restarted."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_container_logs(container_id_or_name: str, tail_lines: int = 50) -> dict:
    """Fetch recent log output from a container for debugging and observability."""
    if not docker_client:
        return {"error": "Docker daemon is not accessible or running."}
    
    try:
        container = docker_client.containers.get(container_id_or_name)
        logs = container.logs(tail=tail_lines).decode('utf-8', errors='ignore')
        return {
            "container": container.name,
            "logs": logs
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()