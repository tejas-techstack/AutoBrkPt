import debugpy

debugpy.listen(("localhost", 5678))

# Wait for the debugger to attach
print("Waiting for debugger to attach...")
debugpy.wait_for_client()

import tester
