import unittest
import json
from app import app  # Import your Flask app instance

class RecommendationAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up test client
        cls.client = app.test_client()
        cls.client.testing = True

    def test_index(self):
        """Test the index route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'API is working!')

    def test_recommendation_invalid_state(self):
        """Test the /api/recommendations endpoint with invalid state"""
        response = self.client.get('/api/recommendations', data={
            'user_id': '1',
            'state': 5  # Invalid state (out of range)
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid state value', response.json['error'])

    # def test_new_user_creation(self):
    #     """Test user creation and initialization"""
    #     response = self.client.post('/api/recommendations/new_user', query_string={
    #         'user_id': 'test1'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('create Response', response.json)
    #     self.assertIn('initialize response', response.json)

    # def test_new_user_creation_v2(self):
    #     """Test user creation and initialization"""
    #     response = self.client.post('/api/recommendations/v2/new_user', query_string={
    #         'user_id': 'test1'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('create Response', response.json)
    #     self.assertIn('initialize response', response.json)

    def test_update_q_value(self):
        """Test Q-value update endpoint"""
        response = self.client.post('/api/recommendations/updateq', query_string={
            'user_id': '123',
            'state': '1',
            'action': '2',
            'reward': '10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('update Response', response.json)

    #update Q value with missing parameters
        
    def test_update_q_value_missing_parameters(self):
        """Test Q-value update endpoint with missing parameters"""
        response = self.client.post('/api/recommendations/updateq', query_string={
            'user_id': '123',
            'state': '1',
            'action': '2',
            # Missing reward parameter
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing user_id, state, action or reward parameter', response.json['error'])

    def test_get_cumulative_reward(self):
        """Test cumulative reward retrieval"""
        response = self.client.get('/api/recommendations/get_cum_reward', query_string={
            'user_id': '123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('cumulative reward', response.json)


    def test_get_recommendation_v1_valid_state(self):
        """Test /api/recommendations endpoint with valid state."""
        response = self.client.get('/api/recommendations', data={
            'user_id': '123',
            'state': 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('activity', response.json)

    # def test_get_recommendation_v1_invalid_user(self):
    #     """Test /api/recommendations with non-existent user."""
    #     response = self.client.get('/api/recommendations', data={
    #         'user_id': '9999',
    #         'state': 2
    #     })
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn('User not found', response.json['error'])
        
    #get recommendation v1 with invalid state
        
    def test_get_recommendation_v1_invalid_state(self):
        """Test /api/recommendations endpoint with invalid state."""
        response = self.client.get('/api/recommendations', data={
            'user_id': '123',
            'state': 5  # Invalid state (out of range)
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid state value', response.json['error'])

    def test_get_all_actions_v2(self):
        """Test /api/v2/recommendations/get_all_actions to retrieve all actions."""
        response = self.client.get('/api/v2/recommendations/get_all_actions')
        self.assertEqual(response.status_code, 200)
        self.assertIn('actions', response.json)

    def test_invalid_recommendation_v2(self):
        """Test /api/v2/recommendations/get with missing parameters."""
        response = self.client.get('/api/v2/recommendations/get', query_string={
            'user_id': '123'
            # Missing other required parameters like vegetarian, weight, etc.
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing user_id, vegetarian, weight, height, exersize_level or meal parameter', response.json['error'])

    def test_get_recommendation_v2_with_parameters(self):
        """Test /api/v2/recommendations/get with valid parameters."""
        response = self.client.get('/api/v2/recommendations/get', query_string={
            'user_id': '456',
            'vegetarian': '0',
            'weight': '70',
            'height': '170',
            'exersize_level': '1',
            'meal': '1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Recommended Meal ', response.json)

    def test_get_recommendation_with_parameters(self):
        """Test /api/recommendations/get with valid parameters."""
        response = self.client.get('/api/recommendations/get', query_string={
            'user_id': '123',
            'vegetarian': '0',
            'weight': '70',
            'height': '170',
            'exersize_level': '1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Recommended Meal ', response.json)


    def test_get_recommendation_v3_with_parameters(self):
        """Test /api/v3/recommendations/get with valid parameters."""
        response = self.client.get('/api/v3/recommendations/get', query_string={
            'user_id': '123',
            'vegetarian': '0',
            'weight': '70',
            'height': '170',
            'exersize_level': '1',
            'meal': '1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Recommended Meal ', response.json)

    # get recommendation v3 with missing parameters
        
    def test_get_recommendation_v3_missing_parameters(self):
        """Test /api/v3/recommendations/get with missing parameters."""
        response = self.client.get('/api/v3/recommendations/get', query_string={
            'user_id': '123',
            'vegetarian': '0',
            'weight': '70',
            'height': '170',
            'exersize_level': '1',
            # Missing meal parameter
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing user_id, vegetarian, weight, height, exersize_level or meal parameter', response.json['error'])

    def test_update_q_value_v3(self):
        """Test /api/v3/recommendations/updateq for Q-value update."""
        response = self.client.post('/api/v2/recommendations/updateq', query_string={
            'user_id': '456',
            'state': '2',
            'action': '3',
            'reward': '0.2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('update Response', response.json)


    def test_get_recommendation_v2_valid_state(self):
            """Test /api/recommendations endpoint with valid state."""
            response = self.client.get('/api/v2/recommendations', query_string={
                'user_id': '456',
                'state': '2'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('activity', response.json)


    def test_get_recommendation_v3_valid_state(self):
            """Test /api/v3/recommendations endpoint with valid state."""
            response = self.client.get('/api/v3/recommendations', query_string={
                'user_id': '456',
                'state': '2'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('activity', response.json)

    def test_insert_version_v3_valid(self):
        """Test /api/v3/recommendations/insert_version with valid parameters."""
        response = self.client.post('/api/v3/recommendations/insert_version', query_string={
            'version_no': '1.2',
            'states': '4',
            'actions': '6'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('create Response', response.json)


    


   

if __name__ == '__main__':
    unittest.main()
