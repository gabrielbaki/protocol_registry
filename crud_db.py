import sqlite3
from flask import Flask, request, jsonify

DB_NAME = 'protocols_registry.db'
app = Flask(__name__)

# Create Operations
def create_workflow(name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO workflows (name) VALUES (?)", (name,))
        conn.commit()

def create_protocol(workflow_id, name, description):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO protocols (workflow_id, name, description) VALUES (?, ?, ?)", (workflow_id, name, description))
        conn.commit()

def create_step(protocol_id, parent_step_id, description, step_order):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO steps (protocol_id, parent_step_id, description, step_order) VALUES (?, ?, ?, ?)", (protocol_id, parent_step_id, description, step_order))
        conn.commit()

def create_parameter(step_id, name, value_type, value):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO parameters (step_id, name, value_type, value) VALUES (?, ?, ?, ?)", (step_id, name, value_type, value))
        conn.commit()

# Read Operations
def get_workflow_by_id(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workflows WHERE id=?", (id,))
        return cursor.fetchone()

def get_protocol_by_id(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM protocols WHERE id=?", (id,))
        return cursor.fetchone()

def get_step_by_id(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM steps WHERE id=?", (id,))
        return cursor.fetchone()

def get_parameter_by_id(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM parameters WHERE id=?", (id,))
        return cursor.fetchone()

# Update Operations
def update_workflow(id, name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE workflows SET name=? WHERE id=?", (name, id))
        conn.commit()

def update_protocol(id, workflow_id, name, description):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE protocols SET workflow_id=?, name=?, description=? WHERE id=?", (workflow_id, name, description, id))
        conn.commit()

def update_step(id, protocol_id, parent_step_id, description, step_order):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE steps SET protocol_id=?, parent_step_id=?, description=?, step_order=? WHERE id=?", (protocol_id, parent_step_id, description, step_order, id))
        conn.commit()

def update_parameter(id, step_id, name, value_type, value):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE parameters SET step_id=?, name=?, value_type=?, value=? WHERE id=?", (step_id, name, value_type, value, id))
        conn.commit()

# Delete Operations
def delete_workflow(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM workflows WHERE id=?", (id,))
        conn.commit()

def delete_protocol(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM protocols WHERE id=?", (id,))
        conn.commit()

def delete_step(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM steps WHERE id=?", (id,))
        conn.commit()

def delete_parameter(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM parameters WHERE id=?", (id,))
        conn.commit()

def get_all_protocols_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM protocols")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def delete_all_steps_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM steps")
        conn.commit()


def delete_all_protocols_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM protocols")
        conn.commit()


def get_all_steps():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM steps")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_all_parameters_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM parameters")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_steps_by_protocol_id(protocol_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM steps WHERE protocol_id=?", (protocol_id,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

# Additional Delete Operation
def delete_all_workflows():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM workflows")
        conn.commit()

def delete_all_parameters_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM parameters")
        conn.commit()

# API endpoints

@app.route('/workflows', methods=['POST'])
def add_workflow():
    name = request.json.get('name')
    create_workflow(name)
    return jsonify({"message": "Workflow created successfully!"}), 201

@app.route('/workflows/<int:id>', methods=['GET'])
def get_a_workflow(id):
    workflow = get_workflow_by_id(id)
    if workflow:
        return jsonify(workflow), 200
    else:
        return jsonify({"message": "Workflow not found!"}), 404

@app.route('/workflows', methods=['GET'])
def fetch_all_workflows():  # Renamed to avoid name conflict
    workflows = get_all_workflows_db()
    if workflows:
        return jsonify(workflows), 200
    else:
        return jsonify({"message": "No workflows found!"}), 404

def get_all_workflows_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row  # This allows you to return rows as dictionaries
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workflows")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]  # Convert rows to dictionaries


@app.route('/workflows/<int:id>', methods=['PUT'])
def modify_workflow(id):
    name = request.json.get('name')
    update_workflow(id, name)
    return jsonify({"message": "Workflow updated successfully!"}), 200

@app.route('/workflows/<int:id>', methods=['DELETE'])
def remove_workflow(id):
    delete_workflow(id)
    return jsonify({"message": "Workflow deleted successfully!"}), 200

@app.route('/workflows', methods=['DELETE'])
def remove_all_workflows():
    delete_all_workflows()
    return jsonify({"message": "All workflows deleted successfully!"}), 200


@app.route('/protocols/<int:id>', methods=['GET'])
def get_a_protocol(id):
    protocol = get_protocol_by_id(id)
    if protocol:
        return jsonify(protocol), 200
    else:
        return jsonify({"message": "Protocol not found!"}), 404

@app.route('/protocols', methods=['GET'])
def get_all_protocols():
    protocols = get_all_protocols_db()
    if protocols:
        return jsonify(protocols), 200
    else:
        return jsonify({"message": "No protocols found!"}), 404

@app.route('/protocols', methods=['DELETE'])
def delete_all_protocols():
    delete_all_protocols_db()
    return jsonify({"message": "All protocols deleted successfully!"}), 200

@app.route('/protocols/<int:id>', methods=['PUT'])
def modify_protocol(id):
    workflow_id = request.json.get('workflow_id')
    name = request.json.get('name')
    description = request.json.get('description')
    update_protocol(id, workflow_id, name, description)
    return jsonify({"message": "Protocol updated successfully!"}), 200

@app.route('/protocols/<int:id>', methods=['DELETE'])
def remove_protocol(id):
    delete_protocol(id)
    return jsonify({"message": "Protocol deleted successfully!"}), 200

@app.route('/steps/<int:id>', methods=['GET'])
def get_a_step(id):
    step = get_step_by_id(id)
    if step:
        return jsonify(step), 200
    else:
        return jsonify({"message": "Step not found!"}), 404

@app.route('/steps', methods=['GET'])
def get_all_steps():
    steps = get_all_steps()
    if steps:
        return jsonify(steps), 200
    else:
        return jsonify({"message": "No steps found!"}), 404

@app.route('/steps', methods=['DELETE'])
def delete_all_steps():
    delete_all_steps_db()
    return jsonify({"message": "All steps deleted successfully!"}), 200

@app.route('/steps/<int:id>', methods=['PUT'])
def modify_step(id):
    protocol_id = request.json.get('protocol_id')
    parent_step_id = request.json.get('parent_step_id')
    description = request.json.get('description')
    step_order = request.json.get('step_order')
    update_step(id, protocol_id, parent_step_id, description, step_order)
    return jsonify({"message": "Step updated successfully!"}), 200

@app.route('/steps/<int:id>', methods=['DELETE'])
def remove_step(id):
    delete_step(id)
    return jsonify({"message": "Step deleted successfully!"}), 200

@app.route('/steps/protocol_id/<int:protocol_id>', methods=['GET'])
def get_steps_by_protocol(protocol_id):
    steps = get_steps_by_protocol_id(protocol_id)
    if steps:
        return jsonify(steps), 200
    else:
        return jsonify({"message": "No steps found for this protocol!"}), 404

@app.route('/parameters/<int:id>', methods=['GET'])
def get_a_parameter(id):
    parameter = get_parameter_by_id(id)
    if parameter:
        return jsonify(parameter), 200
    else:
        return jsonify({"message": "Parameter not found!"}), 404

@app.route('/parameters', methods=['GET'])
def get_all_parameters():
    parameters = get_all_parameters_db()
    if parameters:
        return jsonify(parameters), 200
    else:
        return jsonify({"message": "No parameters found!"}), 404

@app.route('/parameters', methods=['DELETE'])
def delete_all_parameters():
    delete_all_parameters_db()
    return jsonify({"message": "All parameters deleted successfully!"}), 200


@app.route('/parameters/<int:id>', methods=['PUT'])
def modify_parameter(id):
    step_id = request.json.get('step_id')
    name = request.json.get('name')
    value_type = request.json.get('value_type')
    value = request.json.get('value')
    update_parameter(id, step_id, name, value_type, value)
    return jsonify({"message": "Parameter updated successfully!"}), 200

@app.route('/parameters/<int:id>', methods=['DELETE'])
def remove_parameter(id):
    delete_parameter(id)
    return jsonify({"message": "Parameter deleted successfully!"}), 200

@app.route('/protocols', methods=['POST'])
def add_protocol():
    workflow_id = request.json.get('workflow_id')
    name = request.json.get('name')
    description = request.json.get('description')
    create_protocol(workflow_id, name, description)
    return jsonify({"message": "Protocol created successfully!"}), 201

@app.route('/steps', methods=['POST'])
def add_step():
    protocol_id = request.json.get('protocol_id')
    parent_step_id = request.json.get('parent_step_id')
    description = request.json.get('description')
    step_order = request.json.get('step_order')
    create_step(protocol_id, parent_step_id, description, step_order)
    return jsonify({"message": "Step created successfully!"}), 201

@app.route('/parameters', methods=['POST'])
def add_parameter():
    step_id = request.json.get('step_id')
    name = request.json.get('name')
    value_type = request.json.get('value_type')
    value = request.json.get('value')
    create_parameter(step_id, name, value_type, value)
    return jsonify({"message": "Parameter created successfully!"}), 201


if __name__ == "__main__":
    app.run(debug=True)