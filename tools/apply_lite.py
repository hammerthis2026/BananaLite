"""Apply experimental Banana Lite defaults to a clean upstream source tree."""
from pathlib import Path
import sys

root = Path(sys.argv[1])
java = root / "android/app/src/main/java/dev/nxnative/android"

def replace(path, old, new):
    data = path.read_text()
    if data.count(old) != 1:
        raise RuntimeError(f"Unexpected upstream source: {path}: {old}")
    path.write_text(data.replace(old, new))

p = root / "android/app/gradle.properties"
with p.open("a") as f:
    f.write("\nnxApp=bananalite\nnxLabel=Banana Lite\nnxVersion=0.1-prototype\n")

p = java / "Prefs.java"
# Use Android's low-RAM flag and physical RAM rather than a specific chipset.
replace(p, 'static boolean ramSaver(Context c, String titleId) { return of(c).getBoolean(gameKey("ram_saver", titleId), false); }', '''static boolean liteLowMemory(Context c) {
        android.app.ActivityManager am = c.getSystemService(android.app.ActivityManager.class);
        if (am == null) return false;
        android.app.ActivityManager.MemoryInfo info = new android.app.ActivityManager.MemoryInfo();
        am.getMemoryInfo(info);
        return am.isLowRamDevice() || (info.totalMem > 0 && info.totalMem <= 6L * 1024 * 1024 * 1024);
    }
    static boolean ramSaver(Context c, String titleId) { return of(c).getBoolean(gameKey("ram_saver", titleId), liteLowMemory(c)); }''')
# Preserve upstream FP16, fast-core and strong RAM saver defaults.
p = java / "Lsfg.java"
replace(p, 'getBoolean("lsfg", false)', 'getBoolean("lsfg", true)')
replace(p, 'getInt("lsfg_flow", 50)', 'getInt("lsfg_flow", Prefs.liteLowMemory(c) ? 25 : 50)')
print("Applied experimental adaptive defaults; native compilation still required.")
