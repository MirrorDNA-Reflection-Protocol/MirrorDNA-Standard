# MirrorDNA Portable - Deployment Guide

**Building and distributing the portable launcher across platforms**

---

## Overview

This guide covers building, packaging, and distributing MirrorDNA Portable for Windows, macOS, and Linux.

**Build Tool**: Electron Builder
**Platforms**: Windows (portable .exe), macOS (.dmg, universal), Linux (AppImage)
**Target**: Fully self-contained executables for USB distribution

---

## Prerequisites

### Development Machine

- **Node.js**: 18.x or higher
- **npm**: 9.x or higher
- **Git**: For cloning/version control
- **Platform-specific tools**:
  - **Windows**: None (builds on any platform)
  - **macOS**: Must build on macOS for DMG signing
  - **Linux**: Requires AppImage tools (fuse, etc.)

### Dependencies

```bash
cd portable/launcher
npm install
```

This installs:
- `electron` (v27+)
- `electron-builder` (v24+)
- `node-llama-cpp` (v2.8+)
- `electron-store` (v8+)
- `marked` (v9+)

---

## Build Commands

### Development Build (Testing)

```bash
npm start
# or
npm run dev
```

Launches the launcher in dev mode with:
- DevTools enabled
- Hot reload on file changes
- Verbose logging

### Production Builds

**All platforms:**
```bash
npm run build
```

**Platform-specific:**
```bash
npm run build:win    # Windows portable executable
npm run build:mac    # macOS DMG (universal binary)
npm run build:linux  # Linux AppImage
```

Build output: `portable/launcher/dist/`

---

## Build Configuration

### electron-builder Settings

Located in `package.json` under `"build"`:

```json
{
  "build": {
    "appId": "com.mirrordna.portable",
    "productName": "MirrorDNA Portable",
    "directories": {
      "output": "dist"
    },
    "files": [
      "src/**/*",
      "../vault-template/**/*",
      "../glyphs/**/*",
      "models/**/*"
    ],
    "extraResources": [
      {
        "from": "../vault-template",
        "to": "vault-template"
      },
      {
        "from": "../../tools",
        "to": "tools"
      }
    ]
  }
}
```

### What Gets Packaged

