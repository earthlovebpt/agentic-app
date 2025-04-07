#!/bin/bash

# Create target folder if it doesn't exist
TARGET_DIR="data/coffee-shop-sample-data"
ZIP_PATH="$TARGET_DIR.zip"

mkdir -p "$TARGET_DIR"

# Download dataset
echo "📥 Downloading Coffee Shop Sample Data..."
curl -L -o "$ZIP_PATH" \
  https://www.kaggle.com/api/v1/datasets/download/ylchang/coffee-shop-sample-data-1113

# Check if download was successful
if [ $? -eq 0 ]; then
    echo "✅ Download complete: $ZIP_PATH"
else
    echo "❌ Download failed."
    exit 1
fi

# Unzip into target folder
echo "📂 Unzipping into $TARGET_DIR..."
unzip -o "$ZIP_PATH" -d "$TARGET_DIR"

# Remove zip file
echo "🧹 Removing zip file..."
rm "$ZIP_PATH"

echo "✅ Done! Dataset is ready in $TARGET_DIR"
