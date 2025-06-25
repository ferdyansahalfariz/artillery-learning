import json
import pandas as pd
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import sys
import os

# --- Load JSON file ---
if len(sys.argv) < 2:
    print("❌ Usage: python generate_report.py <result.json>")
    sys.exit(1)

input_json = sys.argv[1]
basename = os.path.splitext(os.path.basename(input_json))[0]
output_html_path = f"results-html/report-{basename}.html"

with open(input_json) as f:
    data = json.load(f)

intermediate = data['intermediate']
aggregate = data['aggregate']

# --- Build time-series DataFrame ---
rows = []
for entry in intermediate:
    ts = datetime.fromtimestamp(entry['firstMetricAt'] / 1000)

     # Cek apakah summary dan http.response_time tersedia
    summaries = entry.get('summaries', {})
    http_resp = summaries.get('http.response_time')

    if http_resp is None:
        print(f"⚠️ Warning: No 'http.response_time' in entry at timestamp {ts}")
        continue  # skip entry ini

    latency = entry['summaries']['http.response_time']['mean']
    rps = entry['rates'].get('http.request_rate', 0)
    users = entry['counters'].get('vusers.created', 0)
    rows.append({
        'timestamp': ts,
        'latency': latency,
        'rps': rps,
        'users': users
    })

df = pd.DataFrame(rows)

# --- Build charts ---
def make_plot(df, y, title, y_label, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df[y],
                             mode='lines+markers',
                             name=y_label,
                             line=dict(color=color)))
    fig.update_layout(title=title, xaxis_title='Time', yaxis_title=y_label)
    return fig.to_json()

latency_plot = make_plot(df, 'latency', "Mean Latency Over Time", "Latency (ms)", "blue")
rps_plot = make_plot(df, 'rps', "Requests Per Second (RPS)", "RPS", "green")
users_plot = make_plot(df, 'users', "Concurrent Virtual Users", "Users", "orange")

# --- Pie charts ---
http_codes = {k.split('.')[-1]: v for k, v in aggregate['counters'].items() if k.startswith('http.codes.')}
http_code_chart = go.Figure([go.Pie(labels=list(http_codes.keys()), values=list(http_codes.values()))])
http_code_chart.update_layout(title="HTTP Status Code Distribution")
http_code_plot = http_code_chart.to_json()

logical_errors = {k[7:]: v for k, v in aggregate['counters'].items() if k.startswith('errors.')}
custom_error_chart = go.Figure([go.Pie(labels=list(logical_errors.keys()), values=list(logical_errors.values()))])
custom_error_chart.update_layout(title="Logical / Application Errors")
custom_error_plot = custom_error_chart.to_json()

# --- Statistics Table (per interval) ---
stats_table = []
for entry in intermediate:
    summaries = entry.get('summaries', {})
    http_resp = summaries.get('http.response_time')
    if http_resp is None:
        continue
    
    stats_table.append({
        "time": datetime.fromtimestamp(entry['firstMetricAt'] / 1000).strftime('%H:%M:%S'),
        "latency": round(entry['summaries']['http.response_time']['mean'], 2),
        "rps": round(entry['rates'].get('http.request_rate', 0), 2),
        "users": entry['counters'].get('vusers.created', 0)
    })

# # --- Errors Table ---
# errors_table = []
# for k, v in aggregate['counters'].items():
#     if k.startswith('http.codes.') or k.startswith('errors.'):
#         errors_table.append({
#             "type": k,
#             "count": v
#         })
# --- Errors Table ---
errors_table = []
for k, v in aggregate['counters'].items():
    if k.startswith('errors.'):
        errors_table.append({
            "type": k[7:],  # remove "errors." prefix for cleaner label
            "count": v
        })

# --- Summary Info ---
summary = {
    "start_time": datetime.fromtimestamp(aggregate['firstMetricAt'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
    "end_time": datetime.fromtimestamp(aggregate['lastMetricAt'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
    "duration_sec": (aggregate['lastMetricAt'] - aggregate['firstMetricAt']) // 1000,
    "total_requests": aggregate['counters'].get('http.requests', 0),
    "total_vusers": aggregate['counters'].get('vusers.created', 0),
    "completed": aggregate['counters'].get('vusers.completed', 0),
    "failed": aggregate['counters'].get('vusers.failed', 0)
}

# --- Render HTML ---
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('jmeter_style_report.html')

output_html = template.render(
    summary=summary,
    latency_plot=latency_plot,
    rps_plot=rps_plot,
    users_plot=users_plot,
    http_code_plot=http_code_plot,
    custom_error_plot=custom_error_plot,
    stats_table=stats_table,
    errors_table=errors_table
)

with open(output_html_path, 'w') as f:
    f.write(output_html)

print(f"✅ Report generated: {output_html_path}")
