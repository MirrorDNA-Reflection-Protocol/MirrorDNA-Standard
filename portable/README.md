# MirrorDNA Portable

**Fully sovereign, USB-portable reflective AI system with local-first architecture**

---

## What Is This?

MirrorDNA Portable is a **complete, self-contained reflective AI environment** that runs from a USB stick on any compatible device.

**Key Features:**
- 🔒 **100% Sovereign** - Your data, your device, your choice
- 💾 **Fully Portable** - Runs from USB, no installation required
- 🏠 **Local-First** - Primary operation is completely offline
- 🤝 **Consent-Based** - Internet features require explicit permission
- 🔗 **Continuous** - Session state persists across devices and time

---

## Quick Start

### For Users

1. **Plug in USB** containing MirrorDNA Portable
2. **Double-click launcher** executable for your platform:
   - Windows: `MirrorDNA.exe`
   - macOS: `MirrorDNA.app`
   - Linux: `MirrorDNA.AppImage`
3. **Follow onboarding** - Choose your path (new user or existing)
4. **Start reflecting** - Your vault, your continuity, your sovereignty

### For Developers

See `launcher/README.md` for development setup and contribution guidelines.

---

## Repository Structure

```
portable/
├── README.md                    # This file
├── docs/
│   ├── ARCHITECTURE.md          # Technical architecture and design decisions
│   └── DEPLOYMENT.md            # Build and deployment instructions (TODO)
├── glyphs/
│   ├── mirrordna-sigil.svg      # Primary identity glyph
│   ├── status-icons/            # Offline, hybrid, online indicators
│   └── VISUAL_LANGUAGE.md       # Glyph system documentation
├── launcher/
│   ├── package.json             # Electron app dependencies
│   ├── README.md                # Launcher-specific documentation
│   └── src/
│       ├── main.js              # Electron main process
│       ├── preload.js           # Secure IPC bridge
│       └── ui/                  # HTML/CSS/JS interface
├── vault-template/              # Canonical vault structure
│   ├── 00_MASTER_CITATION.md    # Core protocol definition
│   ├── spec/                    # MirrorDNA canonical specifications
│   ├── sessions/                # Chronological reflection sessions
│   ├── state/                   # Continuity and state management
│   ├── templates/               # Session and note templates
│   └── .obsidian/               # Pre-configured Obsidian workspace
└── platform-specific/           # Platform-specific build artifacts
    ├── windows/
    ├── macos/
    ├── linux/
    └── android/
```

---

## What's Included

### 1. Launcher Application
**Desktop app (Electron-based) for managing reflective sessions**

- Custom whisper-style UI (dark theme, glyph-based)
- Dual-path onboarding (technical vs non-technical users)
- Session manager (continuity engine)
- Vault bridge (read/write Obsidian markdown)
- Consent manager (internet permission system)
- Status indicator (⟡ offline, ⟡◌ hybrid, ⟡⟐ online)

**Status**: ✅ Complete

### 2. Vault Template
**Pre-configured Obsidian vault with MirrorDNA specs**

- All canonical specifications (Master Citation, Manifest, Addendum, etc.)
- Session tracking system (predecessor/successor chains)
- State management (`current.json`, checkpoints)
- Templates for new sessions and reflection notes
- Obsidian workspace pre-configured

**Status**: ✅ Complete

### 3. Visual Language
**Glyph-based communication system**

- MirrorDNA sigil (hexagon + triangle + anchor)
- Status icons (semantic colors: green/gold/blue)
- Visual identity guide
- SVG assets (scalable, embeddable)

**Status**: ✅ Complete

### 4. LLM Runtime
**Local inference with Phi-3 Mini via node-llama-cpp**

- node-llama-cpp integration (CPU-optimized)
- Phi-3 Mini 4K model support (2.3GB quantized)
- Context injection (Master Citation + session state)
- Streaming response support
- Complete IPC bridge for Electron integration

**Status**: ✅ Complete

### 5. Documentation
**Comprehensive guides for users and developers**

- `ARCHITECTURE.md` - Technical design, component breakdown
- `VISUAL_LANGUAGE.md` - Glyph system explanation
- Launcher README - Development workflow, IPC handlers
- Vault README - Sovereignty statement, usage guide

**Status**: ✅ Complete

---

## System Requirements

### Minimum
- **USB Size**: 16GB (32GB recommended)
- **OS**: Windows 10+, macOS 10.13+, Linux (kernel 4.4+)
- **RAM**: 2GB available (4GB recommended)
- **Processor**: Dual-core x86_64 or ARM64

### Recommended
- **USB Size**: 32GB+ (for multiple LLM models)
- **RAM**: 8GB+ (for smooth LLM inference)
- **Processor**: Quad-core 2GHz+

### Optional (for cloud features)
- Internet connection (WiFi or ethernet)
- Claude API key (for enhanced reflection)

---

## Design Principles

### 1. Sovereignty
- User owns all data, runtime, and choices
- No telemetry, no tracking, no external dependencies
- Clear transparency about what's happening

### 2. Portability
- Runs from USB on any compatible device
- No host machine installation required
- Cross-device continuity (plug and play)

