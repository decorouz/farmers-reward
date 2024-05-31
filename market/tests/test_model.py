from unittest.mock import MagicMock, patch

from django.test import TestCase

from market.models import Market


class MarketModelTest(TestCase):

    @patch("market.models.Nominatim")
    def test_save_updates_location_fields(self, MockNominatim):
        # Mock the geolocator and its return value
        mock_geolocator = MockNominatim.return_value
        mock_location = MagicMock()
        mock_location.latitude = 12.34
        mock_location.longitude = 56.78
        mock_location.raw = {
            "address": {
                "city": "Test City",
                "state": "Test State",
                "country": "Test Country",
                "county": "Test County",
            }
        }
        mock_geolocator.geocode.return_value = mock_location

        # Create a Market instance with an address
        market = Market(address="123 Test St")
        market.save()

        # Assert that the location fields are updated correctly
        self.assertEqual(market.latitude, 12.34)
        self.assertEqual(market.longitude, 56.78)
        self.assertEqual(market.city, "Test City")
        self.assertEqual(market.state, "Test State")
        self.assertEqual(market.country, "Test Country")
        self.assertEqual(market.local_govt_area, "Test County")

    @patch("market.models.Nominatim")
    def test_save_does_not_update_location_fields_if_no_location_found(
        self, MockNominatim
    ):
        # Mock the geolocator to return None
        mock_geolocator = MockNominatim.return_value
        mock_geolocator.geocode.return_value = None

        # Create a Market instance with an address
        market = Market(address="123 Test St")
        market.save()

        # Assert that the location fields are not updated
        self.assertIsNone(market.latitude)
        self.assertIsNone(market.longitude)
        self.assertEqual(market.city, "")
        self.assertEqual(market.state, "")
        self.assertEqual(market.country, "")
        self.assertEqual(market.local_govt_area, "")

    @patch("market.models.Nominatim")
    def test_save_does_not_call_geocode_if_latitude_and_longitude_exist(
        self, MockNominatim
    ):
        # Create a Market instance with latitude and longitude
        market = Market(address="123 Test St", latitude=12.34, longitude=56.78)
        market.save()

        # Assert that geocode is not called
        MockNominatim.return_value.geocode.assert_not_called()

    @patch("market.models.Nominatim")
    def test_save_updates_only_missing_location_fields(self, MockNominatim):
        # Mock the geolocator and its return value
        mock_geolocator = MockNominatim.return_value
        mock_location = MagicMock()
        mock_location.latitude = 12.34
        mock_location.longitude = 56.78
        mock_location.raw = {
            "address": {
                "city": "Test City",
                "state": "Test State",
                "country": "Test Country",
                "county": "Test County",
            }
        }
        mock_geolocator.geocode.return_value = mock_location

        # Create a Market instance with some location fields already set
        market = Market(address="123 Test St", latitude=12.34)
        market.save()

        # Assert that the missing location fields are updated correctly
        self.assertEqual(market.latitude, 12.34)
        self.assertEqual(market.longitude, 56.78)
        self.assertEqual(market.city, "Test City")
        self.assertEqual(market.state, "Test State")
        self.assertEqual(market.country, "Test Country")
        self.assertEqual(market.local_govt_area, "Test County")

    @patch("market.models.Nominatim")
    def test_save_does_not_update_location_fields_if_address_is_empty(
        self, MockNominatim
    ):
        # Create a Market instance with an empty address
        market = Market(address="")
        market.save()

        # Assert that the location fields are not updated
        self.assertIsNone(market.latitude)
        self.assertIsNone(market.longitude)
        self.assertEqual(market.city, "")
        self.assertEqual(market.state, "")
        self.assertEqual(market.country, "")
        self.assertEqual(market.local_govt_area, "")
