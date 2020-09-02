Namecheap API for Python
===========

[![PyPi Version](https://img.shields.io/pypi/v/privex-namecheap.svg)](https://pypi.org/project/privex-namecheap/)
![License Button](https://img.shields.io/pypi/l/privex-namecheap) 
![PyPI - Downloads](https://img.shields.io/pypi/dm/privex-namecheap)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/privex-namecheap) 
![GitHub last commit](https://img.shields.io/github/last-commit/Privex/PyNamecheap)


PyNamecheap is a Namecheap API client in Python.
API itself is documented at <https://www.namecheap.com/support/api/intro/>

This client supports:
-   Registering a domain
-   Checking domain name availability
-   Listing domains you have registered
-   Getting contact information for a domain
-   Setting DNS info to default values
-   Set DNS host records

**NOTE: This is a fork of [Bemmu/PyNamecheap](https://github.com/Bemmu/PyNamecheap)**.

The original library was created by @Bemmu - we (@Privex) forked the library so that we
could make various major changes, including using features which **prevent backwards compatibility**
**with Python 2.x and anything before 3.6**.

If you absolutely need to use a Python version prior to 3.6.0, then you should use the original
package: [Bemmu/PyNamecheap](https://github.com/Bemmu/PyNamecheap) 

### Installation

First, check your Python version by running `python3 -V`

```
user@host ~ $ python3 -V
Python 3.8.3
```

#### For Python 3.7 and higher

To install our fork's (`Privex/PyNamecheap`) python package - use `pip3` or `pipenv`
and install the package name `privex-namecheap` 

```
# Using standard Pip
pip3 install -U privex-namecheap

# Using Pipenv
pipenv install privex-namecheap

```

#### For Python 3.6.x

**If you are running Python 3.6.x**, you'll need to install our package with the `py36` extra - or
manually install the `dataclasses` package.

```
# Using standard Pip
pip3 install -U 'privex-namecheap[py36]'

# Using Pipenv
pipenv install 'privex-namecheap[py36]'
```

Do **NOT** install `privex-namecheap[py36]` if you are running Python 3.7 or newer. It will break your
built-in Python `dataclasses` module.

#### For Python 3.5.x or older...

The original library was created by @Bemmu - we (@Privex) forked the library so that we
could make various major changes, including using features which **prevent backwards compatibility**
**with Python 2.x and anything before 3.6**.

This means it's not possible to use `privex-namecheap` with any Python version older than `3.6.0`

If you absolutely need to use a Python version prior to 3.6.0, then you should use the original
package: [Bemmu/PyNamecheap](https://github.com/Bemmu/PyNamecheap) 

### How to sign up to start using the API

The API has two environments, production and sandbox. Since this API will spend real money when registering domains, start with the sandbox by going to <http://www.sandbox.namecheap.com/> and creating an account. Accounts between production and sandbox are different, so even if you already have a Namecheap account you will need a new one.

After you have an account, go to "Profile".

![Profile](img/profile.png "Profile")

From there, select the "Profile" menu again, then "Tools". Scroll to the bottom of the page to the "Business & Dev Tools" and select "Manage" on the "Namecheap API Access" section.

![API menu](img/apimenu.png "API menu")

You'll get to your credentials page. From here you need to take note of your api key, username and add your IP to the whitelist of IP addresses that are allowed to access the account. You can check your public IP by searching "what is my ip" on Google and add it here. It might take some time before it actually starts working, so don't panic if API access doesn't work at first.

![Credentials](img/credentials.png "Credentials")

### How to access the API from Python

Copy namecheap.py to your project. In Python you can access the API as follows:

```python
from namecheap import Api
# api_username, api_key, client_ip_address
api = Api('NamecheapUsername', 'YourNamecheapAPIKey', '12.34.56.78', sandbox=True, debug=True)

# Using keyword arguments (recommended - more reliable in the event the constructor is changed)
api = Api(
    ApiUser='NamecheapUsername', 
    ApiKey='YourNamecheapAPIKey',
    ClientIP='12.34.56.78', 

    # OPTIONAL. You only need to specify UserName if you're managing resources on a different
    # Namecheap account from your own account - e.g. someone has granted your account permission
    # to manage their domains etc.
    UserName='NamecheapUsername', 

    # By default, sandbox and debug are both False. Set sandbox=True to use the Namecheap Sandbox API,
    # and set debug=True to enable verbose debug logging to help you understand what the library is
    # doing behind the scenes.
    sandbox=True, debug=True
)

```
The fields are the ones which appear in the credentials screen above. 

The username appears twice, because you might be acting on behalf of someone else.

### Registering a domain name using the API + common usage examples

Unfortunately you need a bunch of contact details to register a domain, so it is not as easy as just providing the domain name. 

In the sandbox, the following contact details are acceptable. Trickiest field is the phone number, which has to be formatted as shown.

```python
from namecheap import Api, DomainRecord

contact_details = dict(
    FirstName='Jack',
    LastName='Trotter',
    Address1='Ridiculously Big Mansion, Yellow Brick Road',
    City='Tokushima',
    StateProvince='Tokushima',
    PostalCode='771-0144',
    Country='Japan',
    Phone="+81.123123123",
    EmailAddress='jack.trotter@example.com'
)

api = Api('NamecheapUsername', 'YourNamecheapAPIKey', '12.34.56.78', sandbox=True, debug=True)

# First let's find out how much various TLDs cost at the moment
tld_prices = api.get_tld_prices('com', 'org', 'net', 'bz', 'xyz', 'us')
for tld, price in tld_prices.items():
    print(f".{tld} pricing - Current Price: ${price.total_your_price:.2f} | Regular Price: ${price.total_regular_price:.2f}")
print("-------------")
"""
(Example output)
.com pricing - Current Price: $9.06 | Regular Price: $9.06
.org pricing - Current Price: $13.16 | Regular Price: $13.16
.net pricing - Current Price: $12.16 | Regular Price: $13.16
.bz pricing - Current Price: $21.88 | Regular Price: $21.88
.xyz pricing - Current Price: $1.18 | Regular Price: $11.06
.us pricing - Current Price: $3.88 | Regular Price: $8.48
-------------
"""

# Next let's specifically get just the .com TLD price
com_price = api.get_tld_prices('com')
print(f"Price you'll pay: ${com_price.total_your_price:.2f} | Regular Non-promo Price: ${com_price.total_regular_price:.2f}")

# Now for the important part - registering the domain. We need to specify all of the contact details
# when registering the domain.
reg = api.domains_create(
    'mycooldomain.com',
    **contact_details
)
print("Domain registration result:", reg)
# domains_create is also available as the alias: register_domain

# Assuming no exception occurred, then we can now setup the records for the domain

# Using replace_records, we can get rid of all the default parking page records etc., and overwrite them
# with our custom records - in one fell swoop.
api.replace_records(
    'mycooldomain.com',
    DomainRecord('A', '185.130.44.10'),               # Name: @   | Type: A     | Value: 185.130.44.10
    DomainRecord('AAAA', '2a07:e00::abc'),            # Name: @   | Type: A     | Value: 185.130.44.10
    DomainRecord('CNAME', 'mycooldomain.com', 'www')  # Name: www | Type: CNAME | Value: mycooldomain.com
)

# Using add_record, we can insert singular records to the existing records, instead of overwriting them
api.add_record('mycooldomain.com', 'TXT', 'hello world')          # Name: @    | Type: TXT | Value: hello world
api.add_record('mycooldomain.com', 'A', '127.0.0.1', 'test')      # Name: test | Type: A   | Value: 127.0.0.1

# Using delete_record, we can delete individual records based on their type, content, and sub-domain
api.delete_record('mycooldomain.com', 'TXT', 'hello world')       # Delete the root domain TXT record 'hello world'
api.delete_record('mycooldomain.com', 'A', '127.0.0.1', 'test')   # Delete the 'test' subdomain A record '127.0.0.1'

info = api.domains_getInfo('mycooldomain.com')
print(info.expired_date)   # Output: 2020-11-05 00:00:00

# If mycooldomain.com is expiring in the next 60 days, renew it for one year.
if info.days_until_expires < 60:
    api.renew_domain('mycooldomain.com')

# Change the nameservers for mycooldomain.com to ns1.privex.io to ns3.privex.io
api.set_nameservers('mycooldomain.com', 'ns1.privex.io', 'ns2.privex.io', 'ns3.privex.io')

# Change the nameservers for mycooldomain.com back to the default Namecheap nameservers,
# to allow using the domain with Namecheap's email service, URL redirect records + other features.
api.domains_dns_setDefault('mycooldomain.com')
```

This call should succeed in the sandbox, but if you use the API to check whether this domain is available after registering it, the availability will not change. This is normal.

### How to check if a domain name is available

The `domains_available` method returns True if the domain is available.

```python
from namecheap import Api
api = Api('NamecheapUsername', 'YourNamecheapAPIKey', '12.34.56.78', sandbox=True, debug=True)
api.domains_available('taken.com', 'apsdjcpoaskdc.com')
# Might result in
# {
#   'taken.com' : False,
#   'apsdjcpoaskdc.com' : True
# }

# If you check a singular domain, it will return a bool, unless you pass force_dict=True
api.domains_available('taken.com')
# True
api.domains_available('taken.com', force_dict=True)
# {'taken.com' : False}
```

You can also pass a list of domain names, in which case it does a batch check for all and returns a dictionary of the answers.
You should probably not be writing a mass domain checking tool using this, it is intended to be used before registering a domain.

### CLI tool usage

First, you need to edit `./credentials.py` file to provide API access for the script. The example is following:

    #!/usr/bin/env python

    api_key = '0123456789abcdef0123456789abcdef'
    username = 'myusername'
    ip_address = '10.0.0.1'

Then you just call the script with desired arguments:

    ./namecheap-api-cli --domain example.org --list

    ./namecheap-api-cli --domain example.org --add --type "A" --name "test" --address "127.0.0.1" --ttl 300
    ./namecheap-api-cli --domain example.org --add --type "CNAME" --name "alias-of-test" --address "test.example.org." --ttl 1800

    ./namecheap-api-cli --domain example.org --delete --type "CNAME" --name "alias-of-test" --address "test.example.org."
    ./namecheap-api-cli --domain example.org --delete --type "A" --name "test" --address "127.0.0.1"

### Basic host records management code

Here's the example of simple DNS records management script:

```python

#!/usr/bin/env python
"""
Define variables regarding to your API account:
  - api_key
  - username
  - ip_address
"""
from namecheap import Api

username = 'MyNamecheapUser'
api_key = 'SomeAPIKey'
ip_address = '1.2.3.4'
api = Api(username, api_key, ip_address, sandbox=False)

domain = "example.org"

# list domain records
api.list_records(domain)

# add an 'A' record for subdomain "test" pointing to 127.0.0.1
api.add_record(domain, 'A', '127.0.0.1', hostname='test', ttl=1800)

# delete record we just created,
# selecting it by Name, Type and Address values
api.delete_record(domain,  'A', '127.0.0.1', hostname='test')
```

### Retry mechanism

Sometimes you could face wrong API responses, which are related to server-side errors.

Thanks to @gstein, we implemented retry mechanism, one could enable it by adding 2 parameters to Api instance:

```
api = Api(username, api_key, ip_address, sandbox=False,
          attempts_count=3,
          attempts_delay=0.1)
```

Values of 2 or 3 should do the thing.

### More

Look at namecheap_tests.py to see more examples of things you can do.
