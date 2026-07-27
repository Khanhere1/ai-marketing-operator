"""
HubSpot API Connector Stub for AI Marketing Operator.

This connector provides a standardized interface for fetching CRM data
from HubSpot to evaluate lead quality. Currently a stub.

Setup:
  1. Create a HubSpot App or Private App: https://developers.hubspot.com/
  2. Set environment variables:
     - HUBSPOT_API_KEY (or HUBSPOT_ACCESS_TOKEN)
  3. Install: pip install hubspot-api-client
"""

import os
from typing import Dict, Any, List, Optional


class HubSpotNotConfiguredError(Exception):
    """Raised when HubSpot API credentials are not configured."""
    pass


class HubSpotConnector:
    """
    HubSpot API connector for fetching CRM lead and deal data.
    """

    def __init__(self):
        self._validate_credentials()

    def _validate_credentials(self):
        if not os.environ.get("HUBSPOT_API_KEY") and not os.environ.get("HUBSPOT_ACCESS_TOKEN"):
            raise HubSpotNotConfiguredError(
                "HubSpot API not configured. Missing environment variables: HUBSPOT_API_KEY or HUBSPOT_ACCESS_TOKEN. "
                "See module docstring for setup instructions."
            )

    @classmethod
    def is_available(cls) -> bool:
        """Check if HubSpot API credentials are configured."""
        return bool(os.environ.get("HUBSPOT_API_KEY") or os.environ.get("HUBSPOT_ACCESS_TOKEN"))

    def fetch_leads(
        self,
        date_range: str = "LAST_30_DAYS",
    ) -> List[Dict[str, Any]]:
        """Fetch leads (contacts) from HubSpot."""
        raise NotImplementedError(
            "HubSpot API integration pending. Install hubspot-api-client package and configure credentials."
        )

    def fetch_deals(
        self,
        date_range: str = "LAST_30_DAYS",
    ) -> List[Dict[str, Any]]:
        """Fetch deals (opportunities) from HubSpot."""
        raise NotImplementedError(
            "HubSpot API integration pending."
        )

    def fetch_pipeline_metrics(
        self,
        date_range: str = "LAST_30_DAYS",
    ) -> Dict[str, Any]:
        """Fetch aggregated pipeline metrics."""
        raise NotImplementedError(
            "HubSpot API integration pending."
        )

    def reconcile_ad_leads(
        self,
        campaign_name: str,
    ) -> Dict[str, Any]:
        """Reconcile ad campaign performance with CRM lead quality."""
        raise NotImplementedError(
            "HubSpot API integration pending."
        )
