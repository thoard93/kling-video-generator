# 📲 iOS Shortcut - Exact Steps

## Quick Setup (5 minutes)

### Part 1: Get Your Cloud URL

1. Follow deployment guide to get your Render URL
2. Should look like: `https://kling-video-generator.onrender.com`
3. Copy this URL - you'll need it!

---

## Part 2: Build the iOS Shortcut

Open Shortcuts app and follow these EXACT steps:

### Step 1: Create New Shortcut
- Tap "+" button
- Name it "TikTok Video Generator"

### Step 2: Add Photo Selector
```
🔍 Search: "Select Photos"
➕ Add action
⚙️ Settings:
   - Select Multiple: OFF
   - Include Screenshots: ON
```

### Step 3: Add API Upload
```
🔍 Search: "Get Contents of URL"
➕ Add action
⚙️ Settings:
   - Method: POST
   - URL: https://YOUR-RENDER-URL.onrender.com/generate
   
📋 Tap "Show More":
   - Request Body: File
   - Field Name: image
   - File: (Select Photos result)
```

### Step 4: Show Progress
```
🔍 Search: "Show Notification"
➕ Add action
⚙️ Text: "Generating video... Please wait 5-10 minutes ⏳"
```

### Step 5: Extract Video URL
```
🔍 Search: "Get Dictionary Value"
➕ Add action
⚙️ Settings:
   - Key: video_url
   - Dictionary: (Get Contents of URL result)
```

### Step 6: Build Download URL
```
🔍 Search: "Text"
➕ Add action
⚙️ Content:
   https://YOUR-RENDER-URL.onrender.com[Get Dictionary Value]
   
   (Tap [Get Dictionary Value] to insert the variable)
```

### Step 7: Download Video
```
🔍 Search: "Get Contents of URL"
➕ Add action
⚙️ Settings:
   - Method: GET
   - URL: (Text result from previous step)
```

### Step 8: Save Video
```
🔍 Search: "Save to Photo Album"
➕ Add action
⚙️ Settings:
   - Photos: (Get Contents of URL result)
   - Album: Recent (or create "TikTok Videos")
```

### Step 9: Success Message
```
🔍 Search: "Show Notification"
➕ Add action
⚙️ Text: "✅ Video saved to Photos!"
```

---

## Complete Shortcut Flow

```
┌─────────────────────────┐
│   Select Photos         │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Get Contents of URL   │
│   POST to /generate     │
│   with photo            │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Show Notification     │
│   "Generating..."       │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Get Dictionary Value  │
│   key: video_url        │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Text                  │
│   Combine URL           │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Get Contents of URL   │
│   Download video        │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Save to Photo Album   │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Show Notification     │
│   "✅ Saved!"           │
└─────────────────────────┘
```

---

## 🎨 Bonus: Make It Pretty

### Add Custom Icon
1. Edit shortcut
2. Tap (...)  menu
3. Tap shortcut icon
4. Choose: Glyph = "video.fill", Color = Purple

### Add to Home Screen
1. Edit shortcut
2. Tap (...) menu
3. "Add to Home Screen"
4. Choose icon and name

### Enable Share Sheet
1. Edit shortcut
2. Tap settings (...)
3. Enable "Show in Share Sheet"
4. Enable "Photos" input
5. Now works from Photos app!

---

## 🧪 Testing

### Test 1: API Health Check
1. Open Safari on iPhone
2. Go to: `https://YOUR-RENDER-URL.onrender.com/`
3. Should see: `{"status": "online"}`

### Test 2: Run Shortcut
1. Open Shortcuts
2. Tap your shortcut
3. Select a product photo
4. See "Generating..." notification
5. Wait 5-10 minutes
6. See "✅ Saved!" notification
7. Check Photos app!

---

## 💡 Pro Tips

### Faster Testing
- Test with same photo multiple times
- Second request is much faster (no cold start)

### Best Photos
- Good lighting
- Clear background
- Product centered
- High resolution

### Troubleshooting
- If it fails, check Render logs online
- First use takes 30-60s to wake up
- Make sure all API keys are set

---

## 🎬 Usage Flow

```
1. Take product photo (or choose existing)
2. Run shortcut from:
   - Shortcuts app
   - Home screen icon
   - Share sheet in Photos
3. Wait 5-10 minutes
4. Video automatically saves to Photos
5. Upload to TikTok Shop!
```

---

## ⚡ Quick Reference

**Your URLs:**
- API Base: `https://YOUR-URL.onrender.com`
- Generate: `https://YOUR-URL.onrender.com/generate`
- Health: `https://YOUR-URL.onrender.com/health`

**Actions Count:** 9 total
**Time to Build:** ~5 minutes
**Time to Run:** ~5-10 minutes per video

---

You're all set! Happy video creating! 🚀📱
