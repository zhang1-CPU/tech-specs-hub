#!/bin/bash

PRODUCT_PAGES=(
  "pages/specs/ecoflow-delta-pro-3.html"
  "pages/specs/bluetti-ac200max.html"
  "pages/specs/dji-mini-5-pro.html"
  "pages/specs/jackery-explorer-2000-plus.html"
)

COLLECTION_PAGES=(
  "pages/specs/outdoor-power.html"
  "pages/specs/smart-home.html"
  "pages/specs/drones.html"
  "pages/specs/hybrid-cars.html"
  "pages/specs/ebike-micromobility.html"
  "pages/specs/3d-printers.html"
  "pages/specs/navigation.html"
)

ARTICLE_PAGES=(
  "pages/specs/budget-500w-power-station-comparison.html"
  "pages/specs/off-grid-solar-system-sizing-guide.html"
  "pages/tools/best-multimeters-2026.html"
)

for page in "${PRODUCT_PAGES[@]}"; do
  if [ -f "$page" ]; then
    sed -i 's/"@type": "WebSite"/"@type": "Product"/g' "$page"
    sed -i 's/<meta property="og:type" content="WebSite">/<meta property="og:type" content="product">/g' "$page"
    echo "Fixed Product: $page"
  fi
done

for page in "${COLLECTION_PAGES[@]}"; do
  if [ -f "$page" ]; then
    sed -i 's/"@type": "WebSite"/"@type": "CollectionPage"/g' "$page"
    sed -i 's/<meta property="og:type" content="WebSite">/<meta property="og:type" content="website">/g' "$page"
    echo "Fixed Collection: $page"
  fi
done

for page in "${ARTICLE_PAGES[@]}"; do
  if [ -f "$page" ]; then
    sed -i 's/"@type": "WebSite"/"@type": "TechArticle"/g' "$page"
    sed -i 's/<meta property="og:type" content="WebSite">/<meta property="og:type" content="article">/g' "$page"
    echo "Fixed Article: $page"
  fi
done

echo "Done!"
