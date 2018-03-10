# Python Service Factory

> An highly opinionated and very convention-driven framework for creating Python "services"

That being said ...

## What is a Service?

_To me_, in the context of Python, a service is a script that runs forever, performing a (few) typical task(s) at regular intervals.

So what's wrong with the following Python code then?

```python
import time

while True:
  # do wonderful things
  time.sleep(5)
```

Nothing :-)

If not that I want my services to be able to talk to each other and maybe do other things, that in the end I don't want to end up having to write every time over and over again.

Let's look at an example and see what actually happens:

## My kind of Service

The following example is a verbatim copy of the `TestService.py` that comes with the package

```python
"""
Minimalistic example showing basic Service creation.
"""
import time

from servicefactory import Service

@Service.API.endpoint(port=1234)
class Test(Service.base):

  def loop(self):
    self.log("looping...")
    time.sleep(5)

  @Service.API.handle("action")
  def handle_action(self, data):
    print "handling action..."
    print data

if __name__ == "__main__":
  Test().run()
```

Run it ...

```bash
$ PYTHONPATH=. python servicefactory/TestService.py 
Test : looping...
Test : looping...
```

Now in a different terminal execute the following `curl` command:

```bash
$ curl http://localhost:1234/action -X POST -d '"hello world"' -H "Content-Type: application/json"
ok
```

And observe the output of the `TestService.py` script:

```bash
Test : looping...
handling action...
"hello world"
```

Now open a python REPL promp:

```python
$ PYTHONPATH=. python
Python 2.7.13 (default, May 24 2017, 12:12:01) 
[GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.42)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from servicefactory import TestService
>>> TestService.Test.perform("action", "hello world")
```

And again observe the output of the `TestService.py` script:

```bash
Test : looping...
handling action...
"hello world"
```

Finally (for now) go back to the running `TestService.py` script and interrupt the script using `Ctrl+c`:

```bash
Test : looping...
^CTest : shutdown requested
$ 
```

### Property 1: Simple implement your `loop`

Let's not waste time writing an event loop, catching `KeyboardInterrupt` and other boilerplate things. Just implement the `Service.base` class and provide your own `loop` method.

### Property 2: Exposed HTTP/JSON API

The service exposes a basic HTTP and JSON based API, which allows interaction with it from outside the process it runs in. 

Exposing functions is as simple as adding a decorator: `@Service.API.handle("some-action")` to a method in the Service class.

### Property 3: ClassMethod-based calling of exposed API

Any Python process with access to the Service class, can call into a running instance of the class using a `classmethod`.

### Property 4: Default exposed functionality

Besides allowing to expose methods through the HTTP/JSON API, the base Service class also implements some standard functionality. Currently the `shutdown` action is provided, which can be called through the HTTP/JSON API of the `perform` class method. And If you interrupt the service you also see it being performed.

More to come ... ;-)