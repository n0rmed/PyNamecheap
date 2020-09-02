from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Type, Union

from privex.helpers import DAY, DictDataClass, DictObject, MONTH, YEAR, dec_round, empty, is_true

from namecheap.helpers import america_date, api_string, conv_dec, conv_int, dict_to_camel, dict_to_snake
import logging

__all__ = [
    'CamelSnakeDictable', 'CreateDomainResponse', 'DomainRecord', 'Domain', 'DomainCheck',
    'TLDPrice', 'DomainDetails', 'NamecheapTLD'
]


log = logging.getLogger(__name__)


class CamelSnakeDictable(DictDataClass):
    # noinspection PyUnresolvedReferences
    @classmethod
    def from_dict(cls: Type[dataclass], obj):
        return super().from_dict({
            **dict_to_snake(obj),
            'raw_data': obj
        })
    
    def to_dict(self: DictDataClass, camel=False):
        res = dict_to_camel(dict(self)) if camel else dict(self)
        
        s_keys = getattr(self.DictConfig, 'stringify_keys', [])
        s_all = getattr(self.DictConfig, 'stringify_all', False)
        
        if not empty(s_keys, itr=True) or s_all:
            for k, v in dict(res).items():
                if k in self.DictConfig.stringify_keys or s_all:
                    res[k] = api_string(res[k])
        
        return res


@dataclass
class CreateDomainResponse(CamelSnakeDictable):
    class DictConfig:
        stringify_all = True
        # stringify_keys = [
        #     'registered', 'Registered', 'charged_amount', 'ChargedAmount', 'domain_id', 'DomainID',
        #     'order_id', 'OrderID', 'transaction_id', 'TransactionID', 'whoisguard_enable', 'WhoisguardEnable',
        #     'free_positive_ssl', 'FreePositiveSSL', 'non_real_time_domain', 'NonRealTimeDomain'
        # ]
    
    domain: str
    registered: bool = False
    charged_amount: Decimal = field(default_factory=Decimal)
    domain_id: int = 0
    order_id: int = 0
    transaction_id: int = 0
    whoisguard_enable: bool = False
    free_positive_ssl: bool = False
    non_real_time_domain: bool = False
    raw_data: Union[dict, DictObject] = field(default_factory=DictObject, repr=False)


@dataclass
class DomainRecord(CamelSnakeDictable):
    class DictConfig:
        dict_convert_mode = None
        stringify_keys = [
            'mx_pref', 'MXPref', 'ttl', 'TTL', 'is_active', 'IsActive', 'is_ddns_enabled', 'IsDDNSEnabled'
        ]
    
    type: str
    address: str
    name: str = '@'
    host_id: int = None
    mx_pref: int = 10
    ttl: int = 300
    associated_app_title: str = ''
    friendly_name: str = ''
    is_active: bool = True
    is_ddns_enabled: bool = False
    raw_data: Union[dict, DictObject] = field(default_factory=DictObject, repr=False)
    
    def __post_init__(self):
        self.mx_pref = conv_int(self.mx_pref)
        self.ttl = conv_int(self.ttl)
        self.is_active = is_true(self.is_active)
        self.is_ddns_enabled = is_true(self.is_ddns_enabled)


@dataclass
class Domain(CamelSnakeDictable):
    class DictConfig:
        dict_convert_mode = None
        stringify_all = True
    
    id: int
    name: str
    user: str = None
    created: datetime = None
    expires: datetime = None
    is_expired: bool = False
    is_locked: bool = False
    auto_renew: bool = False
    whois_guard: str = 'NOTPRESENT'
    is_premium: bool = False
    is_our_dns: bool = False
    raw_data: Union[dict, DictObject] = field(default_factory=DictObject, repr=False)
    
    def __post_init__(self):
        # Namecheap returns dates in US format - MM/DD/YYYY - so we carefully convert them using that format.
        if not empty(self.created) and isinstance(self.created, str):
            self.created = datetime.strptime(self.created, "%m/%d/%Y")
        if not empty(self.expires) and isinstance(self.expires, str):
            self.expires = datetime.strptime(self.expires, "%m/%d/%Y")
        
        self.is_expired = is_true(self.is_expired)
        self.is_locked = is_true(self.is_locked)
        self.auto_renew = is_true(self.auto_renew)
        self.is_premium = is_true(self.is_premium)
        self.is_our_dns = is_true(self.is_our_dns)


