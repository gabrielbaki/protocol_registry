import unittest
import sqlite3
from crud_db import app
from flask import Flask

class TestDBOperations(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect('protocols_registry.db')
        self.cursor = self.conn.cursor()
        self.client = app.test_client()

    def tearDown(self):
        # Clear the database after each test
        for table in ['parameters', 'steps', 'protocols', 'workflows']:  # Note: order matters due to foreign key constraints
            self.cursor.execute(f"DELETE FROM {table}")
        self.conn.commit()
        self.conn.close()
        self.client = None

    def test_workflow(self):
        # CREATE
        response = self.client.post('/workflows', json={"name": "Test Workflow"})
        self.assertEqual(response.status_code, 201)
        
        # READ
        response = self.client.get('/workflows/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data[1], "Test Workflow")
        
        # UPDATE
        response = self.client.put('/workflows/1', json={"name": "Updated Workflow"})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/workflows/1')
        data = response.get_json()
        self.assertEqual(data[1], "Updated Workflow")
        
        # DELETE
        response = self.client.delete('/workflows/1')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/workflows/1')
        self.assertEqual(response.status_code, 404)

    # Similarly, you can create tests for protocols, steps, and parameters using the structure above.
    def test_protocol(self):
        # CREATE
        response = self.client.post('/protocols', json={"workflow_id": 1, "name": "Test Protocol", "description": "This is a test protocol"})
        self.assertEqual(response.status_code, 201)
        
        # READ
        response = self.client.get('/protocols/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data[2], "Test Protocol")
        
        # UPDATE
        response = self.client.put('/protocols/1', json={"workflow_id": 1, "name": "Updated Protocol", "description": "This is an updated protocol"})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/protocols/1')
        data = response.get_json()
        self.assertEqual(data[2], "Updated Protocol")
        
        # DELETE
        response = self.client.delete('/protocols/1')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/protocols/1')
        self.assertEqual(response.status_code, 404)

    def test_step(self):
        # CREATE
        response = self.client.post('/steps', json={"protocol_id": 1, "parent_step_id": 1, "description": "This is a test step", "step_order": 1})
        self.assertEqual(response.status_code, 201)
        
        # READ
        response = self.client.get('/steps/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data[3], "This is a test step")
        
        # UPDATE
        response = self.client.put('/steps/1', json={"protocol_id": 1, "parent_step_id": 1, "description": "This is an updated step", "step_order": 1})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/steps/1')
        data = response.get_json()
        self.assertEqual(data[3], "This is an updated step")
        
        # DELETE
        response = self.client.delete('/steps/1')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/steps/1')
        self.assertEqual(response.status_code, 404)

    def test_parameter(self):
        # CREATE
        response = self.client.post('/parameters', json={"step_id": 1, "name": "Test Parameter", "value_type": "string", "value": "test"})
        self.assertEqual(response.status_code, 201)
        
        # READ
        response = self.client.get('/parameters/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data[2], "Test Parameter")
        
        # UPDATE
        response = self.client.put('/parameters/1', json={"step_id": 1, "name": "Updated Parameter", "value_type": "string", "value": "updated"})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/parameters/1')
        data = response.get_json()
        self.assertEqual(data[2], "Updated Parameter")
        
        # DELETE
        response = self.client.delete('/parameters/1')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/parameters/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