**Included**:
- ✅ Launcher source (`src/`)
- ✅ Vault template (canonical specs, templates, state structure)
- ✅ Glyphs/icons (sigil, status icons)
- ✅ Tools (checksums, validators)
- ✅ Models directory (empty, ready for user's GGUF files)

**Excluded** (via `.gitignore`):
- ❌ `node_modules/` (bundled by Electron)
- ❌ `*.gguf` model files (too large for repo/distribution)
- ❌ Dev files (`.DS_Store`, etc.)

---

## Platform-Specific Notes

### Windows (Portable .exe)

**Target**: `portable` (single .exe, no installer)

**Build**:
```bash
npm run build:win
```

**Output**: `dist/MirrorDNA Portable.exe` (~150MB)

**Features**:
- No installation required
- Runs directly from USB
- Settings stored in `%APPDATA%` or portable folder (configurable)

**Distribution**:
1. Copy `.exe` to USB root
2. Include `README.txt` with basic instructions
3. Optional: Add `vault-template/` folder pre-extracted

### macOS (DMG)

**Target**: `dmg` (drag-to-Applications)

**Build** (must be on macOS):
```bash
npm run build:mac
```

**Output**: `dist/MirrorDNA Portable-1.0.0-universal.dmg` (~200MB)

**Features**:
- Universal binary (Intel + Apple Silicon)
- Standard macOS app structure
- Gatekeeper-compatible (if signed)

**Code Signing** (optional but recommended):
```bash
export CSC_LINK="/path/to/certificate.p12"
export CSC_KEY_PASSWORD="your_password"
npm run build:mac
```

**Distribution**:
1. Mount DMG
2. Drag `MirrorDNA Portable.app` to Applications
3. Or run directly from USB (slower first launch)

### Linux (AppImage)

**Target**: `AppImage` (universal binary)

**Build**:
```bash
npm run build:linux
```

**Output**: `dist/MirrorDNA-Portable-1.0.0.AppImage` (~180MB)

**Features**:
- Single executable, no installation
- Works on most Linux distros (kernel 4.4+)
- Requires FUSE (usually pre-installed)

**Make executable**:
```bash
chmod +x "MirrorDNA-Portable-1.0.0.AppImage"
```

**Distribution**:
1. Copy AppImage to USB
2. Mark as executable
3. Run directly

---

## File Size Optimization

### Current Sizes (Approximate)

- **Windows**: ~150MB
- **macOS**: ~200MB (universal)
- **Linux**: ~180MB

### What Makes Them Large

1. **Electron runtime**: ~100MB (Chromium + Node.js)
2. **node-llama-cpp binaries**: ~30MB
3. **Vault template + tools**: ~5MB
4. **UI assets**: ~2MB

### Reducing Size

**Not recommended** (breaks functionality):
- Removing Electron runtime
- Removing llama.cpp binaries

**Recommended**:
- Use `--target` for specific architectures (e.g., `x64` only)
- Remove unused Electron APIs via `asar`
- Compress with UPX (Windows only, experimental)

Example for Windows x64 only:
```bash
electron-builder --win --x64
```

---

## Testing Builds

### Pre-Distribution Checklist

**Functional Tests**:
- [ ] Launch without errors
- [ ] Onboarding flow completes
- [ ] Vault creation works
- [ ] Session persistence across restarts
- [ ] LLM initialization (with and without model)
- [ ] Consent dialog appears in hybrid mode
- [ ] Settings persist
- [ ] Vault selection works
- [ ] Model file picker works

**Platform-Specific**:
- [ ] **Windows**: Run from USB, test on clean VM
- [ ] **macOS**: Test on Intel and Apple Silicon
- [ ] **Linux**: Test on Ubuntu, Fedora, Arch

**Performance**:
- [ ] Cold start: < 5 seconds (without model)
- [ ] Model load: 30-60 seconds (Phi-3 Mini)
- [ ] Session save: < 1 second

---

## Distribution Methods

### USB Drive Distribution

**Structure**:
```
USB Root/
├── MirrorDNA-Portable.exe        (Windows)
├── MirrorDNA-Portable.app/       (macOS)
├── MirrorDNA-Portable.AppImage   (Linux)
├── README.txt                     (Quick start)
├── vault-template/                (Optional: Pre-extracted)
└── models/                        (Empty, for user's GGUF files)
```

**Instructions** (README.txt):
```
MirrorDNA Portable - Quick Start

1. Run the launcher for your platform:
   - Windows: Double-click MirrorDNA-Portable.exe
   - macOS: Open MirrorDNA-Portable.app
   - Linux: chmod +x and run MirrorDNA-Portable.AppImage

2. Choose "I'm New" and follow onboarding

3. Optional: Download Phi-3 Mini model
   - Place in models/ folder on this USB
   - See models/README.md for download instructions

4. Your vault will be created on this USB for portability

For more info: https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard
```

### Web Download Distribution

**GitHub Releases**:
1. Tag version: `git tag v1.0.0 && git push --tags`
2. Build all platforms
3. Upload to GitHub Releases:
   - `MirrorDNA-Portable-1.0.0-win.exe`
   - `MirrorDNA-Portable-1.0.0-mac-universal.dmg`
   - `MirrorDNA-Portable-1.0.0-linux.AppImage`
4. Include SHA256 checksums
5. Add release notes

**Checksums**:
```bash
shasum -a 256 dist/* > SHA256SUMS.txt
```

---

## Troubleshooting Build Issues

### "command not found: electron-builder"

**Fix**:
```bash
npm install --save-dev electron-builder
```

### macOS code signing fails

**Fix**: Either:
1. Disable signing (dev only): `export CSC_IDENTITY_AUTO_DISCOVERY=false`
2. Or provide certificate: `export CSC_LINK="/path/to/cert.p12"`

### Linux AppImage won't run

**Fix**: Install FUSE
```bash
# Ubuntu/Debian
sudo apt install libfuse2

# Fedora
sudo dnf install fuse

# Arch
sudo pacman -S fuse2
```

### Build fails with "out of memory"

**Fix**: Increase Node.js memory
```bash
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

### node-llama-cpp binary missing

**Fix**: Rebuild native modules
```bash
npm rebuild node-llama-cpp --build-from-source
```

---

## CI/CD Integration

### GitHub Actions (Example)

```yaml
name: Build MirrorDNA Portable

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        working-directory: ./portable/launcher
        run: npm install

      - name: Build
        working-directory: ./portable/launcher
        run: npm run build

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: ${{ matrix.os }}-build
          path: portable/launcher/dist/*
```

---

## Security Considerations

### Code Signing

**Importance**: Prevents "unverified developer" warnings

**Windows**:
- Requires EV Code Signing Certificate (~$300/year)
- Use `electron-builder` with `certificateFile` and `certificatePassword`

**macOS**:
- Requires Apple Developer Account ($99/year)
- Use `electron-builder` with `CSC_*` environment variables
- Notarize with `electron-notarize`

**Linux**:
- No signing required, but provide PGP signatures for checksums

### Sandboxing

**Current**: None (requires filesystem access for vault operations)

**Future**: Consider:
- Electron sandbox for renderer process
- Prompt for filesystem access on first launch

---

## Updating Distributed Builds

### Auto-Update (Not Yet Implemented)

**Planned**: electron-updater integration
- Check for updates on launch (with consent)
- Download delta updates (save bandwidth)
- Apply updates on restart

**Implementation**:
```bash
npm install electron-updater
```

In `main.js`:
```javascript
const { autoUpdater } = require('electron-updater');

// Check for updates (with user consent)
if (internetMode === 'online') {
  autoUpdater.checkForUpdates();
}
```

### Manual Update

**Instructions for users**:
1. Download new version
2. Replace old executable
3. Vault data remains intact (separate from app)

---

## Deployment Checklist

Before releasing a new version:

- [ ] Bump version in `package.json`
- [ ] Update CHANGELOG.md
- [ ] Run all tests: `npm test`
- [ ] Build all platforms
- [ ] Test builds on clean systems
- [ ] Generate SHA256 checksums
- [ ] Create GitHub release
- [ ] Upload binaries + checksums
- [ ] Tag release: `git tag v1.x.x`
- [ ] Announce in discussions/docs

---

## License & Distribution Rights

MirrorDNA Portable follows the license in the repository root (`../../LICENSE.md`).

**Distribution**: Permitted under license terms
**Modification**: Permitted with attribution
**Commercial use**: See license for restrictions

---

## Support

**Issues**: https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/issues
**Discussions**: https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/discussions

---

⟡ **Build with sovereignty. Distribute with trust.**
