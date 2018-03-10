# Python Service Factory

> A highly opinionated and very convention-driven framework for creating Python "services"

That being said, below the Getting Started section I provide some rationale ... But first...

## Getting Started

This Service Factory is hosted on [PyPi](https://pypi.org/project/servicefactory/), so using it is super easy (I've stripped the output to focus on your actions):

```bash
$ mkdir my-service-project
$ cd my-service-project/
$ virtualenv venv
$ . venv/bin/activate
(venv) $ pip install servicefactory
```

Now read on for some background information and a complete example that you can paste into e.g. `TestService.py` and run it as shown below.

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

  def finalize(self):
    self.log("finalizing...")

  @Service.API.handle("action")
  def handle_action(self, data):
    print("handling action...")
    print(data)

if __name__ == "__main__":
  Test().run()
```

Preliminary step: setup your minimal environment (when running directory from the repository):

```bash
$ virtualenv venv
Using base prefix '/usr/local/Cellar/python3/3.6.1/Frameworks/Python.framework/Versions/3.6'
New python executable in /Users/xtof/Workspace/2know/novid/py-servicefactory/venv/bin/python3.6
Also creating executable in /Users/xtof/Workspace/2know/novid/py-servicefactory/venv/bin/python
Installing setuptools, pip, wheel...done.

$ . venv/bin/activate

(venv) $ pip install -r requirements.txt 
Collecting Werkzeug==0.14.1 (from -r requirements.txt (line 1))
  Using cached Werkzeug-0.14.1-py2.py3-none-any.whl
Installing collected packages: Werkzeug
Successfully installed Werkzeug-0.14.1
```

Run it ...

```bash
(venv) $ PYTHONPATH=. python servicefactory/TestService.py
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
b'hello world'
```

Now open a python REPL promp:

```bash
(venv) $ PYTHONPATH=. python
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
b'hello world'
```

Finally (for now) go back to the running `TestService.py` script and interrupt the script using `Ctrl+c`:

```bash
Test : looping...
^CTest : shutdown requested
Test : finalizing...

(venv) $ deactivate

$ 
```

### Property 1: Simply implement your `loop`

Let's not waste time writing an event loop, catching `KeyboardInterrupt` and other boilerplate things. Just implement the `Service.base` class and provide your own `loop` method.

> If you know [Arduino](https://www.arduino.cc) you might recognise this function from that paradigm. I've not included a `setup()` counterpart, since you can do this in your class'  `__init__(self)` constructor ;-)

### Property 2: Exposed HTTP/JSON API

The service exposes a basic HTTP and JSON based API, which allows interaction with it from outside the process it runs in. 

Exposing functions is as simple as adding a decorator: `@Service.API.handle("some-action")` to a method in the Service class.

### Property 3: Class Method to call the exposed API

Any Python process with access to the Service class, can call into a running instance of the class using a `classmethod`. For now this is a single `perform(self, action, data)` method.

### Property 4: Default exposed functionality

Besides allowing to expose methods through the HTTP/JSON API, the base Service class also implements some standard functionality. Currently the `shutdown` action is provided, which can be called through the HTTP/JSON API of the `perform` class method. And If you interrupt the service you also see it being performed.

More to come ... ;-)
