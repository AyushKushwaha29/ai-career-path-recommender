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