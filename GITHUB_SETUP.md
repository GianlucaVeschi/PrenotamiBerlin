# GitHub Setup Instructions

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Fill in the details:
   - **Repository name:** `PrenotamiBerlin` or `prenotami-embassy-bot`
   - **Description:** "Automated bot for booking Italian embassy appointments in Berlin"
   - **Visibility:** Public ✅
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

## Step 2: Push to GitHub

After creating the repository, GitHub will show you commands. Use these instead:

```bash
cd /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/PrenotamiBerlin.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Quick Commands (Copy-Paste)

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
cd /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin
git remote add origin https://github.com/YOUR_USERNAME/PrenotamiBerlin.git
git push -u origin main
```

## ⚠️ Important: Protected Files

Your `.gitignore` is configured to protect:
- ✅ `.env` - Your credentials (NEVER committed)
- ✅ `*.log` - Logs that may contain sensitive info
- ✅ `*.png` - Screenshots that may show personal data
- ✅ `venv/` - Virtual environment

These will NOT be pushed to GitHub! ✅

## Step 3: Verify on GitHub

After pushing, visit:
`https://github.com/YOUR_USERNAME/PrenotamiBerlin`

You should see:
- ✅ README.md displayed on the homepage
- ✅ All Python files
- ✅ Documentation files
- ❌ NO .env file
- ❌ NO screenshots
- ❌ NO logs

## Optional: Add Topics

On GitHub, add topics to make your repo discoverable:
- `automation`
- `selenium`
- `python`
- `bot`
- `embassy`
- `appointment-booking`
- `prenotami`
- `italian-embassy`

## Optional: Add License

Consider adding a license (MIT is popular for open-source):

```bash
# Create LICENSE file
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "Add MIT License"
git push
```

## Future Updates

When you make changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

## 🎉 Done!

Your bot is now publicly available on GitHub for others to use!

## Sharing Your Repository

Once published, share the link:
- `https://github.com/YOUR_USERNAME/PrenotamiBerlin`

Others can clone it with:
```bash
git clone https://github.com/YOUR_USERNAME/PrenotamiBerlin.git
```

## ⚠️ Security Reminder

- **NEVER** commit your `.env` file
- **NEVER** push logs or screenshots
- The `.gitignore` protects you, but always double-check!

---

**Need help?** Check if files are being ignored:
```bash
git status --ignored
```

