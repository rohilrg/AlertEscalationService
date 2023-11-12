import pytest
from unittest.mock import patch, MagicMock
from src.pager_service import PagerService

class TestPagerService:
    @pytest.fixture
    def pager_service(self):
        # Fixture to create a PagerService instance
        return PagerService(5)  # Example with 5 services

    def test_initialization(self, pager_service):
        # Test the initialization of the PagerService
        assert pager_service.number_of_services == 5
        assert isinstance(pager_service.number_of_services_dict, dict)
        # Additional assertions for other attributes

    @patch('json.dump')
    @patch('os.path.exists')
    def test_create_n_services_json(self, mock_exists, mock_json_dump, pager_service):
        # Mocking os.path.exists and json.dump
        mock_exists.return_value = False
        pager_service._create_n_services_json()
        mock_json_dump.assert_called()

    def test_run_healthy_state_when_already_healthy(self, pager_service):
        # Test handling the 'HEALTHY' state when the service is already marked healthy
        pager_service.make_healthy_the_services_later = []
        with patch('src.utils.setup_logger') as mock_setup_logger:
            mock_logger = MagicMock()
            mock_setup_logger.return_value = mock_logger
            pager_service.run('Service 1', 'HEALTHY')

            mock_logger.info.assert_not_called()

    def test_service_json_initialization(self, pager_service):
        # Test the initialization of the service status JSON
        pager_service._create_n_services_json()
        assert len(pager_service.number_of_services_dict) == pager_service.number_of_services
        for status in pager_service.number_of_services_dict.values():
            assert status == "HEALTHY"
