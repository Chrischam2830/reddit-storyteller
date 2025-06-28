try:
    import moviepy
    print("moviepy imported:", moviepy.__file__)
    import moviepy.editor
    print("moviepy.editor imported successfully")
except Exception as e:
    print("moviepy import error:", e)

import sys
print("PYTHONPATH:", sys.path)
