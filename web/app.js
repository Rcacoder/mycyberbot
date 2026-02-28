document.addEventListener('DOMContentLoaded', () => {
    fetchAvailableDates();
});

async function fetchAvailableDates() {
    const listContainer = document.getElementById('date-list');
    
    try {
        const response = await fetch('/api/reports');
        const data = await response.json();
        
        listContainer.innerHTML = '';
        
        if (data.reports && data.reports.length > 0) {
            data.reports.forEach((dateStr, index) => {
                const btn = document.createElement('button');
                btn.className = 'date-btn';
                
                // Format date nicely
                const dateObj = new Date(dateStr);
                const displayDate = isNaN(dateObj.getTime()) ? dateStr : 
                                  dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                                  
                btn.innerHTML = `<span>🗓️</span> ${displayDate}`;
                btn.onclick = () => loadReport(dateStr, btn);
                listContainer.appendChild(btn);
                
                // Auto load the most recent report on first load
                if (index === 0) {
                    loadReport(dateStr, btn);
                }
            });
        } else {
            listContainer.innerHTML = '<p style="color:var(--text-muted); padding:10px;">No reports generated yet. Run main.py first.</p>';
        }
    } catch (err) {
        console.error("Failed to fetch dates", err);
        listContainer.innerHTML = '<p style="color:#ff0844; padding:10px;">Error connecting to API.</p>';
    }
}

async function loadReport(dateStr, btnElement) {
    // Update active state in sidebar
    document.querySelectorAll('.date-btn').forEach(btn => btn.classList.remove('active'));
    if (btnElement) {
        btnElement.classList.add('active');
    }
    
    // Toggle views
    document.getElementById('empty-state').classList.add('hidden');
    document.getElementById('dashboard-content').classList.remove('hidden');
    
    // Fetch JSON for specific date
    try {
        const response = await fetch(`/api/reports/${dateStr}`);
        if (!response.ok) throw new Error("Report not found");
        
        const data = await response.json();
        
        // Format Header title nicely
        const dateObj = new Date(dateStr);
        const displayDate = isNaN(dateObj.getTime()) ? dateStr : 
                          dateObj.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
                          
        document.getElementById('report-title').textContent = `Intelligence: ${displayDate}`;
        
        renderAttacks(data.top_10_attacks || []);
        renderLessons(data.lessons || []);
        
    } catch (err) {
        console.error("Failed to load report", err);
        document.getElementById('dashboard-content').classList.add('hidden');
        document.getElementById('empty-state').classList.remove('hidden');
        document.getElementById('empty-state').innerHTML = `<div class="icon-large">❌</div><p>Error loading report for ${dateStr}</p>`;
    }
}

function renderAttacks(attacks) {
    const grid = document.getElementById('attacks-grid');
    grid.innerHTML = '';
    
    if (attacks.length === 0) {
        grid.innerHTML = '<p class="subtitle fade-in">No attacks recorded for this date.</p>';
        return;
    }
    
    attacks.forEach((attack, index) => {
        const severityClass = attack.rank <= 3 ? 'critical' : 'high';
        
        const card = document.createElement('div');
        card.className = `attack-card ${severityClass}`;
        
        // Add staggering animation delay
        card.style.animation = `fadeIn 0.5s ease forwards ${index * 0.05}s`;
        card.style.opacity = '0';
        
        card.innerHTML = `
            <div class="card-header">
                <span class="rank-badge">#${attack.rank || '-'}</span>
                <span class="card-source">${attack.source || 'Unknown'}</span>
            </div>
            <h3 class="card-title">
                ${attack.link ? `<a href="${attack.link}" target="_blank">${attack.title}</a>` : attack.title}
            </h3>
            <p class="card-summary">${attack.summary || 'No summary available.'}</p>
        `;
        
        grid.appendChild(card);
    });
}

function renderLessons(lessons) {
    const container = document.getElementById('lessons-container');
    container.innerHTML = '';
    
    if (lessons.length === 0) {
         document.querySelector('.lessons-section').classList.add('hidden');
         return;
    } else {
         document.querySelector('.lessons-section').classList.remove('hidden');
    }
    
    lessons.forEach((lesson, index) => {
        const panel = document.createElement('div');
        panel.className = 'lesson-panel';
        
        panel.style.animation = `fadeIn 0.6s ease forwards ${index * 0.2 + 0.3}s`;
        panel.style.opacity = '0';
        
        // Build Lists safely
        const objHtml = (lesson.learning_objectives || []).map(li => `<li>${li}</li>`).join('');
        const mitHtml = (lesson.mitigation_strategies || []).map(li => `<li>${li}</li>`).join('');
        const qHtml = (lesson.discussion_questions || []).map(li => `<li>${li}</li>`).join('');
        
        panel.innerHTML = `
            <div class="lesson-title-area">
                <span class="lesson-rank">Deep Dive Focus #${lesson.rank || '-'}</span>
                <h3>${lesson.title || 'Untitled Lesson'}</h3>
            </div>
            
            <div class="lesson-content">
                <div class="lesson-left">
                    <div class="lesson-block mb-4">
                        <h4>Real-World Impact</h4>
                        <p>${lesson.real_world_impact || 'No impact analysis provided.'}</p>
                    </div>
                    <div class="lesson-block">
                        <br>
                        <h4>Learning Objectives</h4>
                        <ul>${objHtml}</ul>
                    </div>
                </div>
                
                <div class="lesson-right">
                    <div class="lesson-block mb-4">
                        <h4>Mitigation Strategies</h4>
                        <ul>${mitHtml}</ul>
                    </div>
                    <div class="lesson-block">
                        <br>
                        <h4>Classroom Discussion</h4>
                        <ul>${qHtml}</ul>
                    </div>
                </div>
            </div>
        `;
        
        container.appendChild(panel);
    });
}
