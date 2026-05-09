let polarityChartInstance = null;
let currentData = null; 

async function analyzeSentiment() {
    const keyword = document.getElementById('keywordInput').value;
    // Grab the slider value!
    const limit = document.getElementById('limitSlider').value; 
    
    const btn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loadingMsg');
    const errorMsg = document.getElementById('errorMsg');
    const dashboard = document.getElementById('dashboard');

    if (!keyword) return alert("Please enter a keyword.");

    btn.disabled = true;
    loading.classList.remove('hidden');
    errorMsg.classList.add('hidden');
    dashboard.classList.add('hidden');

    try {
        // Send both the keyword AND the limit to our Azure Function
        const response = await fetch(`http://localhost:7071/api/analyze?keyword=${encodeURIComponent(keyword)}&limit=${limit}`);
        
        if (!response.ok) throw new Error(`API returned status: ${response.status}`);
        
        const data = await response.json();
        currentData = data; 

        
        const scanDate = new Date(data.timestamp).toLocaleTimeString();
        const metaEl = document.getElementById('metaInfo');
        metaEl.innerText = `Analyzed ${data.articles.length} live articles at ${scanDate}`;
        metaEl.classList.remove('hidden');

        document.getElementById('mainScore').innerText = `${data.average_score}%`;
        
        const labelEl = document.getElementById('mainLabel');
        labelEl.innerText = data.label;
        labelEl.className = "text-xl font-medium px-4 py-1 rounded-full ";
        
        if (data.label === "Positive") labelEl.classList.add("bg-green-900", "text-green-300");
        else if (data.label === "Negative") labelEl.classList.add("bg-red-900", "text-red-300");
        else labelEl.classList.add("bg-gray-700", "text-gray-300");

        drawChart(data.positive_score, data.neutral_score, data.negative_score);

        // FEATURE UPDATE: Individual Article Sentiment UI
        const listEl = document.getElementById('headlineList');
        listEl.innerHTML = ''; 
        
        // BUG FIX: Changed 'headlines' to 'articles'
        data.articles.forEach(article => {
            // Determine the color for the individual article pill
            let pillColor = "bg-gray-700 text-gray-300";
            if (article.label === "Positive") pillColor = "bg-green-900 text-green-300";
            if (article.label === "Negative") pillColor = "bg-red-900 text-red-300";

            listEl.innerHTML += `
                <li class="border-b border-gray-700 pb-4 mb-4 flex flex-col gap-2">
                    <div class="flex items-center gap-3">
                        <span class="text-xs text-blue-400 font-bold uppercase">${article.source}</span>
                        <span class="text-xs px-2 py-0.5 rounded-full font-semibold ${pillColor}">
                            ${article.label} (${article.score}%)
                        </span>
                    </div>
                    <a href="${article.url}" target="_blank" class="text-gray-200 hover:text-white transition-colors text-sm">${article.title}</a>
                </li>
            `;
        });

        dashboard.classList.remove('hidden');

    } catch (error) {
        errorMsg.innerText = `Pipeline Error: ${error.message}. Ensure your Azure Function is running!`;
        errorMsg.classList.remove('hidden');
    } finally {
        btn.disabled = false;
        loading.classList.add('hidden');
    }
}

function drawChart(pos, neu, neg) {
    const ctx = document.getElementById('polarityChart').getContext('2d');
    if (polarityChartInstance) polarityChartInstance.destroy();

    polarityChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                data: [pos, neu, neg],
                backgroundColor: ['#22c55e', '#6b7280', '#ef4444'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { color: '#fff' } }
            }
        }
    });
}

// FEATURE UPDATE: Upgraded CSV Export
function exportToCSV() {
    // BUG FIX: Changed 'headlines' to 'articles'
    if (!currentData || !currentData.articles || currentData.articles.length === 0) {
        return alert("No data available to export. Please run an analysis first.");
    }

    // Added new columns for Sentiment Label and Score
    let csvContent = "Source,Headline,URL,Sentiment Label,Confidence Score\n";

    currentData.articles.forEach(article => {
        let safeTitle = article.title.replace(/"/g, '""'); 
        // Added the new data points to the CSV rows
        csvContent += `"${article.source}","${safeTitle}","${article.url}","${article.label}","${article.score}%"\n`;
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `sentiment_export_${currentData.search_term.replace(/\s+/g, '_')}.csv`);
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}