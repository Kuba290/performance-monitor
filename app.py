from flask import Flask, jsonify, render_template
import psutil
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    data = {
        'cpu_percent': psutil.cpu_percent(1),
        'cpu_frequency': psutil.cpu_freq().current,
        'cpu_count': psutil.cpu_count(),
        'ram': {
            'total': psutil.virtual_memory().total,
            'available': psutil.virtual_memory().available,
            'percent': psutil.virtual_memory().percent
        },
        'swap': {
            'total': psutil.swap_memory().total,
            'used': psutil.swap_memory().used,
            'free': psutil.swap_memory().free,
            'percent': psutil.swap_memory().percent
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'free': psutil.disk_usage('/').free,
            'percent': psutil.disk_usage('/').percent
        },
        'network': {
            'bytes_sent': psutil.net_io_counters().bytes_sent,
            'bytes_received': psutil.net_io_counters().bytes_recv,
            'packets_sent': psutil.net_io_counters().packets_sent,
            'packets_received': psutil.net_io_counters().packets_recv,
        },
        'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        'temperature': None
    }

    if hasattr(psutil, "sensors_temperatures"):
        try:
            sensors = psutil.sensors_temperatures()
            if "cpu_thermal" in sensors and sensors["cpu_thermal"]:
                data['temperature'] = sensors["cpu_thermal"][0].current
        except Exception:
            pass

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)