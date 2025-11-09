#!/bin/bash
# MirrorDNA Portable - Build Script
# Builds for all platforms or specific platform

set -e

echo "⟡ MirrorDNA Portable Builder"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed${NC}"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    npm install
    echo ""
fi

# Get platform argument
PLATFORM=${1:-"all"}

case $PLATFORM in
    "win"|"windows")
        echo -e "${GREEN}Building for Windows...${NC}"
        npm run build:win
        echo -e "${GREEN}✓ Windows build complete${NC}"
        echo -e "  Output: dist/MirrorDNA Portable-*.exe"
        ;;

    "mac"|"macos"|"darwin")
        echo -e "${GREEN}Building for macOS (Universal)...${NC}"
        npm run build:mac:universal
        echo -e "${GREEN}✓ macOS build complete${NC}"
        echo -e "  Output: dist/MirrorDNA Portable-*.dmg"
        ;;

    "linux")
        echo -e "${GREEN}Building for Linux (AppImage + deb)...${NC}"
        npm run build:linux
        npm run build:linux:deb
        echo -e "${GREEN}✓ Linux build complete${NC}"
        echo -e "  Output: dist/MirrorDNA Portable-*.AppImage"
        echo -e "  Output: dist/MirrorDNA Portable-*.deb"
        ;;

    "all")
        echo -e "${GREEN}Building for all platforms...${NC}"
        echo ""

        echo -e "${YELLOW}1/3: Windows${NC}"
        npm run build:win
        echo ""

        echo -e "${YELLOW}2/3: macOS${NC}"
        npm run build:mac:universal
        echo ""

        echo -e "${YELLOW}3/3: Linux${NC}"
        npm run build:linux
        npm run build:linux:deb
        echo ""

        echo -e "${GREEN}✓ All builds complete${NC}"
        ;;

    "pack")
        echo -e "${GREEN}Creating unpacked build (development)...${NC}"
        npm run pack
        echo -e "${GREEN}✓ Unpacked build complete${NC}"
        echo -e "  Output: dist/[platform]-unpacked/"
        ;;

    *)
        echo -e "${RED}Unknown platform: $PLATFORM${NC}"
        echo ""
        echo "Usage: ./build.sh [platform]"
        echo ""
        echo "Platforms:"
        echo "  win     - Build Windows portable executable"
        echo "  mac     - Build macOS universal DMG"
        echo "  linux   - Build Linux AppImage + deb"
        echo "  all     - Build for all platforms (default)"
        echo "  pack    - Create unpacked development build"
        exit 1
        ;;
esac

echo ""
echo "⟡ Build artifacts available in: ./dist/"
echo ""
