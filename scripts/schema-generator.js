/**
 * Schema Generator for TechSpecs Hub
 * 
 * This script automatically generates JSON-LD structured data for all HTML pages
 * in the /pages/specs/ and /pages/troubleshooting/ directories.
 * 
 * Usage: node schema-generator.js
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  baseUrl: 'https://powerspecshub.com',
  pagesDir: path.join(__dirname, '..', 'pages'),
  specsDir: path.join(__dirname, '..', 'pages', 'specs'),
  troubleshootingDir: path.join(__dirname, '..', 'pages', 'troubleshooting'),
};

/**
 * Extract data from HTML content
 */
function extractDataFromHTML(htmlContent, filePath) {
  const data = {
    title: '',
    description: '',
    type: 'TechArticle',
    datePublished: '2026-05-14',
    dateModified: '2026-05-14',
  };

  // Extract title
  const titleMatch = htmlContent.match(/<title>(.*?)<\/title>/);
  if (titleMatch) {
    data.title = titleMatch[1].replace(' - TechSpecs Hub', '');
  }

  // Extract description
  const descMatch = htmlContent.match(/<meta name="description" content="(.*?)">/);
  if (descMatch) {
    data.description = descMatch[1];
  }

  // Determine page type from path
  if (filePath.includes('/specs/')) {
    data.type = 'TechArticle';
    data.mainEntity = extractProductData(htmlContent);
  } else if (filePath.includes('/troubleshooting/')) {
    data.type = 'TechArticle';
    data.about = extractTroubleshootingData(htmlContent);
  }

  // Extract table data for structured data
  data.hasPart = extractTableData(htmlContent);

  return data;
}

/**
 * Extract product data from specs pages
 */
function extractProductData(htmlContent) {
  const productData = {
    '@type': 'Product',
    name: '',
    brand: { '@type': 'Brand', name: '' }
  };

  // Try to extract product name from title
  const titleMatch = htmlContent.match(/<title>(.*?)<\/title>/);
  if (titleMatch) {
    const title = titleMatch[1];
    // Extract model name from title (e.g., "Toyota Prius 2022" from "Toyota Prius 2022 Battery Specs")
    const modelMatch = title.match(/^(.*?)\s+(Battery|Specs|Parameters)/);
    if (modelMatch) {
      productData.name = modelMatch[1];
    }
  }

  // Try to extract brand
  const brandMatch = htmlContent.match(/(Toyota|Honda|Ford|Chevrolet|Tesla|BMW|Mercedes|Audi|Nissan|Hyundai|Kia|Lexus)/i);
  if (brandMatch) {
    productData.brand.name = brandMatch[1];
  }

  return productData;
}

/**
 * Extract troubleshooting data
 */
function extractTroubleshootingData(htmlContent) {
  const data = {
    '@type': 'Thing',
    name: ''
  };

  // Extract error code from title or content
  const codeMatch = htmlContent.match(/(P0A80|P0A7F|E\d{2,4})/);
  if (codeMatch) {
    data.name = codeMatch[1] + ' Diagnostic Trouble Code';
  }

  return data;
}

/**
 * Extract table data from HTML
 */
function extractTableData(htmlContent) {
  const tables = [];
  const tableRegex = /<table[^>]*>([\s\S]*?)<\/table>/g;
  let match;

  while ((match = tableRegex.exec(htmlContent)) !== null) {
    const tableHTML = match[1];
    const rows = [];
    
    // Extract rows
    const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/g;
    let rowMatch;
    
    while ((rowMatch = rowRegex.exec(tableHTML)) !== null) {
      const cells = [];
      const cellRegex = /<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/g;
      let cellMatch;
      
      while ((cellMatch = cellRegex.exec(rowMatch[1])) !== null) {
        // Strip HTML tags
        const cellText = cellMatch[1].replace(/<[^>]+>/g, '').trim();
        cells.push(cellText);
      }
      
      if (cells.length > 0) {
        rows.push(cells);
      }
    }

    if (rows.length > 0) {
      tables.push({
        '@type': 'Table',
        about: 'Technical Specifications',
        tableBody: rows
      });
    }
  }

  return tables;
}

/**
 * Generate JSON-LD schema
 */
function generateSchema(data, url) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': data.type,
    headline: data.title,
    description: data.description,
    url: url,
    datePublished: data.datePublished,
    dateModified: data.dateModified,
    author: {
      '@type': 'Organization',
      name: 'TechSpecs Hub',
      url: CONFIG.baseUrl
    },
    publisher: {
      '@type': 'Organization',
      name: 'TechSpecs Hub',
      logo: {
        '@type': 'ImageObject',
        url: `${CONFIG.baseUrl}/assets/images/logo.png`
      }
    }
  };

  if (data.mainEntity) {
    schema.mainEntity = data.mainEntity;
  }

  if (data.about) {
    schema.about = data.about;
  }

  if (data.hasPart && data.hasPart.length > 0) {
    schema.hasPart = data.hasPart;
  }

  return schema;
}

