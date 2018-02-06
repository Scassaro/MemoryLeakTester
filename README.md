# MemoryLeakTester

This program tests MXK-F 219 provisioning for memory leaks.

Requirements:
- Python 3: goes without saying that this is necessary.
- Python library "telnetlib": honestly can't remember if this is included with the Python default libraries, but it is still needed regardless.

WARNING:

MXK-F bulk provisioning is extremely slow (especially my test, 1024 ONUs). This program will take at least half an hour to complete 1 pass, making your 219 mostly unusable for that time period. Use at your own risk!
