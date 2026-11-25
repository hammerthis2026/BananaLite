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
    f.write("\nnxApp=bananalite\nnxLabel=Banana Lite\nnxVersion=0.3.0-experimental\nnxVersionCode=3\n")

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
replace(p, 'return Signer.buildTag(BuildConfig.NX_PLAY, buildId());', 'return "Banana Lite 0.3 · " + buildId();')
replace(p, 'WINDOW_DEFAULT = "1920x1080"', 'WINDOW_DEFAULT = "848x480"')
replace(p, '"960x540", "848x480"},', '"960x540", "848x480", "640x360", "426x240"},')
replace(p, 'Tx.s(R.string.game_phone_480p_848x480)},', 'Tx.s(R.string.game_phone_480p_848x480), "Lite 360p (640x360)", "Ultra Lite 240p (426x240)"},')
replace(p, '"540p", "480p"};', '"540p", "480p", "360p", "240p"};')
res = root / "android/app/src/main/res"
colors = res / 'values/colors.xml'
colors.write_text(colors.read_text().replace('#FF1E5B3A', '#FF17171C'))
icon = """<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
<path android:fillColor="#FFFFD43B" android:pathData="M25,35 Q34,77 79,43 L83,49 Q72,81 43,78 Q24,73 25,35 Z"/>
<path android:fillColor="#FFFFFFFF" android:pathData="M57,24 L43,48 L55,48 L49,67 L70,40 L57,40 Z"/>
</vector>"""
(res / "drawable/ic_launcher_foreground.xml").write_text(icon)
(res / "drawable/ic_launcher_monochrome.xml").write_text(icon)
print("v0.2 experimental compatibility and branding changes applied.")

# Add a dedicated per-game Lite control card.
p = java / "GameSettings.java"
replace(p, 'if (perf) Ui.add(content, Ui.statusChip(a, chipText(a, id)), 12, Ui.wrap());', '''if (perf) {
            Ui.add(content, Ui.statusChip(a, chipText(a, id)), 12, Ui.wrap());
            LinearLayout lite = Ui.add(content, Ui.card(a), 12);
            lite.setPadding(Ui.dp(a, 14), Ui.dp(a, 12), Ui.dp(a, 14), Ui.dp(a, 12));
            lite.addView(Ui.text(a, "BANANA LITE / PERFORMANCE", 15, R.color.bn_text, 700));
            lite.addView(new Ui.Setting(a, "⚡", "Apply Lite preset", v ->
                new PadFocus.Builder(a).setTitle("Performance preset")
                .setItems(new String[]{"Ultra Lite · 360p / 30 fps", "Balanced · 540p / 30 fps", "Performance · 720p / 60 fps", "Ultra Lite 60 · 360p / 60 fps", "Full HD · 1080p / 60 fps", "Custom · keep current settings"}, (d, k) -> {
                    if (k < 5) {
                        Prefs.gameWindow(a, id, new String[]{"640x360", "960x540", "1280x720", "640x360", "1920x1080"}[k]);
                        keepAdvanced(a, g);
                        Prefs.fpsCap(a, id, k >= 2 ? 60 : 30);
                        Prefs.classicPasses(a, id, k != 2);
                        Prefs.fp16(a, id, false);
                        Prefs.ramSaverStrong(a, id, false);
                        Prefs.ramSaver(a, id, false);
                        Prefs.customPicked(a, id, true);
                    }
                    again.run();
                }).setNegativeButton(android.R.string.cancel, null).show())
                .value("Changes resolution, frame cap and rendering settings").chevron(a).view);
            lite.addView(new Ui.Setting(a, "🛠", "Safe rendering recovery", v -> {
                Prefs.classicPasses(a, id, true);
                Prefs.fp16(a, id, false);
                Prefs.instancedDraws(a, id, false);
                Prefs.ramSaverStrong(a, id, false);
                Prefs.ramSaver(a, id, false);
                again.run();
            }).value("Experimental fallback for missing geometry; restart game").chevron(a).view);
            lite.addView(new Ui.Setting(a, "💾", "Auto backup before play", null)
                .value("At most once daily; uses existing verified save backup")
                .toggle(a, Prefs.of(a).getBoolean("lite_auto_backup", false), (b, x) ->
                    Prefs.of(a).edit().putBoolean("lite_auto_backup", x).commit()).view);
        }''')
p = java / "Overlay.java"
replace(p, '%.0f→%.0f fps', 'Native %.0f | Output %.0f fps')
replace(p, 'line(s, "no LSFG")', 'line(s, "FG unavailable")')
replace(p, 'line(s, "LSFG")', 'line(s, "FG active")')
p = java / "Lsfg.java"
replace(p, 'st.setText(status);', 'st.setText(status + "\\nA detected DLL is not proof of active FG. Check the in-game overlay for FG active and output FPS.");')
# Optional daily backup on a background thread before game launch.
p = java / "MainActivity.java"
replace(p, 'private void start(Game g) {', '''private boolean liteBackupBusy;
    private void start(Game g) {
        if (liteBackupBusy) return;
        String key = "lite_backup_day@" + g.titleId;
        long day = System.currentTimeMillis() / 86400000L;
        File save = Folders.save(this, g);
        if (!Prefs.of(this).getBoolean("lite_auto_backup", false) || Prefs.of(this).getLong(key, -1) == day || save == null) {
            liteStart(g); return;
        }
        liteBackupBusy = true;
        new Thread(() -> {
            String error = null;
            try {
                if (SaveStore.hasFiles(save) || SaveStore.hasFiles(new File(save.getPath() + "_device"))) {
                    SaveStore.backup(save, SaveUi.target(this, g), SaveUi.stamp() + "-auto");
                    Prefs.of(this).edit().putLong(key, day).commit();
                }
            } catch (Exception e) { error = e.toString(); }
            final String failure = error;
            runOnUiThread(() -> {
                liteBackupBusy = false;
                if (isFinishing() || isDestroyed()) return;
                if (failure == null) liteStart(g);
                else new PadFocus.Builder(this).setTitle("Auto backup failed").setMessage(failure)
                    .setPositiveButton("Play without backup", (d, w) -> liteStart(g))
                    .setNegativeButton(android.R.string.cancel, null).show();
            });
        }).start();
    }

    private void liteStart(Game g) {''')
