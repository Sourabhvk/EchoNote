# 🔧 Dependency Check Guide

## Quick Start

Run the dependency checker before starting any EchoNote work:

```bash
python check_dependencies.py
```

### What it does:
✅ Reads `requirements.txt`  
✅ Checks which packages are already installed  
✅ Shows missing dependencies  
✅ Asks for confirmation, then auto-installs missing packages  

---

## Usage Examples

### 1. **Auto-Check on Startup** (add to your Pipeline)
Add this to the top of `src/Pipeline.py`:
```python
from pathlib import Path
import sys

# Add root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Check dependencies before running
import subprocess
result = subprocess.run([sys.executable, "check_dependencies.py"], cwd=Path(__file__).parent.parent)
if result.returncode != 0:
    print("⚠️  Dependency check failed. Exiting.")
    sys.exit(1)

# Rest of your code...
```

### 2. **Silent Mode** (for automated environments)
```bash
python check_dependencies.py --silent
```
(Not yet implemented - can add if needed)

### 3. **Check Only (don't install)**
```bash
python check_dependencies.py --check-only
```
(Not yet implemented - can add if needed)

---

## For RWTH HPC

On HPC clusters without internet, pre-download packages:

```bash
# On your laptop WITH internet:
pip download -r requirements.txt -d ./wheels

# Transfer wheels/ folder to HPC, then:
pip install --no-index --find-links ./wheels -r requirements.txt
```

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'faster_whisper'"**  
→ Run `python check_dependencies.py` to install it

**"pip not found"**  
→ Use: `python -m pip` instead of `pip`

**Permission denied on HPC**  
→ Use: `python -m pip install --user -r requirements.txt`

---