@dataclass
class DomainCheck(CamelSnakeDictable):
    class DictConfig:
        dict_convert_mode = None
        stringify_all = True
    domain: str
    available: bool
    error_no: int = None
    description: str = ''
    is_premium_name: bool = False
    premium_registration_price: Decimal = field(default_factory=Decimal)
    premium_renewal_price: Decimal = field(default_factory=Decimal)
    premium_restore_price: Decimal = field(default_factory=Decimal)
    premium_transfer_price: Decimal = field(default_factory=Decimal)
    icann_fee: Decimal = field(default_factory=Decimal)
    eap_fee: Decimal = field(default_factory=Decimal)
    raw_data: Union[dict, DictObject] = field(default_factory=DictObject, repr=False)

    def __post_init__(self):
        conv_bool_keys = ['available', 'is_premium_name']
        conv_dec_keys = [
            'premium_registration_price', 'premium_renewal_price', 'premium_restore_price',
            'premium_transfer_price', 'icann_fee', 'eap_fee',
        ]
        self.error_no = None if empty(self.error_no) else int(self.error_no)
        for k in conv_bool_keys:
            v = getattr(self, k, None)
            if not empty(v):
                setattr(self, k, is_true(v))
        for k in conv_dec_keys:
            v = getattr(self, k, None)
            if empty(v):
                log.debug("Skipping %s - is empty", k)
                continue
            log.debug("Converting %s to decimal", k)
            setattr(self, k, dec_round(Decimal(v), dp=4))


@dataclass
class TLDPrice(CamelSnakeDictable):
    class DictConfig:
        dict_convert_mode = None
        stringify_all = True
    
    tld: str = None
    duration: int = 0
    duration_type: str = 'YEAR'
    price: Decimal = field(default_factory=Decimal)
    pricing_type: str = field(default='', repr=False)
    additional_cost: Decimal = field(default_factory=Decimal)
    
    regular_price: Decimal = field(default_factory=Decimal)
    regular_price_type: str = field(default='', repr=False)
    regular_additional_cost: Decimal = field(default_factory=Decimal)
    regular_additional_cost_type: str = field(default='', repr=False)

    your_price: Decimal = field(default_factory=Decimal)
    your_price_type: str = field(default='', repr=False)
    your_additional_cost: Decimal = field(default_factory=Decimal)
    your_additional_cost_type: str = field(default='', repr=False)

    promotion_price: Decimal = field(default_factory=Decimal)
    coupon_price: Decimal = field(default_factory=Decimal)
    currency: str = 'USD'

    raw_data: Union[dict, DictObject] = field(default_factory=DictObject, repr=False)

    @property
    def total_your_price(self) -> Decimal:
        return self.your_price + self.your_additional_cost

    @property
    def total_price(self) -> Decimal:
        return self.price + self.additional_cost

    @property
    def total_regular_price(self) -> Decimal:
        return self.regular_price + self.regular_additional_cost

    def __post_init__(self):
        if empty(self.your_additional_cost, True, True) and 'YourAdditonalCost' in self.raw_data:
            self.your_additional_cost = self.raw_data['YourAdditonalCost']
        if empty(self.your_additional_cost_type, True, True) and 'YourAdditonalCost' in self.raw_data:
            self.your_additional_cost_type = self.raw_data['YourAdditonalCostType']
        self.duration = conv_int(self.duration)
        self.price = conv_dec(self.price)
        self.additional_cost = conv_dec(self.additional_cost)
        self.regular_price = conv_dec(self.regular_price)
        self.regular_additional_cost = conv_dec(self.regular_additional_cost)
        self.your_price = conv_dec(self.your_price)
        self.your_additional_cost = conv_dec(self.your_additional_cost)
        self.promotion_price = conv_dec(self.promotion_price)
        self.coupon_price = conv_dec(self.coupon_price)


