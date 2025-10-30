# MirrorDNA Portable Launcher

Electron-based desktop application for portable, sovereign reflective AI.

## Status: ✅ Functional Prototype with LLM Integration

Complete launcher with local AI integration. Ready for testing with downloaded Phi-3 model.

---

## What's Implemented ✅

### Core Architecture
- ✅ Electron app shell (main process + renderer)
- ✅ Secure IPC bridge (context isolation)
- ✅ Cross-platform window management
- ✅ Persistent settings (electron-store)

### User Interface
- ✅ Custom title bar with glyph branding
- ✅ Status indicator (offline/hybrid/online modes)
- ✅ Onboarding flow (dual-path: new user vs existing)
- ✅ Setup screen (vault creation, internet mode selection)
- ✅ Session screen (chat-like interface)
- ✅ Settings panel (overlay)
- ✅ Whisper-style design system

### Vault Integration
- ✅ Vault initialization (copy template to user location)
- ✅ State persistence (`state/current.json`)
- ✅ Session writing (markdown files with front matter)
- ✅ Template variable replacement
- ✅ Session numbering and lineage tracking

### Visual Language
- ✅ MirrorDNA sigil (hexagon + triangle + center point)
- ✅ Status icons (offline, hybrid, online with distinct colors)
- ✅ Glyph-based status communication

### LLM Integration ✅
- ✅ llama.cpp runtime integration (node-llama-cpp)
- ✅ Phi-3 Mini model loading (GGUF format)
- ✅ Context injection (Master Citation + session state)
- ✅ Master Citation system prompt injection
- ✅ Session state continuity
- ✅ Graceful fallback (placeholder mode when model not present)

---

## What's Pending ⏳

### Streaming Support
- ⏳ Real-time token streaming for responses
- ⏳ Progress indicator during generation

### Cloud Enhancement
- ⏳ Claude API bridge
- ⏳ Consent dialog UI (currently auto-grants in hybrid mode)
- ⏳ Persistent consent tracking
- ⏳ Model downloader (Llama 3.2, Mistral)

### Advanced Features
- ⏳ Obsidian integration (launch external app, URI protocol)
- ⏳ Checksum verification on vault load
- ⏳ Session pause/resume
- ⏳ Cross-device sync (Git-based)
- ⏳ Vault encryption (VeraCrypt container support)

### Platform Builds
- ⏳ Windows `.exe` installer
- ⏳ macOS `.dmg` bundle (Intel + Apple Silicon)
- ⏳ Linux AppImage
- ⏳ Android APK (via Termux or native)

---

## Quick Start (Development)

### Prerequisites
- Node.js 18+ and npm
- Git

### Install Dependencies
```bash
cd portable/launcher
npm install
```

### Run in Development Mode
```bash
npm run dev
```

This launches the app with:
- DevTools enabled
- Live reload on file changes
- Console logging

### Build for Production
```bash
# All platforms (current OS only)
npm run build

# Specific platform
npm run build:win    # Windows
npm run build:mac    # macOS
npm run build:linux  # Linux
```

Built files appear in `dist/` directory.

---

## Local AI Model Setup

### Download Phi-3 Mini (Required for AI functionality)

**Without a model, the launcher runs in placeholder mode with instructions.**

#### Quick Download (Recommended)

1. **Visit**: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
2. **Download**: `Phi-3-mini-4k-instruct-q4.gguf` (~2.4GB)
3. **Rename** to: `phi3-mini-4k.Q4_K_M.gguf`
4. **Place** in: `portable/launcher/models/`

#### Command Line Download

```bash
cd portable/launcher/models

# Using wget
wget https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf -O phi3-mini-4k.Q4_K_M.gguf

# Or using curl
curl -L https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf -o phi3-mini-4k.Q4_K_M.gguf
```

#### Verify Download

```bash
# Check file exists and size (~2.3-2.4GB)
ls -lh portable/launcher/models/phi3-mini-4k.Q4_K_M.gguf
```

### First Run with Model

1. Ensure model is in `models/` directory
2. Run `npm run dev`
3. Complete onboarding (create vault)
4. Wait 30-60 seconds for model to load
5. Start reflecting with local AI!

**Model loads automatically** when you reach the session screen.

---

## Project Structure

```
launcher/
├── package.json           # Dependencies and build config
├── src/
│   ├── main.js           # Electron main process (Node.js)
│   ├── preload.js        # IPC bridge (secure context)
│   └── ui/
│       ├── index.html    # Main UI structure
│       ├── styles.css    # Whisper-style design system
│       └── app.js        # UI controller logic
├── models/               # Local LLM models (user downloads)
│   └── .gitkeep
└── README.md            # This file
```

---

## Architecture Decisions

### Why Electron?
- **Cross-platform**: Single codebase for Windows/Mac/Linux
- **Web tech UI**: HTML/CSS/JS for rapid prototyping
- **File system access**: Native Node.js APIs for vault operations
- **Mature ecosystem**: Well-documented, large community

**Trade-off**: Larger bundle size (~150-200MB) vs Tauri (~50MB)

**Future consideration**: Migrate to Tauri for smaller footprint

### Why llama.cpp?
- **CPU-only**: No GPU required, works on any machine
- **Quantized models**: Smaller, faster (GGUF format)
- **Active development**: Regular updates, optimization improvements
- **Cross-platform**: Works on x86, ARM, macOS Metal

### Why Electron-Store?
- **Simple API**: JSON-based settings persistence
- **Cross-platform**: Handles OS-specific paths automatically
- **Atomic writes**: Safe for concurrent access

---

## UI Design Philosophy

