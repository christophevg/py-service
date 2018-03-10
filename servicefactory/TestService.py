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
