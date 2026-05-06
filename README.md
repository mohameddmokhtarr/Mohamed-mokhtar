# Instagram Comment-to-DM Automation Tool

A full-stack web application that automates Instagram comment replies and direct messages based on keywords. Similar to ManyChat, when a user comments a specific keyword on a chosen Instagram post, the tool automatically replies to the comment AND sends the commenter a private DM.

## Features

✅ **Webhook-based Comment Detection** — Real-time comment processing using Facebook Webhook subscriptions  
✅ **Automated Replies & DMs** — Auto-reply to comments + send DMs with different messages  
✅ **Campaign Management** — Create and manage multiple campaigns per post  
✅ **Keyword Triggers** — Case-insensitive, partial-match keyword detection  
✅ **Deduplication** — Tracks processed comments to prevent duplicate actions  
✅ **Dark-mode Dashboard** — Professional, responsive UI with settings & campaign management  
✅ **Cloud-ready** — Dockerfile, Railway.toml, and Render.yaml included  
✅ **No Selenium/instagrapi** — Uses only the official Instagram Graph API  

## Tech Stack

- **Backend:** Python + FastAPI
- **Database:** SQLite (easy migration to PostgreSQL)
- **Frontend:** Vanilla HTML/JS/CSS with Jinja2 templating
- **Async:** httpx for non-blocking API calls
- **ORM:** SQLAlchemy
- **Deployment:** Docker, Railway, Render

## Project Structure

```
├── main.py                  # FastAPI app entry point
├── instagram.py             # Instagram Graph API client
├── models.py                # SQLAlchemy database models
├── database.py              # DB session setup
├── routes/
│   ├── webhook.py          # Webhook endpoints (POST /webhook/instagram)
│   ├── dashboard.py        # Dashboard HTML routes
│   └── api.py              # REST API for campaigns/config
├── static/
│   ├── style.css           # Dashboard styling (dark theme)
│   └── app.js              # Dashboard JavaScript logic
├── templates/
│   └── dashboard.html      # Main dashboard template
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker containerization
├── railway.toml            # Railway.app deployment config
├── render.yaml             # Render.com deployment config
└── README.md               # This file
```

## Installation & Setup

### 1. Clone and Install Dependencies

```bash
git clone <repo-url>
cd instagram-automation-tool
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
INSTAGRAM_ACCESS_TOKEN=your_long_lived_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id
FACEBOOK_APP_SECRET=your_app_secret
WEBHOOK_VERIFY_TOKEN=your_random_webhook_token
DATABASE_URL=sqlite:///./app.db
```

### 3. Run Locally

```bash
python main.py
```

Visit `http://localhost:8000/dashboard` in your browser.

## Instagram API Setup (Step-by-Step)

If you don't have a Facebook Developer App yet, follow these steps:

### Step 1: Convert Your Instagram Account to Business

1. Open the Instagram app
2. Go to **Settings** → **Account**
3. Tap **Switch to Professional Account**
4. Choose **Business** or **Creator** account type
5. Complete the onboarding

### Step 2: Create a Facebook Developer App

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Log in with your Facebook account
3. Click **My Apps** → **Create App**
4. Select **Business** as the app type
5. Fill in your app details and create the app
6. Go to **Settings** → **Basic** and note your **App ID** and **App Secret**

### Step 3: Add Instagram Graph API Product

1. In your app dashboard, click **+ Add Product**
2. Find **Instagram Graph API** and click **Set Up**
3. In **Products** → **Instagram Graph API** → **Settings**, configure:
   - **App Roles:** Add your Facebook account
   - **Instagram Business Account:** Connect your business account

### Step 4: Generate a Long-Lived Access Token

1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer)
2. In the top-left dropdown, select your app
3. Click **Generate Access Token**
4. Select **User Token** mode
5. Select these permissions:
   - `instagram_business_basic`
   - `instagram_manage_comments`
   - `instagram_manage_messages`
6. Click **Generate**
7. Copy the token and paste it in `.env` as `INSTAGRAM_ACCESS_TOKEN`

### Step 5: Get Your Business Account ID

1. In the Graph API Explorer, run this query:
   ```
   me/ig_user_id
   ```
2. The response will contain your **Business Account ID**
3. Copy it to `.env` as `INSTAGRAM_BUSINESS_ACCOUNT_ID`

### Step 6: Find a Post ID

To test or create campaigns, you'll need post IDs:

**Via Instagram URL:**
- Instagram post URL format: `instagram.com/p/{POST_ID}/`
- Example: `instagram.com/p/ABC123XYZ/` → POST_ID = `ABC123XYZ`

**Via Graph API Explorer:**
1. In Graph API Explorer, run:
   ```
   me/ig_user_id/media
   ```
