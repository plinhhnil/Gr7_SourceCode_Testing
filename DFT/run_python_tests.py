import sys
import unittest
from pathlib import Path


test_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(test_dir.parent))
suite = unittest.defaultTestLoader.discover(
    str(test_dir),
    pattern="test_*.py",
    top_level_dir=str(test_dir),
)
result = unittest.TextTestRunner(stream=sys.stdout, verbosity=0).run(suite)
sys.exit(not result.wasSuccessful())
