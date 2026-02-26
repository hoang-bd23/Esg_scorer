const fs = require('fs');
const pdfjs = require('pdfjs-dist/legacy/build/pdf.mjs');

async function extractPDF(filePath, outputPath) {
    const data = new Uint8Array(fs.readFileSync(filePath));
    const doc = await pdfjs.getDocument({ data }).promise;

    let fullText = '';
    for (let i = 1; i <= doc.numPages; i++) {
        const page = await doc.getPage(i);
        const content = await page.getTextContent();
        const pageText = content.items.map(item => item.str).join(' ');
        fullText += `--- Page ${i} ---\n${pageText}\n\n`;
    }

    fs.writeFileSync(outputPath, fullText, 'utf8');
    console.log(`Extracted ${doc.numPages} pages from ${filePath}`);
    console.log(`Text length: ${fullText.length} characters`);
}

async function main() {
    await extractPDF(
        'F:\\A Personal PJ\\Esg_score\\scoring principles\\admin,+BAI+8_3783-econ.en-Appendix-ok.pdf',
        'F:\\A Personal PJ\\Esg_score\\scoring_principles_text.txt'
    );
    await extractPDF(
        'F:\\A Personal PJ\\Esg_score\\company evaluation document\\SAM_2024.pdf',
        'F:\\A Personal PJ\\Esg_score\\company_evaluation_text.txt'
    );
}

main().catch(console.error);