### Whisper, Don't Shout
- Minimalist color palette (dark theme)
- Subtle visual feedback
- Clear hierarchy (title bar → content → input)
- Glyphs as functional communication (not decoration)

### Always Informative
- Status indicator always visible
- Current vault displayed in title bar
- No hidden states or modes

### User Control
- Clickable status for quick mode switch
- Settings accessible from any screen
- Explicit consent for internet actions

### Semantic Color
- **Green** (⟡): Self-contained, offline, secure
- **Gold** (⟡◌): Choice available, hybrid mode
- **Blue** (⟡⟐): Connected, cloud features active

---

## Key Files

### `src/main.js`
Electron main process - handles:
- Window creation and management
- IPC handler registration
- Settings persistence
- Vault file operations

**IPC Handlers:**
- `get-settings` - Load user preferences
- `update-settings` - Save user preferences
- `init-vault` - Create vault from template
- `read-vault-state` - Load `state/current.json`
- `write-session` - Create new session markdown file
- `request-internet` - Consent manager (placeholder)

### `src/preload.js`
Secure IPC bridge - exposes:
- `window.mirrorDNA.*` API to renderer
- Context isolation (no direct Node.js access from UI)

### `src/ui/index.html`
UI structure:
- Custom title bar (draggable, branded)
- Three main screens (onboarding, setup, session)
- Settings panel (overlay)

### `src/ui/styles.css`
Design system:
- CSS variables for theme colors
- Responsive layouts
- Smooth transitions
- Custom scrollbar styling

### `src/ui/app.js`
UI controller:
- Screen navigation
- Form handling
- Message display
- Settings management

---

## Development Workflow

### Adding a New IPC Handler

**1. Register handler in `main.js`:**
```javascript
ipcMain.handle('my-new-action', async (event, arg1, arg2) => {
  // Your logic here
  return { success: true, data: 'result' };
});
```

**2. Expose in `preload.js`:**
```javascript
contextBridge.exposeInMainWorld('mirrorDNA', {
  myNewAction: (arg1, arg2) => ipcRenderer.invoke('my-new-action', arg1, arg2)
});
```

**3. Call from UI (`app.js`):**
```javascript
const result = await window.mirrorDNA.myNewAction(arg1, arg2);
```

### Adding a New Screen

**1. Add HTML in `index.html`:**
```html
<div id="my-screen" class="screen hidden">
  <!-- Your content -->
</div>
```

**2. Style in `styles.css`:**
```css
#my-screen {
  /* Your styles */
}
```

**3. Navigate in `app.js`:**
```javascript
this.showScreen('my'); // Shows #my-screen
```

---

## Next Implementation Steps

### Priority 1: LLM Integration
1. Install `node-llama-cpp` package
2. Download Phi-3 Mini GGUF model
3. Create `src/llm-bridge.js`:
   ```javascript
   class LLMBridge {
     async init(modelPath) { /* Load model */ }
     async generate(prompt, context) { /* Run inference */ }
   }
   ```
4. Wire up in `main.js`:
   ```javascript
   ipcMain.handle('generate-reflection', async (event, prompt) => {
     return await llmBridge.generate(prompt, vaultContext);
   });
   ```
5. Replace placeholder in `app.js` `generateReflection()` method

### Priority 2: Consent Dialog
1. Create modal UI component in `index.html`
2. Add handler in `main.js` to show system dialog
3. Track granted permissions in settings
4. Implement "Yes, always" persistence

### Priority 3: Obsidian Integration
1. Detect Obsidian installation
2. Launch Obsidian with vault path:
   ```javascript
   const { exec } = require('child_process');
   exec(`open obsidian://vault/${vaultName}`);
   ```
3. Add "Open in Obsidian" button to UI

---

## Testing

### Manual Testing Checklist
- [ ] App launches successfully
- [ ] Onboarding flow completes
- [ ] Vault is created in chosen location
- [ ] Settings persist across restarts
- [ ] Session messages display correctly
- [ ] Session files written to `vault/sessions/`
- [ ] State JSON updates after session
- [ ] Status indicator changes with internet mode
- [ ] Settings panel opens/closes

### Automated Testing (TODO)
- Unit tests for vault operations
- Integration tests for IPC handlers
- UI tests with Spectron

---

## Troubleshooting

### App Won't Launch
- Check Node.js version: `node --version` (should be 18+)
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check Electron logs: `npm run dev` and view DevTools console

### Vault Creation Fails
- Ensure target directory exists and is writable
- Check for file permission errors in DevTools
- Verify vault template exists at `../vault-template/`

### Settings Not Persisting
- Check electron-store data location:
  - Windows: `%APPDATA%/mirrordna-portable`
  - macOS: `~/Library/Application Support/mirrordna-portable`
  - Linux: `~/.config/mirrordna-portable`
- Delete config file to reset: `config.json`

---

## Performance Notes

### Memory Usage
- **Idle**: ~200MB (Electron runtime)
- **Active (no LLM)**: ~250MB
- **With LLM loaded**: ~1.5-2GB (Phi-3 Mini in RAM)

### Launch Time
- **Cold start**: 2-4 seconds
- **Warm start**: 1-2 seconds

### Build Size
- **Uncompressed**: ~200MB (includes Electron runtime)
- **Compressed installer**: ~80MB

---

## Contributing

See main repo `CONTRIBUTING.md` for guidelines.

**Launcher-specific notes:**
- Use `npm run dev` for testing
- Follow existing code style (2-space indent, semicolons)
- Update this README when adding features
- Add IPC handlers to both `main.js` and `preload.js`

---

## License

See `../../LICENSE.md` in repo root.

---

⟡ MirrorDNA Portable — Sovereignty through portability
