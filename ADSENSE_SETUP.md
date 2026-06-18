# AdSense Ad Unit Templates
# Replace 'pub-XXXXXXXXXXXXXXXX' with your actual Google AdSense Publisher ID

## How to set up AdSense:

### 1. Get your Publisher ID
- Log in to Google AdSense at https://www.google.com/adsense
- Your Publisher ID is in the format: pub-XXXXXXXXXXXXXXXX

### 2. Update ads.txt
Replace the placeholder in ads.txt with your real Publisher ID:
```
google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
```

### 3. Ad Unit Placement Guide

#### Display Ads (Responsive)
```html
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
```

#### In-Article Ads
```html
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
```

#### Sidebar Ads (300x250 or 300x600)
```html
<ins class="adsbygoogle"
     style="display:inline-block;width:300px;height:250px"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"></ins>
```

## Ad Placement Strategy:

### Homepage
- 1 leaderboard ad (728x90) below hero section
- 1 in-feed ad after first content block
- 1 rectangle ad (300x250) in footer area

### Category Pages (specs pages)
- 1 responsive ad at top of content
- 1 in-article ad after 2nd paragraph
- 1 sidebar ad (if layout supports)

### Product Detail Pages
- 1 ad above spec table
- 1 ad in sidebar
- 1 ad below "Related Products" section

### Troubleshooting/Error Code Pages (High Traffic)
- 1 ad above diagnosis steps
- 1 ad between troubleshooting steps
- 1 ad below conclusion/CTA

### Tools Pages (High Intent)
- 1 ad above calculator/converter
- 1 ad below results

## Important Notes:
- Wait 24-48 hours after adding ad code before expecting ads to show
- Keep ads clearly separated from content with borders or spacing
- Test ads in mobile view as well as desktop
- Use the AdSense auto ads feature for optimal placement
