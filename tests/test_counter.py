import pytest

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

@pytest.fixture()
def client():
  return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    def test_create_a_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_duplicate_a_counter(self, client):
        """It should return an error for duplicates"""
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT

    def test_update_a_counter(self, client):
        #create a couter and check that the result is 201
        result = client.post('/counters/xyz')
        assert result.status_code == status.HTTP_201_CREATED
        #increment a counter, and check that the result is OK
        #and contains 1
        result = client.put('/counters/xyz')
        assert result.status_code == status.HTTP_200_OK
        assert result.data == b'{"xyz":1}\n'
        #attempt to increment an invalid counter, check tfor 404
        result = client.put('/counters/not_xyz')
        assert result.status_code == status.HTTP_404_NOT_FOUND
        #increment the xyz counter again, and check result 2
        result = client.put('/counters/xyz')
        assert result.status_code == status.HTTP_200_OK
        assert result.data == b'{"xyz":2}\n'