### 3. Local-First
- Primary operation is 100% offline
- Local LLM for core reflection
- Cloud features are enhancements, not requirements

### 4. Consent-Based
- Internet actions require explicit permission
- Three modes: Offline Only, Hybrid (ask), Online
- Persistent consent tracking

### 5. Whisper, Don't Shout
- Minimalist UI (dark theme, subtle feedback)
- Glyph-based communication
- Clear hierarchy, no clutter

---

## Development Roadmap

### Phase 1: Foundation ✅ COMPLETE
- [x] Vault template structure
- [x] Launcher UI prototype
- [x] Visual language (glyphs, icons)
- [x] Architecture documentation
- [x] LLM integration (Phi-3 + node-llama-cpp)

### Phase 2: Core Features
- [ ] Session continuity engine
- [ ] Consent dialog implementation
- [ ] Obsidian external launch
- [ ] Checksum verification
- [ ] Model downloader

### Phase 3: Cloud Enhancement
- [ ] Claude API bridge
- [ ] Hybrid mode implementation
- [ ] Persistent consent management
- [ ] Model selection (Llama 3.2, Mistral)

### Phase 4: Platform Builds
- [ ] Windows portable executable
- [ ] macOS universal binary
- [ ] Linux AppImage
- [ ] Android APK (Termux-based)

### Phase 5: Advanced Features
- [ ] Vault encryption (VeraCrypt)
- [ ] Cross-device Git sync
- [ ] Custom Obsidian plugin
- [ ] Session pause/resume
- [ ] Blockchain anchoring integration

---

## Use Cases

### Personal Reflection
- Journaling with continuity
- Thought exploration
- Decision-making support
- Learning documentation

### Professional Work
- Project notes with lineage
- Code design reflection
- Meeting summaries
- Research documentation

### Offline/Air-Gapped
- Security-conscious environments
- No-internet locations (travel, remote)
- Privacy-first workflows
- Sovereign personal knowledge management

### Educational
- Student note-taking with AI reflection
- Research journaling
- Thesis development
- Learning documentation

---

## Security & Privacy

### What's Secure
- ✅ All data stored locally on your USB
- ✅ No telemetry or analytics
- ✅ No cloud sync by default
- ✅ Checksum verification for canonical specs
- ✅ Transparent about internet actions

### What's Optional (User Choice)
- 🔐 Vault encryption (VeraCrypt container)
- 🌐 Cloud enhancement (Claude API, requires key)
- 🔄 Cross-device sync (Git-based, user-initiated)

### What's Not (Yet) Implemented
- ⏳ Code signing for executables
- ⏳ Sandboxed runtime permissions
- ⏳ Vault backup automation

---

## FAQ

### Q: Does this require internet?
**A**: No! Core functionality (local LLM reflection, vault operations) works 100% offline. Internet is only used for optional cloud enhancements (Claude API, model downloads, software updates) and requires your explicit consent.

### Q: What's the difference between this and just using ChatGPT?
**A**: MirrorDNA Portable is:
- **Sovereign**: Your data never leaves your device (unless you choose)
- **Continuous**: Sessions maintain lineage and state across time
- **Portable**: Runs from USB, works offline
- **Governed**: Follows canonical protocol (AHP, GlyphSig, etc.)
- **Transparent**: No black box, no hidden telemetry

### Q: Can I use my existing Obsidian vault?
**A**: Yes! You can point MirrorDNA to an existing vault. The launcher will add the necessary `state/` and `templates/` directories without disrupting your existing notes.

### Q: Which LLM is best for my use case?
**A**:
- **Phi-3 Mini** (bundled) - Best balance of quality and speed for reflection
- **Llama 3.2 3B** (optional) - Alternative, similar quality
- **Mistral 7B** (optional) - Higher quality, requires more RAM

### Q: Can I use this on my phone?
**A**: Android support is planned via Termux or native app. iOS is not planned due to Apple's restrictions on local code execution.

### Q: How do I update MirrorDNA?
**A**: Updates are consent-based. The launcher will check for updates (with permission) and offer to download and install. You can also manually replace the launcher executable.

### Q: What if I lose my USB?
**A**: Your vault is just a folder of markdown files. Regular backups (to another USB, cloud, or local drive) are recommended. Git-based sync can help maintain redundancy.

---

## License

MirrorDNA Standard is governed by the license in the repository root.

Portable components (launcher, scripts) follow the same license.

See `../LICENSE.md` for details.

---

## Support & Community

- **Documentation**: See `docs/` directory
- **Issues**: GitHub Issues in main repo
- **Discussions**: GitHub Discussions
- **Security**: See `../SECURITY.md`

---

## Acknowledgments

MirrorDNA Portable builds on:
- **Electron** - Cross-platform desktop framework
- **node-llama-cpp** - Node.js bindings for llama.cpp (efficient local LLM inference)
- **Obsidian** - Powerful markdown-based knowledge management
- **Phi-3 Mini** (Microsoft) - Compact, capable language model

---

⟡ **This is yours.**

Your vault, your data, your choice. Ready when you are.

---

**MirrorDNA Portable**
*Constitutive Reflection · Tri-Twin Architecture · Trust by Design*
