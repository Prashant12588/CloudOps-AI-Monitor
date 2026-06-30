import requests
import statistics
import datetime
import time

PROMETHEUS_URL = "http://prometheus:9090"

QUERIES = {
    "cpu_usage_percent": '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)',
    "memory_usage_percent": '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100',
}

def query_prometheus_range(query):
    end = int(time.time())
    start = end - 300

    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query_range",
        params={
            "query": query,
            "start": start,
            "end": end,
            "step": "30s"
        },
        timeout=10
    )
    response.raise_for_status()
    data = response.json()["data"]["result"]

    if not data:
        return []

    return [float(point[1]) for point in data[0]["values"]]

def detect_anomaly(metric_name, values):
    if len(values) < 3:
        return f"✅ {metric_name}: Not enough historical data"

    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    latest = values[-1]

    if stdev == 0:
        return f"✅ {metric_name}: stable at {latest:.2f}%"

    z_score = abs((latest - mean) / stdev)

    if z_score > 2:
        return f"🚨 {metric_name}: anomaly detected | latest={latest:.2f}% avg={mean:.2f}% z={z_score:.2f}"

    return f"✅ {metric_name}: normal | latest={latest:.2f}% avg={mean:.2f}% z={z_score:.2f}"

def main():
    print(f"CloudOps AI Anomaly Report - {datetime.datetime.now()}")

    for metric_name, query in QUERIES.items():
        values = query_prometheus_range(query)
        print(detect_anomaly(metric_name, values))

if __name__ == "__main__":
    main()
