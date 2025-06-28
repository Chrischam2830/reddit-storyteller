import sys
import moviepy
print("moviepy imported:", moviepy.__file__)
try:
    import moviepy.editor
    print("moviepy.editor imported OK:", moviepy.editor.__file__)
except Exception as e:
    print("moviepy import error:", e)

import os
print("PYTHONPATH:", sys.path)
print("Site-packages listing for moviepy:")
try:
    print(os.listdir('/usr/local/lib/python3.11/site-packages/moviepy'))
except Exception as e:
    print("Error listing site-packages/moviepy:", e)
