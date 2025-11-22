/**
 * Extract ALL project IDs from ALL pages of the download section
 *
 * INSTRUCTIONS:
 * 1. Open https://guolab.wchscu.cn/EVmiRNA2.0/#/download
 * 2. Wait for the first page to load
 * 3. Open browser console (F12)
 * 4. Copy and paste this entire script
 * 5. Press Enter and WAIT - it will automatically navigate through all pages
 */

(async function() {
    'use strict';

    console.log('========================================');
    console.log('Project ID Extractor (All Pages)');
    console.log('========================================');

    const projectIds = new Set();
    let currentPage = 1;
    let totalPages = 1;

    // Function to extract IDs from current page
    function extractIdsFromCurrentPage() {
        const pageText = document.body.textContent;
        const matches = pageText.match(/PRJ[A-Z]{2}\d+/g);

        if (matches) {
            const beforeCount = projectIds.size;
            matches.forEach(id => projectIds.add(id));
            const newIds = projectIds.size - beforeCount;
            console.log(`  Found ${newIds} new IDs on this page (${projectIds.size} total)`);
            return newIds;
        }
        return 0;
    }

    // Function to get total number of pages
    function getTotalPages() {
        // Try to find pagination component
        // Common patterns in Vue.js pagination:
        const paginationTexts = [
            ...document.querySelectorAll('.el-pagination, .pagination, [class*="page"]')
        ].map(el => el.textContent);

        // Look for "/ XX" or "of XX" patterns
        for (const text of paginationTexts) {
            const match = text.match(/\/\s*(\d+)|of\s+(\d+)|共\s*(\d+)/);
            if (match) {
                return parseInt(match[1] || match[2] || match[3]);
            }
        }

        // Try to find page number buttons
        const pageButtons = document.querySelectorAll('.el-pager li, .page-item, [class*="page-"]');
        let maxPage = 1;
        pageButtons.forEach(btn => {
            const num = parseInt(btn.textContent);
            if (num > maxPage) maxPage = num;
        });

        return maxPage;
    }

    // Function to click next page
    function goToNextPage() {
        // Try different selectors for "next" button
        const nextSelectors = [
            '.el-pagination .btn-next',
            '.el-pagination button.el-icon-arrow-right',
            '.pagination .next',
            'button[aria-label="Next"]',
            'button:has(.el-icon-arrow-right)',
            '[class*="next"]'
        ];

        for (const selector of nextSelectors) {
            const nextBtn = document.querySelector(selector);
            if (nextBtn && !nextBtn.disabled && !nextBtn.classList.contains('disabled')) {
                console.log(`  Clicking next page button...`);
                nextBtn.click();
                return true;
            }
        }

        // Try to find and click page number
        const pageButtons = document.querySelectorAll('.el-pager li');
        for (const btn of pageButtons) {
            if (btn.textContent.trim() === String(currentPage + 1)) {
                console.log(`  Clicking page ${currentPage + 1}...`);
                btn.click();
                return true;
            }
        }

        return false;
    }

    // Function to wait for page to load
    function waitForPageLoad(ms = 2000) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    console.log('\nStarting extraction from all pages...\n');

    // Extract from first page
    console.log(`Page ${currentPage}:`);
    extractIdsFromCurrentPage();

    // Determine total pages
    totalPages = getTotalPages();
    console.log(`\nDetected ${totalPages} total pages\n`);

    // Navigate through remaining pages
    while (currentPage < totalPages) {
        await waitForPageLoad(2000);  // Wait for page to load

        if (!goToNextPage()) {
            console.log('\n⚠️  Could not find next page button. Trying alternative method...');

            // Alternative: Try to set page number directly if there's an input
            const pageInput = document.querySelector('.el-pagination__jump input');
            if (pageInput) {
                currentPage++;
                console.log(`  Jumping to page ${currentPage}...`);
                pageInput.value = currentPage;
                pageInput.dispatchEvent(new Event('input'));

                const confirmBtn = document.querySelector('.el-pagination__jump button');
                if (confirmBtn) confirmBtn.click();

                await waitForPageLoad(2000);
            } else {
                break;
            }
        } else {
            currentPage++;
        }

        await waitForPageLoad(2000);  // Wait for new content to load

        console.log(`Page ${currentPage}:`);
        const newIds = extractIdsFromCurrentPage();

        if (newIds === 0 && currentPage > 2) {
            console.log('  No new IDs found - might have reached the end');
            break;
        }
    }

    // Convert to sorted array
    const sortedIds = Array.from(projectIds).sort();

    console.log(`\n${'='.repeat(60)}`);
    console.log(`✓ Extraction Complete!`);
    console.log('='.repeat(60));
    console.log(`Total unique project IDs: ${sortedIds.length}`);
    console.log(`Pages processed: ${currentPage}`);
    console.log('='.repeat(60));

    // Show first and last few IDs
    console.log('\nFirst 10 IDs:');
    sortedIds.slice(0, 10).forEach((id, i) => console.log(`  ${i + 1}. ${id}`));

    if (sortedIds.length > 20) {
        console.log('\n  ...');
        console.log(`\nLast 10 IDs:`);
        sortedIds.slice(-10).forEach((id, i) => console.log(`  ${sortedIds.length - 10 + i + 1}. ${id}`));
    }

    // Create downloadable files
    console.log(`\n${'='.repeat(60)}`);
    console.log('Creating downloadable files...');
    console.log('='.repeat(60));

    // Text file
    const blob = new Blob([sortedIds.join('\n')], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'project_ids.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    console.log('✓ Downloaded project_ids.txt');

    // JSON file
    const jsonBlob = new Blob([JSON.stringify(sortedIds, null, 2)], { type: 'application/json' });
    const jsonUrl = URL.createObjectURL(jsonBlob);
    const jsonA = document.createElement('a');
    jsonA.href = jsonUrl;
    jsonA.download = 'project_ids.json';
    document.body.appendChild(jsonA);
    jsonA.click();
    document.body.removeChild(jsonA);
    URL.revokeObjectURL(jsonUrl);
    console.log('✓ Downloaded project_ids.json');

    console.log(`\n${'='.repeat(60)}`);
    console.log('Done! Check your Downloads folder.');
    console.log('='.repeat(60));

    return sortedIds;
})();
