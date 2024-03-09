import debugpy

# Set up the debugger to listen for incoming connections
debugpy.listen(("localhost", 5678))

# Wait for the debugger to attach
print("Waiting for debugger to attach...")
debugpy.wait_for_client()

# Set a breakpoint at line 5 of the current file

# Your code here
x = 1
print("before bp1")
debugpy.breakpoint()


y = 1

z = x + y

print("before bp2")

print(z)