2. Find your post in the response and use its `id`

### Step 7: Configure Webhook (For Real-Time Comments)

To receive real-time comment notifications (optional but recommended):

1. In your app dashboard, go to **Products** → **Instagram Graph API** → **Webhooks**
2. Click **Edit Subscriptions**
3. Set:
   - **Callback URL:** `https://yourdomain.com/webhook/instagram`
   - **Verify Token:** Use the value from `WEBHOOK_VERIFY_TOKEN` in your `.env`
4. Subscribe to these events:
   - `comments`
   - `messages`
5. Click **Save**

## API Reference

### Config Endpoints

**POST /api/config** — Save Instagram credentials
```json
{
  "instagram_access_token": "...",
  "instagram_business_account_id": "...",
  "facebook_page_id": "..."
}
```

**GET /api/config** — Retrieve saved config

### Campaign Endpoints

**POST /api/campaigns** — Create campaign
```json
{
  "post_id": "123456789",
  "keywords": "promo,discount,offer",
  "comment_reply": "Thanks for your interest! Check your DMs for details.",
  "dm_message": "Here's an exclusive offer just for you..."
}
```

**GET /api/campaigns** — List all campaigns

**GET /api/campaigns/{id}** — Get campaign details

**PUT /api/campaigns/{id}** — Update campaign

**DELETE /api/campaigns/{id}** — Delete campaign

**POST /api/campaigns/{id}/toggle** — Toggle active status

### Webhook Endpoint

**GET /webhook/instagram** — Webhook verification (Facebook)

**POST /webhook/instagram** — Receive comment events

## Database Models

### Config
Stores Instagram credentials (access token, business account ID, page ID)

### Campaign
Links a post ID to trigger keywords and associated messages

### ProcessedComment
Tracks comment IDs + timestamps to prevent duplicate processing

## DM Limitation & How to Resolve

**Important:** Instagram DMs via Graph API have restrictions:

- The user must have **previously messaged** your business account, OR
- Your app must have **approved** `instagram_manage_messages` permission

### To Get Approved:

1. In your app dashboard, go to **App Roles** → **Roles**
2. Add your test accounts as **Testers** or **Developers**
3. For production, go to **Settings** → **Basic** and check **App Roles**
4. Request `instagram_manage_messages` permission via the **Permissions** page

**For testing:** Ask your followers to send you a DM first, then they'll receive automated replies.

## Deployment

### Option 1: Railway.app

1. Push your repo to GitHub
2. Go to [railway.app](https://railway.app)
3. Create a new project and connect your GitHub repo
4. Set environment variables in Railway dashboard
5. Deploy

### Option 2: Render.com

1. Go to [render.com](https://render.com) and sign up
2. Create a new **Web Service**
3. Connect your GitHub repo
4. Set **Build Command:** `pip install -r requirements.txt`
5. Set **Start Command:** `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Click **Deploy**

### Option 3: Docker (Local or Cloud)

```bash
docker build -t instagram-automation-tool .

docker run -p 8000:8000 \
  -e INSTAGRAM_ACCESS_TOKEN=xxx \
  -e INSTAGRAM_BUSINESS_ACCOUNT_ID=xxx \
  -e FACEBOOK_APP_SECRET=xxx \
  -e WEBHOOK_VERIFY_TOKEN=xxx \
  instagram-automation-tool
```

## Security Notes

⚠️ **Never commit `.env` to version control**
- Use `.env.example` as a template
- Add `.env` to `.gitignore`

⚠️ **Webhook Signature Verification**
- Every webhook is verified using `X-Hub-Signature-256` header
- The app validates signatures before processing

⚠️ **Access Token Security**
- Never expose tokens in logs or frontend
- Tokens expire after 60 days — regenerate regularly
- Use HTTPS in production

## Troubleshooting

### No comments being received?

1. Check that the webhook URL is publicly accessible
2. Verify `WEBHOOK_VERIFY_TOKEN` matches your Facebook app settings
3. Ensure webhook is subscribed to `comments` field in Facebook app dashboard
4. Check app logs for webhook signature verification errors

### DM not sending?

1. Ensure the user has previously messaged your business account
2. Verify `instagram_manage_messages` permission is approved
3. Check that business account has enough message capacity
4. Look for rate limit errors in logs

### Database connection error?

1. Check `DATABASE_URL` is set correctly
2. For SQLite: ensure write permissions in app directory
3. For PostgreSQL: verify connection string format

## License

MIT

## Support

For issues, questions, or feature requests, please create a GitHub issue.

## Disclaimer

This tool uses the official Instagram Graph API. Ensure your use complies with Instagram's Terms of Service and Community Guidelines. Automated engagement must be genuine and provide value to users.
