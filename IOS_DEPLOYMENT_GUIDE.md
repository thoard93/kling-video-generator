# 📱 iOS Shortcut + Cloud Deployment Guide

Complete guide to deploy your Kling AI video generator to the cloud and use it from your iPhone!

---

## 🎯 What You'll Get

- Take a photo on iPhone (or choose from library)
- Tap "Generate Video"
- Wait 5-10 minutes
- Get professional TikTok video back
- Works from anywhere, no computer needed!

---

## 📋 Step 1: Deploy to Render.com (Free)

### 1.1 Create Render Account

1. Go to https://render.com
2. Sign up for free account (use GitHub, Google, or email)
3. Verify your email

### 1.2 Create New Web Service

1. Click "New +" → "Web Service"
2. Choose "Deploy from GitHub" (easier) or "Public Git repository"

### 1.3 If Using GitHub (Recommended):

1. Create a new GitHub repository
2. Upload these files to it:
   - `app.py`
   - `requirements_cloud.txt` (rename to `requirements.txt`)
   - `Procfile`
3. Connect your GitHub account to Render
4. Select the repository

### 1.4 If Using Public Git:

Just point to a public URL where you've uploaded the files

### 1.5 Configure the Web Service

**Build & Deploy Settings:**
- **Name:** `kling-video-generator` (or any name)
- **Region:** Choose closest to you
- **Branch:** `main` or `master`
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Plan:** Free

### 1.6 Add Environment Variables

Click "Advanced" → "Environment Variables" and add:

```
KLING_ACCESS_KEY = your-kling-access-key
KLING_SECRET_KEY = your-kling-secret-key
ANTHROPIC_API_KEY = sk-ant-your-anthropic-key
```

### 1.7 Deploy!

1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. You'll get a URL like: `https://kling-video-generator.onrender.com`

**Save this URL - you'll need it for the iOS Shortcut!**

---

## 📱 Step 2: Create iOS Shortcut

### 2.1 Open Shortcuts App on iPhone

### 2.2 Create New Shortcut

1. Tap "+" to create new shortcut
2. Name it "Generate TikTok Video"

### 2.3 Add These Actions

**Action 1: Select Photo**
- Search for "Select Photos"
- Add it
- Configure: "Select Multiple" = OFF

**Action 2: Get Contents of Photo**
- Search for "Get Contents of URL"
- Set Method: POST
- Set URL: `https://your-render-url.onrender.com/generate`
  (Replace with YOUR Render URL from Step 1.7)

**Action 3: Set Request Body**
- Tap "Show More" on the Get Contents action
- Set Request Body: File
- Field Name: `image`
- File: (select the photo from previous action)

**Action 4: Get Video URL**
- Search for "Get Dictionary Value"
- Key: `video_url`
- Dictionary: (result from previous action)

**Action 5: Download Video**
- Search for "Get Contents of URL"
- URL: Combine your Render URL + the video_url from previous step
  Example: `https://your-render-url.onrender.com` + (Get Dictionary Value result)

**Action 6: Save Video**
- Search for "Save to Photo Album"
- Input: (result from previous Get Contents)

**Action 7: Show Notification**
- Search for "Show Notification"
- Text: "Video generated and saved to Photos!"

### 2.4 Shortcut Flow Summary

```
1. Select Photos
2. Get Contents of URL (POST to /generate with photo)
3. Get Dictionary Value (extract video_url)
4. Get Contents of URL (download video)
5. Save to Photo Album
6. Show Notification
```

---

## 🧪 Step 3: Test It!

### 3.1 Test the API First

Open Safari on your iPhone and visit:
```
https://your-render-url.onrender.com/
```

You should see:
```json
{
  "status": "online",
  "service": "Kling AI Video Generator",
  "version": "1.0"
}
```

If you see this, your API is working! ✅

### 3.2 Run the Shortcut

1. Open Shortcuts app
2. Tap your "Generate TikTok Video" shortcut
3. Select a product photo
4. Wait 5-10 minutes (you'll see progress)
5. Video saves to Photos automatically!

---

## 🎨 Make It Better (Optional)

### Add to Home Screen

1. In Shortcuts app, tap your shortcut
2. Tap (...) menu → "Add to Home Screen"
3. Choose an icon and name
4. Now you can generate videos directly from home screen!

### Add to Share Sheet

1. Edit your shortcut
2. Tap settings icon (...)
3. Enable "Show in Share Sheet"
4. Enable "Photos" as input
5. Now you can share any photo → "Generate TikTok Video"

### Add Loading Message

Between "Get Contents of URL" (upload) and the download:
- Add "Show Notification"
- Text: "Generating video... This takes 5-10 minutes"

---

## ⚡ Usage Tips

### First Use (Cold Start)

Render's free tier "sleeps" after inactivity. First request might take 30-60 seconds to wake up. Subsequent requests are fast.

### Processing Time

- Analysis: 2-3 seconds
- Video generation: 3-8 minutes (Kling AI)
- Download: 10-30 seconds
- **Total: 5-10 minutes**

### Best Practices

1. **Use good lighting** - Better product photos = better videos
2. **Clear background** - Helps Claude analyze the product
3. **Center the product** - Optimal framing
4. **Be patient** - Video generation takes time!

---

## 🔧 Troubleshooting

### "Could not connect to server"

- Check your Render URL is correct
- Make sure service is deployed (check Render dashboard)
- Try accessing the URL in Safari first

### "Error 500"

- Check Render logs (Render dashboard → Logs)
- Verify all 3 API keys are set correctly
- Check if you have credits in Kling AI and Anthropic

### "Rate limit" errors

- Wait 10-15 minutes
- Check Kling AI usage dashboard
- Make sure you have credits

### Video takes too long

- First generation after inactivity takes longer (cold start)
- Kling AI processing is 3-8 minutes normally
- Check Render logs to see progress

---

## 💰 Cost Breakdown

### Free Tier Limits

**Render.com Free:**
- 750 hours/month (enough for occasional use)
- Sleeps after 15 min inactivity
- Perfect for this use case!

**Kling AI:**
- Depends on your plan
- ~$0.10-0.50 per video

**Anthropic:**
- ~$0.01-0.03 per image analysis
- Add $5 minimum credits

**Total per video: ~$0.11-0.53**

### Upgrade Options

If you use it a lot:
- **Render Starter:** $7/mo - No sleeping, better performance
- **Kling AI Pro:** Better quotas
- **Anthropic Pro:** Higher rate limits

---

## 📊 Advanced: View Generation Status

Want to see real-time progress? Add this to your shortcut after uploading:

1. Add "Get Dictionary Value" action
2. Key: `message`
3. Add "Show Notification"
4. Text: (result from Get Dictionary Value)

This shows status messages as it processes!

---

## 🎉 You're Done!

You now have:
- ✅ Cloud-based video generator
- ✅ iOS Shortcut to use it
- ✅ Works from anywhere
- ✅ No computer needed!

Take a product photo, run the shortcut, and get your TikTok video! 🚀📱

---

## 🆘 Need Help?

**Check Render Logs:**
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. See what's happening in real-time

**Common Issues:**
- API keys not set → Check environment variables
- Service sleeping → First request wakes it up (30-60s)
- Rate limits → Wait and try again
- Out of credits → Add credits to Kling AI/Anthropic

---

Enjoy your automated TikTok shop video creator! 🎬✨
