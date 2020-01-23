# HTTP Rx - Your HTTP Doctor

**HTTP Rx** is a simple site/http monitor for your websites and HTTP endpoints. The tool monitors a given list of endpoint configurations and sends alerts if the expected health check does not pass.

Additional reporting is also provided and be configured per health check.

---

## Installing

This package is available on the Python Package Index (PyPi) and can be installed with pip:  

```
pip install --upgrade http-rx
```

Alternatively, you may clone this repository and install from the source code:  

```
python setup.py install
```

---

## Configuration

HTTP Rx is very dynamic and configurable. The health checker 
looks for a `config.json` file in your current directory, or if you specify the `RX_CONFIG` environment variable you can change the path to your config file. 

This JSON config file is structured like so:  

```json
{
  "checks": [
    {
      "type": "rx.check.StatusCodeCheck",
      "expected": 200,
      "url": "https://github.com/zcking"
    },
    ...
  ]
}
```

The `checks` key is a list of health check configurations, 
each of which has the following required settings:  

* `url`  - the HTTP(s) target to request
* `type` - fully qualified Python class; must be a derivative of the `rx.check.Check` base class. Defaults to the `rx.check.StatusCodeCheck` class

The `type` configuration is how you may specify your own custom health check classes when extending http-rx. See the next section on doing just this.

---

## Extending

HTTP Rx is setup in a framework manner, allowing you to easily extend it with your own 
custom health checks, written in Python. 

For example:

Create a fresh virtual environment to install the `http-rx` package:  

```
python3 -m virtualenv venv
source venv/bin/activate
pip install http-rx
```

Then simply create your own custom health check that extends HTTP Rx's `Check` base class:  

```python
"""
content.py
"""

import rx
from rx import check


class CheckContentType(check.Check):
    def __init__(self, conf):
        super().__init__(conf)
        self.expected_content_type = conf.get('expected', 'text/html')
    
    def result(self):
        resp = self.call()
        content_type = resp.headers.get('content-type', None)
        healthy = content_type == self.expected_content_type
        return check.Result(
            resp=resp, 
            is_healthy=healthy, 
            fail_reason=f'expected content type of {self.expected_content_type} but received {content_type}'
        )


if __name__ == '__main__':
    rx.run()

```

And your config file to go along with it:  

```json
{
  "checks": [
    {
      "type": "__main__.CheckContentType",
      "expected": "text/html",
      "url": "https://github.com/zcking"
    }
  ]
}
```

Notice in this simple example that the module name is `__main__` because we're executing it as a script. If you were to write your own Python package with submodules etc. this may not be the case.