@dataclass
class DomainDetails(CamelSnakeDictable):
    class DictConfig:
        dict_convert_mode = None
        stringify_all = True
    
    domain_name: str = None
    status: str = None
    id: int = None
    owner_name: str = None
    is_owner: bool = False
    is_premium: bool = False
    
    domain_details: dict = field(default_factory=dict, repr=False)
    lock_details: dict = field(default_factory=dict, repr=False)
    whoisguard: dict = field(default_factory=dict, repr=False)
    premium_dns_subscription: dict = field(default_factory=dict, repr=False)
    dns_details: dict = field(default_factory=dict, repr=False)
    nameservers: List[str] = field(default_factory=list, repr=False)
    modification_rights: dict = field(default_factory=dict, repr=False)
    
    raw_data: Union[dict, DictObject] = field(default_factory=DictObject, repr=False)
    
    @property
    def created_date(self) -> Optional[datetime]:
        d = self.domain_details.get('CreatedDate', None)
        return None if empty(d) else america_date(d)
    
    created_at = created_date
    
    @property
    def expired_date(self) -> Optional[datetime]:
        d = self.domain_details.get('ExpiredDate', None)
        return None if empty(d) else america_date(d)
    
    expired_at = expires_at = expiry_date = expired_date
    
    @property
    def days_left_expiry(self) -> Optional[int]:
        if self.expired_date is None:
            return None
        ex = self.expired_date
        diff = ex - datetime.utcnow()
        return int(diff.total_seconds() // DAY)
    
    days_left_expires = days_til_expires = days_until_expires = days_left_expiry
    days_til_expiry = days_until_expiry = days_left_expiry
    
    @property
    def months_left_expiry(self) -> Optional[int]:
        if self.expired_date is None:
            return None
        return int(self.days_left_expiry // MONTH)
    
    months_left_expires = months_til_expires = months_until_expires = months_left_expiry
    months_til_expiry = months_until_expiry = months_left_expiry
    
    @property
    def years_left_expiry(self) -> Optional[int]:
        if self.expired_date is None:
            return None
        return int(self.days_left_expiry // YEAR)
    
    years_left_expires = years_til_expires = years_until_expires = years_left_expiry
    years_til_expiry = years_until_expiry = years_left_expiry
    
    @property
    def num_years(self) -> Optional[int]:
        d = self.domain_details.get('NumYears', None)
        if empty(d): return None
        return d if isinstance(d, int) else int(d)
    
    @property
    def has_whoisguard(self) -> bool:
        return is_true(self.whoisguard.get('Enabled', False))
    
    @property
    def has_premium_dns(self) -> bool:
        return is_true(self.premium_dns_subscription.get('IsActive', False))
    
    @property
    def using_namecheap_dns(self) -> bool:
        return is_true(self.dns_details.get('IsUsingOurDNS', False))
    
    def __post_init__(self):
        if not empty(self.id, zero=True):
            self.id = int(self.id)
        if not empty(self.is_owner, zero=True):
            self.is_owner = is_true(self.is_owner)
        if not empty(self.is_premium, zero=True):
            self.is_premium = is_true(self.is_premium)


@dataclass
class NamecheapTLD(CamelSnakeDictable):
    class DictConfig:
        dict_convert_mode = None
        stringify_all = True
    
    name: str = None
    description: str = ""
    
    non_real_time: bool = False
    
    min_register_years: int = field(default=None, repr=False)
    max_register_years: int = field(default=None, repr=False)
    min_renew_years: int = field(default=None, repr=False)
    max_renew_years: int = field(default=None, repr=False)
    min_transfer_years: int = field(default=None, repr=False)
    max_transfer_years: int = field(default=None, repr=False)
    reactivate_max_days: int = field(default=None, repr=False)
    add_grade_period_days: int = field(default=None, repr=False)
    renewal_min_days: int = field(default=None, repr=False)
    renewal_max_days: int = field(default=None, repr=False)
    
    is_api_registerable: bool = False
    is_api_renewable: bool = False
    is_api_transferable: bool = False
    is_epp_required: bool = field(default=False, repr=False)
    is_disable_mod_contact: bool = field(default=False, repr=False)
    is_disable_wg_allot: bool = field(default=False, repr=False)
    is_include_in_extended_search_only: bool = field(default=False, repr=False)
    
    sequence_number: int = field(default=None, repr=False)
    type: str = None
    sub_type: str = None
    
    is_supports_idn: bool = field(default=False, repr=False)
    supports_registrar_lock: bool = field(default=False, repr=False)
    whois_verification: bool = field(default=False, repr=False)
    provider_api_delete: bool = field(default=False, repr=False)
    
    category: str = None
    tld_categories: List[Dict[str, str]] = field(default_factory=list)
    """
    [
        {'Name': 'popular', 'SequenceNumber': '20'}, {'Name': 'new', 'SequenceNumber': '2910'},
        {'Name': '088domains', 'SequenceNumber': '250'}
    ]
    """
    
    tld_state: str = None
    search_group: str = None
    registry: str = None
    
    raw_data: Union[dict, DictObject] = field(default_factory=DictObject, repr=False)
    
    def __post_init__(self):
        conv_bool_keys = [
            'non_real_time', 'is_api_registerable', 'is_api_renewable', 'is_api_transferable',
            'is_epp_required', 'is_disable_mod_contact', 'is_disable_wg_allot', 'is_include_in_extended_search_only',
            'is_supports_idn', 'supports_registrar_lock', 'whois_verification', 'provider_api_delete'
        ]
        conv_int_keys = [
            'min_register_years', 'max_register_years' 'min_renew_years', 'max_renew_years',
            'min_transfer_years', 'max_transfer_years', 'reactivate_max_days', 'add_grace_period_days',
            'renewal_min_days', 'renewal_max_days', 'sequence_number',
        ]
        
        for k in conv_bool_keys:
            v = getattr(self, k, None)
            if not empty(v):
                setattr(self, k, is_true(v))
        for k in conv_int_keys:
            v = getattr(self, k, None)
            if not empty(v) and not isinstance(v, int):
                setattr(self, k, int(v))
