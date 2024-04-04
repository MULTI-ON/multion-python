# MultiOn Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)
[![pypi](https://img.shields.io/pypi/v/multion.svg)](https://pypi.python.org/pypi/multion)

The MultiOn Python Library provides convenient access to the MultiOn API from applications written in Python.

## Documentation

API reference documentation is available [here](https://multion.docs.buildwithfern.com/).

## Installation
Add this dependency to your project's build file:

```bash
pip install multion
# or
poetry add multion
```

## Usage
Simply import `MultiOn` and start making calls to our API. 

```python
from multion.client import MultiOn

client = MultiOn(
    api_key="YOUR_API_KEY" # defaults to os.getenv("MULTION_API_KEY")
)
response = client.browse(
    url="https://google.com"
)
```

## Async Client

The SDK also exports an async client so that you can make non-blocking
calls to our API. 

```python
from multion.client import AsyncMultiOn

client = AsyncMultiOn(
    api_key="YOUR_API_KEY" # defaults to os.getenv("MULTION_API_KEY")
)

async def main() -> None:
    await response = client.browse(
        url="https://google.com"
    )

asyncio.run(main())
```

## Exception Handling
All errors thrown by the SDK will be subclasses of [`ApiError`](./src/multion/core/api_error.py).

```python
import multion

try:
  client.browse(...)
except multion.core.ApiError as e: # Handle all errors
  print(e.status_code)
  print(e.body)
```

## Advanced

### Retries
The MultiOn SDK is instrumented with automatic retries with exponential backoff. A request will be
retried as long as the request is deemed retriable and the number of retry attempts has not grown larger
than the configured retry limit.

A request is deemed retriable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)
  
Use the `max_retries` request option to configure this behavior. 

```python
from multion.client import MultiOn

client = MultiOn()

# Override retries for a specific method
client.brwose(url="https://google.com", {
    max_retries=1
})
```

### Timeouts
By default, requests time out after 60 seconds. You can configure this with a 
timeout option at the client or request level.

```python
from multion.client import MultiOn

client = MultiOn(
    # All timeouts are 20 seconds
    timeout=20.0,
)

# Override timeout for a specific method
client.brwose(url="https://google.com", {
    timeout_in_seconds=20.0
})
```

### Custom HTTP client
You can override the httpx client to customize it for your use-case. Some common use-cases 
include support for proxies and transports.

```python
import httpx

from multion.client import MultiOn

client = MultiOn(
    http_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Beta Status

This SDK is in beta, and there may be breaking changes between versions without a major 
version update. Therefore, we recommend pinning the package version to a specific version. 
This way, you can install the same version each time without breaking changes.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. 
Additions made directly to this library would have to be moved over to our generation code, 
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening 
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
