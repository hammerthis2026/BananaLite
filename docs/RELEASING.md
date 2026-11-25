# Banana Lite release process

Before publishing, compile and test the APK on a device. Use a permanent release signing key, stored privately, never committed to Git. Keep an offline backup of the key. Configure signing credentials as encrypted GitHub Actions secrets only after verifying the upstream signing process.

Verify the final APK with Android SDK apksigner verify --print-certs. Compare the certificate with the previous release and ensure versionCode increases. A debug-signed prototype may require a one-time reinstall; export saves before uninstalling.

Publish the verified signed APK on the repository's GitHub Releases page with a unique version tag and release notes. Test the in-app updater from the previous version before announcing availability. Preserve upstream licenses and source obligations. Do not publish proprietary game data or DLLs.

Never publish an untested build as a stable release.

## v0.4 automatic update milestone

Trigger CI automatically on versioned release tags; publish only successfully built, verified APKs to GitHub Releases. Configure a persistent private signing key before enabling publishing. Expose Check for updates and Update now in the app using the existing release updater. Never embed GitHub credentials in the APK. Android installation confirmation remains required. Test an upgrade preserving saves before enabling automatic releases.
