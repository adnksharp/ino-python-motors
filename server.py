from flask import Flask, request, jsonify
import numpy as np
import threading
import time
from pymongo import MongoClient

thrlock = threading.Lock()

rtd = 2 * np.pi
dtr = 1 / rtd

mongo = {
    'uri': 'mongodb://localhost:27017/',
    'db': 'motors',
    'collect': 'project'
}


device = {
    '0': {
        'pos': 0.0, 
        'IErr': 0.0, 
        'lstErr': 0.0, 
        'lstTime': 
        time.time()
        },
    '1': {
        'pos': 0.0, 
        'IErr': 0.0, 
        'lstErr': 0.0, 
        'lstTime': time.time()
    }
}

ref = {
    '0': {
        'rev': 0.0,
        'rad': 0.0
        },
    '1': {
        'rev': 0.0,
        'rad': 0.0
    }
}

maxSREV = 0.45 
maxSRAD = maxSREV * rtd
maxMV = 12.0
minMV = 1.5

kPM, kIM, kDM = 0.6168, 1.1387, 0.1000
kPS, kIS, kDS = 0.1364, 0.2750, 0.0100

def save(ID, POS, OUT):
    try:
        data_entry = {
            "timestamp": time.time(),
            "ID": ID,
            "POS": POS,
            "OUT": OUT
        }
        collection.insert_one(data_entry)
    except Exception as e:
        print(f"Error al guardar datos en MongoDB: {e}")

def calcPID(ID, Kp, Ki, Kd, ref, maxy):
    state = device[ID]
    
    posRAD = state['pos']
    errI = state['IErr']
    errLast = state['lstErr']
    
    now = time.time()
    dt = now - state['lstTime']

    if dt == 0:
        return 0.0
    
    error = ref - posRAD

    if ID == '0':
        error = round(error, 2)

        if error == 0:
            state['lstErr'] = 0.0
            state['IErr'] = 0.0
            device[ID] = state
            return 0.0

    outP = Kp * error
    
    errI += error * dt
    outI = Ki * errI
    
    outD = Kd * (error - errLast) / dt
    
    action = outP + outI + outD
    
    clip = np.clip(action, -maxy, maxy)

    if action != clip:
        errI -= error * dt 
        outI = Ki * errI
        action = outP + outI + outD
        clip = np.clip(action, -maxy, maxy) 

    state['IErr'] = errI
    state['lstErr'] = error
    state['lstTime'] = now
    
    device[ID] = state
    
    return clip

def setMotor(ID, posREV):
    posRAD = posREV * rtd
    
    with thrlock:
        radRef = ref[ID]['rad']
        revRef = ref[ID]['rev']
    device[ID]['pos'] = posRAD
    
    cmd = calcPID(
        ID, kPM, kIM, kDM, radRef, maxMV
    )

    if abs(cmd) > 0 and abs(cmd) < minMV:
        if cmd > 0:
            cmd = minMV
        else:
            cmd = -minMV
    cmd = np.clip(cmd, -maxMV, maxMV)
    
    print(f"[{ID}] POS: [{posREV:.2f} rev | {posRAD:.2f} rad] WRK: [{cmd:.4f} V] REF: [{revRef:.2f} rev | {radRef:.2f} rad]")
    dbson = {"TYPE": "VOLTAGE", "VAL": cmd}
    save(ID, posREV, dbson)
    
    return jsonify({
        "status": "success", 
        "device_id": ID, 
        "action_type": "voltage",
        "voltage": cmd 
    }), 200

def setServo(ID, posREV):
    posRAD = posREV * rtd
    
    with thrlock:
        radRef = ref[ID]['rad']
        revRef = ref[ID]['rev']
    device[ID]['pos'] = posRAD
    
    cmdRAD = calcPID(
        ID, kPS, kIS, kDS, radRef, maxSRAD
    )
    
    cmdREV = cmdRAD * dtr

    print(f"[{ID}] POS: [{posREV:.2f} rev | {posRAD:.2f} rad] WRK: [{cmdREV:.4f} rev  | {cmdRAD:.2f} rad] REF: [{revRef:.2f} rev | {radRef:.2f} rad]")
    dbson = {"TYPE": "POSITION", "VAL": cmdREV}
    save(ID, posREV, dbson)

    return jsonify({
        "status": "success", 
        "device_id": ID, 
        "action_type": "position",
        "position": cmdREV 
    }), 200

app = Flask(__name__)

@app.route('/enc_status', methods=['POST'])
def receive_data():
    if not request.is_json:
        return jsonify({"status": "error"}), 400

    data = request.get_json()
    ID = data.get('id')
    posREV = data.get('position')
    
    if ID is None or posREV is None:
        return jsonify({"status": "error"}), 400

    try:
        posREV = float(posREV)
    except ValueError:
        return jsonify({"status": "error"}), 406

    if ID == '0':
        return setMotor(ID, posREV)
    
    elif ID == '1':
        return setServo(ID, posREV)
    
    else:
        return jsonify({"status": "error"}), 401

@app.route('/ref_cmd', methods=['POST'])
def set_reference():
    if not request.is_json:
        return jsonify({"status": "error"}), 400

    data = request.get_json()
    
    ID = data.get('id')
    newrev = data.get('ref')
    
    if ID is None or newrev is None:
        return jsonify({"status": "error"}), 400
    
    if ID not in ref:
        return jsonify({"status": "error"}), 401

    try:
        newrev = float(newrev)
    except ValueError:
        return jsonify({"status": "error"}), 406

    newrad = newrev * rtd
    
    with thrlock:
        ref[ID]['rev'] = newrev
        ref[ID]['rad'] = newrad

    return jsonify({
        "status": "success",
        "message": f"{ID} updated.",
        "new": newrev
    }), 200

if __name__ == '__main__':
    import logging
    try:
        client = MongoClient(mongo['uri'])
        db = client[mongo['db']]
        collection = db[mongo['collect']]
        print(f' * MONGODB OK')
    except Exception as e:
        print(f' * MONGODB FAIL')
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app.run(host='0.0.0.0', port=5000)
