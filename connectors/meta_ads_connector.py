"""
Meta Ads API Connector Stub for AI Marketing Operator.

This connector provides a standardized interface for fetching campaign
performance data from Meta (Facebook/Instagram) Ads. Currently a stub.

Setup:
  1. Create a Meta Business app: https://developers.facebook.com/docs/marketing-apis/
  2. Set environment variables:
     - META_ADS_ACCESS_TOKEN
     - META_ADS_APP_ID
     - META_ADS_APP_SECRET
     - META_ADS_AD_ACCOUNT_ID
  3. Install: pip install facebook_business
"""

import os
from typing import Dict, Any, List, Optional


class MetaAdsNotConfiguredError(Exception):
    """Raised when Meta Ads API credentials are not configured."""
    pass


class MetaAdsConnector:
    """
    Meta Ads API connector for fetching campaign performance data.
    """

    REQUIRED_ENV_VARS = [
        "META_ADS_ACCESS_TOKEN",
        "META_ADS_APP_ID",
        "META_ADS_APP_SECRET",
        "META_ADS_AD_ACCOUNT_ID",
    ]

    def __init__(self):
        self._validate_credentials()

    def _validate_credentials(self):
        missing = [v for v in self.REQUIRED_ENV_VARS if not os.environ.get(v)]
        if missing:
            raise MetaAdsNotConfiguredError(
                f"Meta Ads API not configured. Missing environment variables: {', '.join(missing)}. "
                f"See module docstring for setup instructions."
            )

    @classmethod
    def is_available(cls) -> bool:
        """Check if Meta Ads API credentials are configured."""
        return all(os.environ.get(v) for v in cls.REQUIRED_ENV_VARS)

    def fetch_campaign_insights(
        self,
        date_range: str = "LAST_30_DAYS",
        campaign_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Fetch campaign performance insights from Meta Ads API."""
        raise NotImplementedError(
            "Meta Ads API integration pending. Install facebook_business package and configure credentials."
        )

    def fetch_ad_set_performance(
        self,
        campaign_id: str,
        date_range: str = "LAST_30_DAYS",
    ) -> List[Dict[str, Any]]:
        """Fetch ad set level performance data."""
        raise NotImplementedError(
            "Meta Ads API integration pending."
        )

    def fetch_creative_performance(
        self,
        campaign_id: str,
        date_range: str = "LAST_30_DAYS",
    ) -> List[Dict[str, Any]]:
        """Fetch ad creative performance for fatigue analysis."""
        raise NotImplementedError(
            "Meta Ads API integration pending."
        )
