import requests
import datetime
import os

PROMETHEUS_URL = "http://prometheus:9090"

QUERIES = {
    "CPU Usage (%)": '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)',
    "Memory Usage (%)": '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100',
    "Disk Usage (%)": '100 - ((node_filesystem_avail_bytes * 100) / node_filesystem_size_bytes)',
    "App Status": 'up{job="cloudops-app"}',
    "Node Exporter Status": 'up{job="node-exporter"}',
}

def query(query):
    try:
        r = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": query},
            timeout=10,
        )
        r.raise_for_status()
        result = r.json()["data"]["result"]

        if not result:
            return None

        return float(result[0]["value"][1])

    except Exception:
        return None


def status(v):
    return "UP" if v == 1 else "DOWN"


now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

os.makedirs("ai-engine/reports", exist_ok=True)

report_file = f"ai-engine/reports/health_report_{timestamp}.txt"

lines = []

lines.append("=" * 60)
lines.append("CloudOps AI Health Report")
lines.append("=" * 60)
lines.append(f"Generated: {now}")
lines.append("")

cpu = query(QUERIES["CPU Usage (%)"])
memory = query(QUERIES["Memory Usage (%)"])
disk = query(QUERIES["Disk Usage (%)"])
app = query(QUERIES["App Status"])
node = query(QUERIES["Node Exporter Status"])

if cpu is not None:
    lines.append(f"CPU Usage           : {cpu:.2f}%")

if memory is not None:
    lines.append(f"Memory Usage        : {memory:.2f}%")

if disk is not None:
    lines.append(f"Disk Usage          : {disk:.2f}%")

lines.append(f"Application Status  : {status(app) if app is not None else 'Unknown'}")
lines.append(f"Node Exporter       : {status(node) if node is not None else 'Unknown'}")

lines.append("")
lines.append("Recommendation")
lines.append("-" * 60)

if app != 1:
    lines.append("❌ Application is DOWN. Restart immediately.")
elif cpu is not None and cpu > 80:
    lines.append("⚠ High CPU usage detected.")
elif memory is not None and memory > 85:
    lines.append("⚠ High Memory usage detected.")
elif disk is not None and disk > 85:
    lines.append("⚠ Disk almost full.")
else:
    lines.append("✅ System is healthy.")

lines.append("=" * 60)

report = "\n".join(lines)

print(report)

with open(report_file, "w") as f:
    f.write(report)

print(f"\nReport saved to: {report_file}")
