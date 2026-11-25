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
    f.write("\nnxApp=bananalite\nnxLabel=Banana Lite\nnxVersion=0.2-experimental\nnxVersionCode=2\n")

p = java / "Prefs.java"
# Use Android's low-RAM flag and physical RAM rather than a specific chipset.
replace(p, 'static boolean ramSaver(Context c, String titleId) { return of(c).getBoolean(gameKey("ram_saver", titleId), false); }', '''static boolean liteLowMemory(Context c) {
        android.app.ActivityManager am = c.getSystemService(android.app.ActivityManager.class);
        if (am == null) return false;
        android.app.ActivityManager.MemoryInfo info = new android.app.ActivityManager.MemoryInfo();
        am.getMemoryInfo(info);
        return am.isLowRamDevice() || (info.totalMem > 0 && info.totalMem <= 6L * 1024 * 1024 * 1024);
    }
    static boolean ramSaver(Context c, String titleId) { return of(c).getBoolean(gameKey("ram_saver", titleId), false); }''')
# Preserve upstream FP16, fast-core and strong RAM saver defaults.
p = java / "Lsfg.java"
replace(p, 'getBoolean("lsfg", false)', 'getBoolean("lsfg", true)')
replace(p, 'getInt("lsfg_flow", 50)', 'getInt("lsfg_flow", Prefs.liteLowMemory(c) ? 25 : 50)')
print("Applied experimental adaptive defaults; native compilation still required.")

# v0.2: conservative rendering defaults and distinct branding.
p = java / "Prefs.java"
replace(p, 'getBoolean(gameKey("vk_classic_rp", titleId), false)', 'getBoolean(gameKey("vk_classic_rp", titleId), liteLowMemory(c))')
replace(p, 'getInt("ui_theme", 0)', 'getInt("ui_theme", 2)')
replace(p, 'getInt("ui_background", 0)', 'getInt("ui_background", 1)')
replace(p, 'return Signer.buildTag(BuildConfig.NX_PLAY, buildId());', 'return "Banana Lite 0.2 · " + buildId();')
replace(p, 'WINDOW_DEFAULT = "1920x1080"', 'WINDOW_DEFAULT = "848x480"')
replace(p, '"960x540", "848x480"},', '"960x540", "848x480", "640x360", "426x240"},')
replace(p, 'Tx.s(R.string.game_phone_480p_848x480)},', 'Tx.s(R.string.game_phone_480p_848x480), "Lite 360p (640x360)", "Ultra Lite 240p (426x240)"},')
replace(p, '"540p", "480p"};', '"540p", "480p", "360p", "240p"};')
res = root / "android/app/src/main/res"
replace(res / "values/colors.xml", '#FF1E5B3A', '#FF17171C')
icon = """<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
<path android:fillColor="#FFFFD43B" android:pathData="M25,35 Q34,77 79,43 L83,49 Q72,81 43,78 Q24,73 25,35 Z"/>
<path android:fillColor="#FFFFFFFF" android:pathData="M57,24 L43,48 L55,48 L49,67 L70,40 L57,40 Z"/>
</vector>"""
(res / "drawable/ic_launcher_foreground.xml").write_text(icon)
(res / "drawable/ic_launcher_monochrome.xml").write_text(icon)
print("v0.2 experimental compatibility and branding changes applied.")
