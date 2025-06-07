let selectedFile = null;

class ButtonController {
    constructor(buttonId) {
        this.button = document.getElementById(buttonId);
        this.originalContent = this.button.innerHTML;
    }

    reset() {
        this.button.disabled = false;
        this.button.innerHTML = this.originalContent;
    }

    setLoading() {
        this.button.disabled = true;
        this.button.innerHTML = `
            <span class="relative z-10 flex items-center justify-center space-x-2">
                <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Processing...</span>
            </span>
        `;
    }
}

const aiOutput = {
    name: "",
    email: "",
    core_skills: [],
    soft_skills: [],
    resume_rating: 0,
    improvement_areas: "",
    upskill_suggestions: "",
};

const buttonController = new ButtonController("upload-btn");
const resumeFile = document.getElementById("resume-file");
const uploadButton = document.getElementById("upload-btn");
const uploadArea = document.getElementById("upload-area");
const error = document.getElementById("error");
const loading = document.getElementById("loading");
const resultsModal = document.getElementById("results-modal");

// Initialize drag and drop functionality
function initializeDragAndDrop() {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    uploadArea.addEventListener('drop', handleDrop, false);
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    uploadArea.classList.add('file-drop-active');
}

function unhighlight(e) {
    uploadArea.classList.remove('file-drop-active');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        handleFileSelection(files[0]);
    }
}

function handleFileSelection(file) {
    selectedFile = file;
    const fileName = document.getElementById("file-name");
    fileName.textContent = file.name;
    fileName.classList.add('text-green-600');
    uploadButton.removeAttribute("disabled");
    
    // Add file size info
    const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);
    fileName.textContent += ` (${sizeInMB} MB)`;
}

function showError(message) {
    error.classList.remove("hidden");
    error.querySelector("#error-message").textContent = message;
}

function hideError() {
    error.classList.add("hidden");
}

function showLoading() {
    loading.classList.remove("hidden");
    document.querySelector('form').style.display = 'none';
}

function hideLoading() {
    loading.classList.add("hidden");
    document.querySelector('form').style.display = 'block';
}

function showResultsModal() {
    resultsModal.classList.remove("hidden");
    populateResults();
}

function closeResultsModal() {
    resultsModal.classList.add("hidden");
}

function populateResults() {
    document.getElementById("result-name").textContent = aiOutput.name || "Not provided";
    document.getElementById("result-email").textContent = aiOutput.email || "Not provided";
    
    // Rating
    const rating = aiOutput.resume_rating || 0;
    const ratingBar = document.getElementById("rating-bar");
    const ratingText = document.getElementById("rating-text");
    
    setTimeout(() => {
        ratingBar.style.width = `${rating}%`;
        ratingText.textContent = `${rating}/10`;
    }, 500);
    
    // Core Skills
    const coreSkillsContainer = document.getElementById("core-skills");
    coreSkillsContainer.innerHTML = "";
    (aiOutput.core_skills || []).forEach(skill => {
        const skillTag = document.createElement("span");
        skillTag.className = "bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium animate-slide-down";
        skillTag.textContent = skill;
        coreSkillsContainer.appendChild(skillTag);
    });
    
    // Soft Skills
    const softSkillsContainer = document.getElementById("soft-skills");
    softSkillsContainer.innerHTML = "";
    (aiOutput.soft_skills || []).forEach(skill => {
        const skillTag = document.createElement("span");
        skillTag.className = "bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium animate-slide-down";
        skillTag.textContent = skill;
        softSkillsContainer.appendChild(skillTag);
    });
    

    document.getElementById("improvement-areas").innerHTML = formatText(aiOutput.improvement_areas);
    

    document.getElementById("upskill-suggestions").innerHTML = formatText(aiOutput.upskill_suggestions);
}

function formatText(text) {
    if (!text) return "No suggestions available.";
    
    // Convert bullet points to HTML list
    if (text.includes('•') || text.includes('-')) {
        const lines = text.split('\n').filter(line => line.trim());
        const listItems = lines.map(line => {
            const cleanLine = line.replace(/^[•\-\*]\s*/, '').trim();
            return cleanLine ? `<li class="mb-2">${cleanLine}</li>` : '';
        }).filter(item => item);
        
        return `<ul class="list-disc list-inside space-y-2">${listItems.join('')}</ul>`;
    }
    
    return `<p>${text}</p>`;
}



function downloadReport() {
    const reportContent = `
RESUME ANALYSIS REPORT
======================

Personal Information:
- Name: ${aiOutput.name || "Not provided"}
- Email: ${aiOutput.email || "Not provided"}

Resume Rating: ${aiOutput.resume_rating || 0}/10

Core Skills:
${(aiOutput.core_skills || []).map(skill => `- ${skill}`).join('\n')}

Soft Skills:
${(aiOutput.soft_skills || []).map(skill => `- ${skill}`).join('\n')}

Areas for Improvement:
${aiOutput.improvement_areas || "No suggestions available."}

Upskill Suggestions:
${aiOutput.upskill_suggestions || "No suggestions available."}

Generated on: ${new Date().toLocaleDateString()}
    `;
    
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resume-analysis-report.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

function goBack() {
    window.history.back();
}

// File input change handler
resumeFile.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileSelection(file);
    } else {
        selectedFile = null;
        const fileName = document.getElementById("file-name");
        fileName.textContent = "No file selected";
        fileName.classList.remove('text-green-600');
        uploadButton.setAttribute("disabled", true);
    }
});

// Form submission handler
async function handleSubmit(event) {
    event.preventDefault();
    
    if (!selectedFile) {
        showError("Please select a file before submitting.");
        return;
    }
    
    if (selectedFile.size > 10 * 1024 * 1024) {
        showError("File size exceeds 10MB limit.");
        return;
    }
    
    const title = event.target.querySelector("#title").value || 'Frontend Intern';
    if (!title.trim()) {
        showError("Please enter a job title.");
        return;
    }
    
    // Validate file type
    const fileName = selectedFile.name;
    const allowedExtensions = ["pdf", "doc", "docx"];
    const fileArray = fileName.split(".");
    const currentExtension = fileArray[fileArray.length - 1].toLowerCase();
    
    if (!allowedExtensions.includes(currentExtension)) {
        showError("Invalid file type. Please upload a PDF, DOC, or DOCX file.");
        return;
    }
    
    const formData = new FormData();
    formData.append("resume", selectedFile);
    formData.append("title", title);
    
    buttonController.setLoading();
    showLoading();
    
    try {

        const response = await axios.post("/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        const responseData = response.data;
        if (responseData.status === "error") {
            showError(responseData.error);
        } else {
            hideError();
            const resp = responseData.data;
            
            // Update aiOutput with response data
            Object.assign(aiOutput, resp);
            
            console.log("Analysis complete:", resp);
            
            // Show results modal
            hideLoading();
            showResultsModal();
        }
    } catch (error) {
        console.error("Error uploading file:", error);
        showError("An error occurred while processing your resume. Please try again.");
        hideLoading();
    } finally {
        buttonController.reset();
    }
}

// Initialize drag and drop when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDragAndDrop();
    
    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === error) {
            hideError();
        }
        if (event.target === resultsModal) {
            closeResultsModal();
        }
    });
});

// Expose functions to global scope for HTML onclick handlers
window.handleSubmit = handleSubmit;
window.showError = showError;
window.hideError = hideError;
window.closeResultsModal = closeResultsModal;
window.downloadReport = downloadReport;
window.goBack = goBack;