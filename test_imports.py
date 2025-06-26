# test_imports.py
try:
    from moviepy.editor import VideoFileClip
    print("✅ MoviePy installed and importable!")
except ModuleNotFoundError:
    print("❌ MoviePy NOT installed!")
