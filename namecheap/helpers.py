from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, Union

from privex.helpers import camel_to_snake as _camel_to_snake, dec_round, empty, human_name, is_true, stringify

from privex.helpers.types import AnyNum

import logging

log = logging.getLogger(__name__)

__all__ = [
    'CAMEL_MAP', 'camel_to_snake', 'snake_to_camel', 'dict_to_snake', 'dict_to_camel', 'api_string',
    'america_date', 'american_date', 'conv_bool', 'conv_int', 'conv_dec', 'conv_decimal'
]

CAMEL_MAP = {
    'id': 'ID',
    'ttl': 'TTL',
    'mxpref': 'MXPref',
    'mx_pref': 'MXPref',
    'isddnsenabled': 'IsDDNSEnabled',
    'is_ddns_enabled': 'IsDDNSEnabled',
    'domain_id': 'DomainID',
    'order_id': 'OrderID',
    'transaction_id': 'TransactionID',
    'free_positive_ssl': 'FreePositiveSSL',
    'is_our_dns': 'IsOurDNS',
}

SNAKE_MAP = {
    'IsDisableWGAllot': 'is_disable_wg_allot',
    'IsDDNSEnabled': 'is_ddns_enabled',
}


def camel_to_snake(data: str) -> str:
    """
    Convert a string from camel case "ExampleKey" into snake case "example_key"
    """
    if data in SNAKE_MAP:
        return SNAKE_MAP[data]
    return _camel_to_snake(data)


def snake_to_camel(data: str) -> str:
    """
    Convert a string from snake case "example_key" into camel case "ExampleKey"
    """
    # Certain snakecase names are explicitly mapped to the correct CamelCase output format,
    # as human_name() does not format them as expected. E.G. ``ttl`` should convert to ``TTL`` not ``Ttl``
    if data.lower() in CAMEL_MAP:
        return CAMEL_MAP[data.lower()]
    return human_name(data).replace(' ', '')


def dict_to_snake(obj: dict) -> dict:
    """
    Convert camel case "ExampleKey" dict keys into snake case "example_key"
    """
    return {camel_to_snake(k): v for k, v in obj.items()}


def dict_to_camel(obj: dict) -> dict:
    """
    Convert snake case "example_key" dict keys into camel case "ExampleKey"
    """
    return {snake_to_camel(k): v for k, v in obj.items()}


def api_string(obj: Any) -> str:
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (Decimal, float)):
        return f"{obj:.4f}"
    return stringify(obj)


def america_date(date: str) -> datetime:
    return datetime.strptime(date, "%m/%d/%Y")


american_date = america_date


def conv_dec(obj: Optional[AnyNum], dp=4) -> Optional[Decimal]:
    if empty(obj):
        return None
    try:
        d = Decimal(obj)
        return dec_round(d, dp=dp)
    except Exception as e:
        log.warning("Error while converting object '%s' to decimal. Reason: %s %s", obj, type(e), str(e))
        return None


conv_decimal = conv_dec


def conv_int(obj: Optional[AnyNum]) -> Optional[int]:
    if empty(obj):
        return None
    try:
        return int(obj)
    except Exception as e:
        log.warning("Error while converting object '%s' to integer. Reason: %s %s", obj, type(e), str(e))
        return None


def conv_bool(obj: Optional[Union[str, bool, int]]) -> Optional[bool]:
    if empty(obj):
        return None
    try:
        return is_true(obj)
    except Exception as e:
        log.warning("Error while converting object '%s' to integer. Reason: %s %s", obj, type(e), str(e))
        return None