print("Applied Lite presets, safe rendering control, optional backups and FG overlay labels.")

# Reuse upstream updater with a fixed Banana Lite release source.
p = java / "Updater.java"
data = p.read_text()
start = data.index("    static List<UpdateCheck.Source> sources(Context c) {")
end = data.index("\n    }", start) + len("\n    }")
p.write_text(data[:start] + '''    static List<UpdateCheck.Source> sources(Context c) {
        return java.util.Collections.singletonList(UpdateCheck.github("hammerthis2026/BananaLite"));
    }''' + data[end:])
replace(p, 'return override(c).getOrDefault("version", BuildConfig.VERSION_NAME);', 'return BuildConfig.VERSION_NAME;')
p = java / "UpdateCheck.java"
replace(p, 'GITHUB_HOST, "objects.githubusercontent.com");', 'GITHUB_HOST, "objects.githubusercontent.com", "release-assets.githubusercontent.com");')
replace(res / "values/strings.xml", '<string name="settings_banana_native_version">Banana Native %1$s</string>', '<string name="settings_banana_native_version">Banana Lite %1$s</string>')
print("Configured Banana Lite in-app release updates.")

# v0.3: explicit LSFG diagnostics without pretending a detected DLL is usable.
p = java / "Lsfg.java"
replace(p, 'st.setText(status + "\\nA detected DLL is not proof of active FG. Check the in-game overlay for FG active and output FPS.");', '''File detected = privateCopy(c);
        st.setText(status + "\\nNative LSFG build: " + BuildConfig.NX_LSFG
            + "\\nPrivate DLL: " + (looksLikeDll(detected) ? detected.length() + " bytes" : "not detected")
            + "\\nRequested: " + (on(c) ? "on" : "off") + ", " + multiplier(c) + "x, flow " + flow(c) + "%"
            + "\\nDisplay limit: " + maxHz(c) + " Hz"
            + "\\nRestart after replacing the DLL. A detected DLL does not prove initialization succeeded.");''')

# v0.3 compatibility: preset labels and resolution already updated above.
p = java / "GameSettings.java"
replace(p, 'Prefs.classicPasses(a, id, k != 2);', 'Prefs.classicPasses(a, id, true);\n                        Prefs.instancedDraws(a, id, false);\n                        GameUpscaler.mode(a, id, GameUpscaler.MODE_FSR);\n                        GameUpscaler.sharp(a, id, 0.25f);')

# Prefer an explicitly imported DLL over automatic discovery.
p = java / "Lsfg.java"
replace(p, 'File copy = privateCopy(c);', '''File copy = privateCopy(c);
        if (prefs(c).getBoolean("lite_lsfg_manual", false) && looksLikeDll(copy)) {
            note = "Using manually imported Lossless.dll";
            return copy;
        }''')
replace(p, 'note = Tx.s(R.string.game_lossless_dll_picked_by_hand);', '''prefs(c).edit().putBoolean("lite_lsfg_manual", true).commit();
        note = Tx.s(R.string.game_lossless_dll_picked_by_hand);''')
replace(p, 'env.add("DM_LSFG=" + (on(c) ? 1 : 0));', 'env.add("DM_LSFG=" + (on(c) && dll != null ? 1 : 0));')
# Use existing single-pass SGSR on Ultra Lite to limit upscaling cost.
p = java / "GameSettings.java"
replace(p, 'GameUpscaler.mode(a, id, GameUpscaler.MODE_FSR);', 'GameUpscaler.mode(a, id, (k == 0 || k == 3) ? GameUpscaler.MODE_DEFAULT : GameUpscaler.MODE_FSR);')
print("Applied manual LSFG priority and lightweight upscaling preset.")

# v0.3: expose existing runtime log sharing and cover picker on Home.
p = java / "MainActivity.java"
replace(p, 'top.addView(logo);', '''top.addView(logo);
        TextView liteBrand = Ui.heading(this, "BANANA LITE");
        liteBrand.setTextColor(0xffffd43b);
        top.addView(liteBrand);''')
replace(p, 'help.addView(new Ui.Setting(this, "📨", Tx.s(R.string.common_share_log), v -> shareLog()).value(Tx.s(R.string.settings_the_newest_log)).chevron(this).view);', '''help.addView(new Ui.Setting(this, "📨", "Export diagnostic log", v -> shareLog()).value("Share the latest game runtime log").chevron(this).view);''')
print("Exposed runtime diagnostics and selected single-pass SGSR for Lite presets.")
