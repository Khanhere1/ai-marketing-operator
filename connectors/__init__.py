"""
Connectors module for AI Marketing Operator.
Exports all platform connectors and provides utilities for managing them.
"""

from .google_ads_connector import GoogleAdsConnector, GoogleAdsNotConfiguredError
from .meta_ads_connector import MetaAdsConnector, MetaAdsNotConfiguredError
from .hubspot_connector import HubSpotConnector, HubSpotNotConfiguredError

__all__ = [
    "GoogleAdsConnector",
    "GoogleAdsNotConfiguredError",
    "MetaAdsConnector",
    "MetaAdsNotConfiguredError",
    "HubSpotConnector",
    "HubSpotNotConfiguredError",
    "get_available_connectors"
]


def get_available_connectors() -> dict:
    """
    Returns a dictionary of available connectors based on environment configuration.
    """
    available = {}
    
    if GoogleAdsConnector.is_available():
        available["google_ads"] = GoogleAdsConnector()
        
    if MetaAdsConnector.is_available():
        available["meta_ads"] = MetaAdsConnector()
        
    if HubSpotConnector.is_available():
        available["hubspot"] = HubSpotConnector()
        
    return available
