import requests
import datetime

PROMETHEUS_URL = "http://localhost:9090"

QUERIES = {
    "CPU Usage (%)": '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)',
    "Memory Usage (%)": '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100',
    "Disk Usage (%)": '100 - ((node_filesystem_avail_bytes{mountpoint="/"} * 100) / node_filesystem_size_bytes{mountpoint="/"})',
    "App Status": 'up{job="cloudops-app"}',
    "Node Exporter Status": 'up{job="node-exporter"}',
}

def query_prometheus(query):
    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": query},
        timeout=10
    )
    response.raise_for_status()
    result = response.json()["data"]["result"]

    if not result:
        return None

    return float(result[0]["value"][1])

def status_text(value):
    return "UP" if value == 1 else "DOWN"

def main():
    report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 50)
    print("CloudOps AI Health Report")
    print("=" * 50)
    print(f"Generated At: {report_time}")
    print("-" * 50)

    for name, query in QUERIES.items():
        value = query_prometheus(query)

        if value is None:
            print(f"{name}: No data")
            continue

        if "Status" in name:
            print(f"{name}: {status_text(value)}")
        else:
            print(f"{name}: {value:.2f}%")

    print("-" * 50)
    print("Recommendation:")

    cpu = query_prometheus(QUERIES["CPU Usage (%)"])
    memory = query_prometheus(QUERIES["Memory Usage (%)"])
    disk = query_prometheus(QUERIES["Disk Usage (%)"])
    app = query_prometheus(QUERIES["App Status"])

    if app != 1:
        print("Critical: Flask application is DOWN. Restart immediately.")
    elif cpu and cpu > 80:
        print("Warning: CPU usage is high. Check running processes.")
    elif memory and memory > 85:
        print("Warning: Memory usage is high. Check container/resource usage.")
    elif disk and disk > 85:
        print("Warning: Disk usage is high. Clean logs and unused Docker images.")
    else:
        print("System is healthy. No immediate action required.")

    print("=" * 50)

if __name__ == "__main__":
    main()
