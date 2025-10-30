# MirrorDNA Portable - LLM Models

This directory contains the local LLM models for offline reflection.

---

## Primary Model: Phi-3 Mini 4K

**Recommended for MirrorDNA Portable**

- **Model**: Phi-3 Mini 4K Instruct
- **Size**: ~2.3GB (quantized Q4_K_M)
- **Context**: 4096 tokens
- **Quality**: Excellent for reflection and reasoning
- **Performance**: Runs on CPU, ~2-10 tokens/sec (depends on hardware)

### Download Instructions

#### Option 1: Hugging Face (Recommended)

1. Visit: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
2. Download file: `Phi-3-mini-4k-instruct-q4.gguf` (~2.4GB)
3. Rename to: `phi3-mini-4k.Q4_K_M.gguf`
4. Place in this directory (`portable/launcher/models/`)

#### Option 2: Direct Download (if available)

```bash
# From this directory
wget https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf -O phi3-mini-4k.Q4_K_M.gguf
```

Or use `curl`:

```bash
curl -L https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf -o phi3-mini-4k.Q4_K_M.gguf
```

#### Option 3: Use llama.cpp model repository

```bash
# Clone llama.cpp models (large repo!)
git clone https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
# Copy the quantized model
cp Phi-3-mini-4k-instruct-gguf/Phi-3-mini-4k-instruct-q4.gguf ./phi3-mini-4k.Q4_K_M.gguf
```

---

## Expected File

After download, you should have:

```
portable/launcher/models/
└── phi3-mini-4k.Q4_K_M.gguf  (~2.3-2.4GB)
```

**Verify the model:**
- File size: ~2.3-2.4GB
- Format: GGUF (quantized)
- SHA256 checksum: (check Hugging Face page for official checksum)

---

## Alternative Models (Optional)

### Llama 3.2 3B

- **Model**: Llama 3.2 3B Instruct
- **Size**: ~2.0GB (Q4_K_M)
- **Download**: https://huggingface.co/lmstudio-community/Llama-3.2-3B-Instruct-GGUF
- **Filename**: `llama-3.2-3b-instruct.Q4_K_M.gguf`

### Mistral 7B (Higher Quality, More Resources)

- **Model**: Mistral 7B Instruct
- **Size**: ~4.1GB (Q4_K_M)
- **Download**: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF
- **Filename**: `mistral-7b-instruct-v0.2.Q4_K_M.gguf`
- **Note**: Requires more RAM (~8GB recommended)

---

## System Requirements

### For Phi-3 Mini (Recommended)
- **RAM**: 4GB available (8GB total recommended)
- **Storage**: 3GB free space
- **CPU**: Any modern x86_64 or ARM64 processor
- **Performance**: 2-10 tokens/sec (CPU-only)

### For Mistral 7B (Optional)
- **RAM**: 6GB available (12GB total recommended)
- **Storage**: 5GB free space
- **CPU**: Modern multi-core processor recommended
- **Performance**: 1-5 tokens/sec (CPU-only)

---

## Integration Notes

The MirrorDNA launcher will automatically detect models in this directory with these exact filenames:

1. `phi3-mini-4k.Q4_K_M.gguf` (primary)
2. `llama-3.2-3b-instruct.Q4_K_M.gguf` (fallback)
3. `mistral-7b-instruct-v0.2.Q4_K_M.gguf` (premium)

If no model is found, the launcher will run in **placeholder mode** with instructions to download a model.

---

## Troubleshooting

### Model not loading

**Error**: "Model not found"
- **Solution**: Verify filename exactly matches: `phi3-mini-4k.Q4_K_M.gguf`
- Check file is in correct directory: `portable/launcher/models/`

**Error**: "Failed to load model"
- **Solution**: Verify file is not corrupted (check file size)
- Re-download if necessary
- Check available RAM (need ~4GB free)

**Error**: "Out of memory"
- **Solution**: Close other applications
- Use smaller model (Phi-3 instead of Mistral)
- Increase system swap space

### Slow performance

- **Normal**: CPU-only inference is slower than GPU
- **Expected**: 2-10 tokens/second on modern CPU
- **Improve**:
  - Close background applications
  - Use quantized model (Q4_K_M is already optimized)
  - Consider dedicated hardware (M-series Mac, modern CPU)

---

## License & Attribution

- **Phi-3**: MIT License (Microsoft)
- **Llama 3.2**: Llama 3 Community License (Meta)
- **Mistral**: Apache 2.0 (Mistral AI)

All models are used under their respective licenses for local, personal use.

---

## Security Note

⟡ **Sovereignty**: Models run 100% locally. No internet connection required for inference.

- Your prompts never leave your device
- No telemetry, no tracking, no data collection
- Complete privacy and control

---

⟡ **Ready for Reflection**

Once you've downloaded a model, restart MirrorDNA Portable to begin reflecting with local AI.
