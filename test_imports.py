# test_imports.py
try:
    import moviepy.editor
    print("✅ moviepy.editor IMPORTED")
except ImportError as e:
    print("❌ moviepy.editor NOT IMPORTED:", e)

try:
    import PIL
    print("✅ Pillow IMPORTED")
except ImportError as e:
    print("❌ Pillow NOT IMPORTED:", e)
