import sys
def try_import(name):
    try:
        m = __import__(name)
        v = getattr(m, "__version__", "unknown")
        print(f"{name}: OK (version {v})")
    except Exception as e:
        print(f"{name}: FAIL ({e})")

print("Python:", sys.version.splitlines()[0])
for pkg in ("pyspark","pandas","numpy","sklearn","matplotlib","seaborn","yaml"):
    try_import(pkg)
