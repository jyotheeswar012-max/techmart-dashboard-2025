# How to Upload the Real Screenshots

The README image paths point to this folder. Run the commands below from your local clone to replace the placeholder files with the real screenshots.

```bash
git clone https://github.com/jyotheeswar012-max/techmart-dashboard-2025.git
cd techmart-dashboard-2025
git pull

# Copy your screenshots into docs/screenshots/ with these exact names:
cp ~/Downloads/Screenshot-2026-06-10-at-6.21.25-PM.jpg  docs/screenshots/01-overview-hero.jpg
cp ~/Downloads/Screenshot-2026-06-10-at-6.21.17-PM.jpg  docs/screenshots/02-overview-bottom.jpg
cp ~/Downloads/Screenshot-2026-06-10-at-6.23.13-PM-3.jpg docs/screenshots/03-products-categories.jpg
cp ~/Downloads/Screenshot-2026-06-10-at-6.23.22-PM-3.jpg docs/screenshots/04-discount-treemap.jpg
cp ~/Downloads/Screenshot-2026-06-10-at-6.23.35-PM-4.jpg docs/screenshots/05-customers.jpg
cp ~/Downloads/Screenshot-2026-06-10-at-6.23.42-PM-5.jpg docs/screenshots/06-operations.jpg
cp ~/Downloads/Screenshot-2026-06-10-at-6.23.53-PM-6.jpg docs/screenshots/07-scenario-engine.jpg
cp ~/Downloads/Screenshot-2026-06-10-at-6.24.06-PM-8.jpg docs/screenshots/08-key-insights.jpg

git add docs/screenshots/
git commit -m "docs: add real dashboard screenshots"
git push origin main
```

After pushing, the README will show all 8 screenshots correctly.