/**
 * Process a single HTML file
 */
function processHTMLFile(filePath) {
  try {
    const htmlContent = fs.readFileSync(filePath, 'utf-8');
    const relativePath = path.relative(CONFIG.pagesDir, filePath);
    const url = `${CONFIG.baseUrl}/${relativePath.replace('.html', '')}`;
    
    const data = extractDataFromHTML(htmlContent, filePath);
    const schema = generateSchema(data, url);
    
    // Check if schema already exists
    const existingSchemaMatch = htmlContent.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
    
    let newHTML;
    const schemaScript = `<script type="application/ld+json">\n${JSON.stringify(schema, null, 2)}\n</script>`;
    
    if (existingSchemaMatch) {
      // Replace existing schema
      newHTML = htmlContent.replace(
        /<script type="application\/ld\+json">[\s\S]*?<\/script>/,
        schemaScript
      );
    } else {
      // Insert before </head>
      newHTML = htmlContent.replace(
        '</head>',
        `    ${schemaScript}\n</head>`
      );
    }
    
    // Write back
    fs.writeFileSync(filePath, newHTML, 'utf-8');
    
    console.log(`✓ Processed: ${relativePath}`);
    return true;
  } catch (error) {
    console.error(`✗ Error processing ${filePath}:`, error.message);
    return false;
  }
}

/**
 * Process all HTML files in a directory
 */
function processDirectory(dirPath) {
  if (!fs.existsSync(dirPath)) {
    console.log(`Directory does not exist: ${dirPath}`);
    return;
  }

  const files = fs.readdirSync(dirPath);
  
  files.forEach(file => {
    const filePath = path.join(dirPath, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      processDirectory(filePath);
    } else if (file.endsWith('.html')) {
      processHTMLFile(filePath);
    }
  });
}

/**
 * Generate sitemap for a directory
 */
function generateSitemap(dirPath, sitemapName) {
  const urls = [];
  
  function scanDirectory(currentPath, basePath) {
    if (!fs.existsSync(currentPath)) return;
    
    const files = fs.readdirSync(currentPath);
    
    files.forEach(file => {
      const filePath = path.join(currentPath, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory()) {
        scanDirectory(filePath, basePath);
      } else if (file.endsWith('.html')) {
        const relativePath = path.relative(basePath, filePath);
        const urlPath = relativePath.replace('.html', '');
        urls.push({
          loc: `${CONFIG.baseUrl}/${urlPath}`,
          lastmod: '2026-05-14',
          changefreq: 'weekly',
          priority: '0.8'
        });
      }
    });
  }
  
  scanDirectory(dirPath, CONFIG.pagesDir);
  
  // Generate sitemap XML
  let sitemapXML = '<?xml version="1.0" encoding="UTF-8"?>\n';
  sitemapXML += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
  
  urls.forEach(url => {
    sitemapXML += '  <url>\n';
    sitemapXML += `    <loc>${url.loc}</loc>\n`;
    sitemapXML += `    <lastmod>${url.lastmod}</lastmod>\n`;
    sitemapXML += `    <changefreq>${url.changefreq}</changefreq>\n`;
    sitemapXML += `    <priority>${url.priority}</priority>\n`;
    sitemapXML += '  </url>\n';
  });
  
  sitemapXML += '</urlset>';
  
  const sitemapPath = path.join(__dirname, '..', 'public', sitemapName);
  fs.writeFileSync(sitemapPath, sitemapXML, 'utf-8');
  
  console.log(`\n✓ Generated ${sitemapName} with ${urls.length} URLs`);
}

/**
 * Main function
 */
function main() {
  console.log('TechSpecs Hub - Schema Generator\n');
  console.log('================================\n');
  
  // Process specs pages
  console.log('\nProcessing specs pages...');
  processDirectory(CONFIG.specsDir);
  
  // Process troubleshooting pages
  console.log('\nProcessing troubleshooting pages...');
  processDirectory(CONFIG.troubleshootingDir);
  
  // Process root pages
  console.log('\nProcessing root pages...');
  processDirectory(CONFIG.pagesDir);
  
  // Generate sitemaps
  console.log('\nGenerating sitemaps...');
  generateSitemap(CONFIG.pagesDir, 'sitemap-pages.xml');
  generateSitemap(CONFIG.specsDir, 'sitemap-specs.xml');
  generateSitemap(CONFIG.troubleshootingDir, 'sitemap-troubleshooting.xml');
  
  console.log('\n================================');
  console.log('Schema generation complete!');
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = {
  extractDataFromHTML,
  generateSchema,
  processHTMLFile
};
