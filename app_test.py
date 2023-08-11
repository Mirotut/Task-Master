import unittest
from app import app, db, Todo
from flask import current_app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_existing_task(self):
        task = Todo(content='new task to check buttons')
        db.session.add(task)
        db.session.commit()

        response = self.app.post('/', data={'content': 'new task to check buttons'})
        self.assertIn('This task exists!', response.data.decode('utf-8'))

    def test_add_blank_task(self):
        response = self.app.post('/', data={'content': ''})
        self.assertIn('No new task added!', response.data.decode('utf-8'))

    def test_delete_task(self):
        task = Todo(content='task to be deleted')
        db.session.add(task)
        db.session.commit()

        response = self.app.get(f'/delete/{task.id}')
        self.assertEqual(response.status_code, 302)  # Check if the redirect works

        deleted_task = Todo.query.get(task.id)
        self.assertIsNone(deleted_task)

    def test_update_task(self):
        task = Todo(content='task to be updated')
        db.session.add(task)
        db.session.commit()

        response = self.app.post(f'/update/{task.id}', data={'content': 'updated task'})
        self.assertEqual(response.status_code, 302)  # Check if the redirect works

        updated_task = Todo.query.get(task.id)
        self.assertEqual(updated_task.content, 'updated task')

if __name__ == '__main__':
    unittest.main()
