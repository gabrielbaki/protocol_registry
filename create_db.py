import sqlite3

def create_db():
    conn = sqlite3.connect('protocols_registry.db')
    cursor = conn.cursor()

    # Workflows table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS workflows (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    ''')

    # Protocols table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS protocols (
        id INTEGER PRIMARY KEY,
        workflow_id INTEGER REFERENCES workflows(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        description TEXT
    );
    ''')

    # Steps table (with self-referencing foreign key for parent/child relationships)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS steps (
        id INTEGER PRIMARY KEY,
        protocol_id INTEGER REFERENCES protocols(id) ON DELETE CASCADE,
        parent_step_id INTEGER REFERENCES steps(id) ON DELETE CASCADE,
        description TEXT NOT NULL,
        step_order INTEGER NOT NULL
    );
    ''')

    # Parameters table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parameters (
        id INTEGER PRIMARY KEY,
        step_id INTEGER REFERENCES steps(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        value_type TEXT NOT NULL,  -- can be "numeric" or "categorical"
        value TEXT NOT NULL
    );
    ''')

    conn.commit()
    conn.close()

create_db()
