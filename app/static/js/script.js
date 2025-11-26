document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('btn-upload-resume');
    
    if (uploadBtn) {
        uploadBtn.addEventListener('click', uploadResume);
    }
});

async function uploadResume() {
    const fileInput = document.getElementById('resumeFile');
    const status = document.getElementById('uploadStatus');
    const skillsInput = document.getElementById('skillsInput');

    if (fileInput.files.length === 0) {
        alert("Please select a PDF file first.");
        return;
    }

    const formData = new FormData();
    formData.append('resume', fileInput.files[0]);

    // Show loading state
    status.innerHTML = '<span class="loading-spinner"></span> Extracting skills...';
    status.className = "text-primary mt-2 d-block";

    try {
        const response = await fetch('/upload-resume', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        if (data.extracted_skills && data.extracted_skills.length > 0) {
            // Auto-fill the input
            skillsInput.value = data.extracted_skills.join(', ');
            
            // Success message
            status.innerText = `Success! Found ${data.extracted_skills.length} skills.`;
            status.className = "text-success mt-2 d-block fw-bold";
        } else {
            status.innerText = "No skills identified. Try adding them manually.";
            status.className = "text-warning mt-2 d-block";
        }
    } catch (e) {
        console.error(e);
        status.innerText = "Error uploading file. Please try again.";
        status.className = "text-danger mt-2 d-block";
    }
}
document.addEventListener('DOMContentLoaded', () => {
    
    // --- DARK MODE LOGIC START ---
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    const icon = themeToggleBtn.querySelector('span'); // We will use an emoji span

    // 1. Check LocalStorage on load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        htmlElement.setAttribute('data-bs-theme', 'dark');
        icon.innerText = '☀️'; // Show Sun icon because mode is dark
    } else {
        htmlElement.setAttribute('data-bs-theme', 'light');
        icon.innerText = '🌙'; // Show Moon icon
    }

    // 2. Toggle on click
    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = htmlElement.getAttribute('data-bs-theme');
        
        if (currentTheme === 'dark') {
            htmlElement.setAttribute('data-bs-theme', 'light');
            localStorage.setItem('theme', 'light');
            icon.innerText = '🌙';
        } else {
            htmlElement.setAttribute('data-bs-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            icon.innerText = '☀️';
        }
    });
    // --- DARK MODE LOGIC END ---

    // ... existing Resume Upload logic ...
    const uploadBtn = document.getElementById('btn-upload-resume');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', uploadResume);
    }
});

// ... existing functions ...