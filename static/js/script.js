// Check if elements exist before adding event listeners
const remoteCheckbox = document.getElementById('remote');
const autismCheckbox = document.getElementById('autism-level-3-1');

if (remoteCheckbox && autismCheckbox) {
    remoteCheckbox.addEventListener('change', function () {
        if (this.checked == false) {
            autismCheckbox.checked = false;
            autismCheckbox.disabled = true;
            console.log('Autism checkbox was unchecked and disabled');
        } else {
            autismCheckbox.disabled = false;
        }
    });
}



//okay yg ni untuk toggle preview, kalau tekan dia nanti dia akan display. tapi make sure dh ada checkbox dia punya id dengan preview id dia la
function setupCheckboxPreview(checkboxId, previewId) {
      const checkbox = document.getElementById(checkboxId);
      const preview = document.getElementById(previewId);
      checkbox.addEventListener('change', () => {
        preview.classList.toggle('d-none', !checkbox.checked);
      });
    }
//sokay ni call listing untuk setup checkbox tu
    if (document.getElementById('full-time')) setupCheckboxPreview('full-time','previewFullTime');
    if (document.getElementById('part-time')) setupCheckboxPreview('part-time','previewPartTime');
    if (document.getElementById('remote')) setupCheckboxPreview('remote','previewRemote');

//okay this one untuk radio button, sama macam function atas tadi, beza dia ni dia ambik name instead of id so lets go little 
//jangan padam ni 
    function setupRadioPreview(radioName, previewId) {
      const radios = document.querySelectorAll(`input[name="${radioName}"]`);
      const preview = document.getElementById(previewId);
      if (radios.length > 0 && preview) {
        radios.forEach(radio => {
          radio.addEventListener('change', () => {
            const selected = document.querySelector(`input[name="${radioName}"]:checked`);
            if (selected) {
              preview.textContent = `${selected.value}`;
              preview.classList.remove('d-none');
            } else {
              preview.classList.add('d-none');
            }
          });
        });
      }
    }
//these kita call balik function setupRadioPreview tu
    if (document.querySelector('input[name="job-category"]')) setupRadioPreview('job-category','previewJobCategory')


//this function will be the goat, cuz it will add required to the opened text area
function addRequiredIfChecked(toggleId, textareaId) {
  const trigger = document.getElementById(toggleId);     // checkbox or radio
  const target = document.getElementById(textareaId);  // input/textarea/select/etc

  function updateRequired() {
    if (trigger.checked) {
      target.setAttribute('required', 'required');
    } else {
      target.removeAttribute('required');
    }
  }

  trigger.addEventListener('change', updateRequired);

  // Initialize on page load
  updateRequired();
}

function addRequiredIfRadioChecked(radioName, wrapperId, mapWrap) {
  const radios = document.querySelectorAll(`input[name="${radioName}"]`);
  const wrapper = document.getElementById(wrapperId);
  const target = wrapper.querySelector('textarea');

  function updateRequired() {
    const selected = Array.from(radios).find(r => r.checked);
    if (selected && selected.value && selected.value !== 'none') {
      target.setAttribute('required', 'required');
    } else {
      target.removeAttribute('required');
    }
  }

  radios.forEach(radio => {
    radio.addEventListener('change', updateRequired);
  });

  // Initialize on load
  updateRequired();

  // Optional: attach to mapWrap so you can call it from outside if needed
  mapWrap.updateRequired = updateRequired;
}



//function ni untuk sigma ohayo yg power code. function ni digunakan untuk buat preview yg sangat epic
function setupTextareaTogglePreview(toggleId, previewTitleId, previewTextId, textareaId, wrapperId) {
  const toggle = document.getElementById(toggleId);
  const previewTitle = document.getElementById(previewTitleId);
  const previewText = document.getElementById(previewTextId);
  const textarea = document.getElementById(textareaId);
  const wrapper = document.getElementById(wrapperId);

  const collapse = new bootstrap.Collapse(wrapper, {
    toggle: false // prevent it from auto toggling on init
  });

  function updatePreview() {
    if (toggle.checked) {
      collapse.show(); // show textarea
      previewTitle.classList.remove('d-none');
      previewText.classList.remove('d-none');
      previewText.textContent = textarea.value;
    } else {
      collapse.hide(); // hide textarea
      previewTitle.classList.add('d-none');
      previewText.classList.add('d-none');
      previewText.textContent = '';
    }
  }

  toggle.addEventListener('change', updatePreview);
  textarea.addEventListener('input', () => {
    previewText.textContent = textarea.value;
  });
  addRequiredIfChecked(toggleId, textareaId);
  // initialize on load
  updatePreview();
}


function setupRadioWithTextareaAndFixedPreview({ radioName, wrapperId, previewTitleId, previewDescId, labelMap }) {
  const radios = document.querySelectorAll(`input[name="${radioName}"]`);
  const wrapper = document.getElementById(wrapperId);
  const textarea = wrapper.querySelector('textarea');
  const collapseEl = wrapper.querySelector('.collapse');
  const previewTitle = document.getElementById(previewTitleId);
  const previewDesc = document.getElementById(previewDescId);

  const bsCollapse = new bootstrap.Collapse(collapseEl, { toggle: false });

  function updatePreview() {
    const selected = document.querySelector(`input[name="${radioName}"]:checked`);
    if (!selected || selected.value === 'none') {
      bsCollapse.hide();
      textarea.value = '';
      previewTitle.classList.add('d-none');
      previewDesc.classList.add('d-none');
      previewTitle.textContent = '';
      previewDesc.textContent = '';
    } else {
      const label = labelMap[selected.value] || selected.value;

      bsCollapse.show();
      previewTitle.classList.remove('d-none');
      previewDesc.classList.remove('d-none');

      previewTitle.innerHTML = `<b>${label}</b>`;
      previewDesc.textContent = textarea.value;
    }
  }

  radios.forEach(radio => {
    radio.addEventListener('change', updatePreview);
  });

  textarea.addEventListener('input', () => {
    previewDesc.textContent = textarea.value;
  });

  addRequiredIfRadioChecked(radioName, wrapperId, labelMap)
  updatePreview();
}

function setupSimpleTextareaPreview(textareaId, previewDescId) {
      const textarea = document.getElementById(textareaId);
      const preview = document.getElementById(previewDescId);

      function update() {
        const value = textarea.value.trim();
        if (value) {
          preview.classList.remove('d-none');
          preview.textContent = value;
        } else {
          preview.classList.add('d-none');
          preview.textContent = '';
        }
      }

      textarea.addEventListener('input', update);
      update(); // Initialize once
    }

// ✅ Setup simple textarea preview
if (document.getElementById('jobtitle')) setupSimpleTextareaPreview('jobtitle','previewJobTitle');
if (document.getElementById('state')) setupSimpleTextareaPreview('state','previewState');
if (document.getElementById('city')) setupSimpleTextareaPreview('city','previewCity');
if (document.getElementById('min-pay')) setupSimpleTextareaPreview('min-pay','previewMinSalary');
if (document.getElementById('max-pay')) setupSimpleTextareaPreview('max-pay','previewMaxSalary');
if (document.getElementById('question1')) setupSimpleTextareaPreview('question1','previewQuestion1');
if (document.getElementById('question2')) setupSimpleTextareaPreview('question2','previewQuestion2');
if (document.getElementById('question3')) setupSimpleTextareaPreview('question3','previewQuestion3');
if (document.getElementById('maintask')) setupSimpleTextareaPreview('maintask','previewMainTaskDesc');

// ✅ Setup checkbox-only preview
if (document.getElementById('repetitiveTask')) setupCheckboxPreview('repetitiveTask', 'previewRepetitiveTask');
if (document.getElementById('easyToPerform')) setupCheckboxPreview('easyToPerform', 'previewEasyToPerform');
if (document.getElementById('easyToRemember')) setupCheckboxPreview('easyToRemember', 'previewEasyToRemember');
if (document.getElementById('noInterview')) setupCheckboxPreview('noInterview', 'previewNoInterview');
if (document.getElementById('lessNoisy')) setupCheckboxPreview('lessNoisy', 'previewLessNoisy');
if (document.getElementById('lessStressful')) setupCheckboxPreview('lessStressful', 'previewLessStressful');
if (document.getElementById('autism-level-1')) setupCheckboxPreview('autism-level-1', 'previewLevel1');
if (document.getElementById('autism-level-2')) setupCheckboxPreview('autism-level-2', 'previewLevel2');
if (document.getElementById('autism-level-3-1')) setupCheckboxPreview('autism-level-3-1', 'previewLevel3');
// ✅ Setup checkbox + textarea preview
if (document.getElementById('toggleSubtask')) setupTextareaTogglePreview('toggleSubtask', 'previewSubTask', 'previewSubTaskDesc', 'subtask', 'subtaskWrapper');
if (document.getElementById('toggleInteractionWithCustomer')) setupTextareaTogglePreview('toggleInteractionWithCustomer', 'previewInteractionWithCustomer', 'previewInteractionWithCustomerDesc', 'interactionWithCustomer', 'interactionWithCustomerWrapper');
if (document.getElementById('toggleVerbal')) setupTextareaTogglePreview('toggleVerbal', 'previewVerbal', 'previewVerbalDesc', 'verbal', 'verbalWrapper');
if (document.getElementById('toggleNonVerbal')) setupTextareaTogglePreview('toggleNonVerbal', 'previewNonVerbal', 'previewNonVerbalDesc', 'nonverbal', 'nonVerbalWrapper');
if (document.getElementById('toggleRepresentative')) setupTextareaTogglePreview('toggleRepresentative', 'previewRepresentative', 'previewRepresentativeDesc', 'representative', 'representativeWrapper');
if (document.getElementById('toggleSpecialTraining')) setupTextareaTogglePreview('toggleSpecialTraining', 'previewSpecialTraining', 'previewSpecialTrainingDesc', 'specialTraining', 'specialTrainingWrapper');
if (document.getElementById('toggleWorkBuddy')) setupTextareaTogglePreview('toggleWorkBuddy', 'previewWorkBuddy', 'previewWorkBuddyDesc', 'workBuddy', 'workBuddyWrapper');
if (document.getElementById('toggleMentor')) setupTextareaTogglePreview('toggleMentor', 'previewMentor', 'previewMentorDesc', 'mentor', 'mentorWrapper');
if (document.getElementById('toggleCalmingSpace')) setupTextareaTogglePreview('toggleCalmingSpace', 'previewCalmingSpace', 'previewCalmingSpaceDesc', 'calmingSpace', 'calmingSpaceWrapper');
if (document.getElementById('toggleProgressUpdate')) setupTextareaTogglePreview('toggleProgressUpdate', 'previewProgressUpdate', 'previewProgressUpdateDesc', 'progressUpdate', 'progressUpdateWrapper');
if (document.getElementById('toggleOtherNotes')) setupTextareaTogglePreview('toggleOtherNotes', 'previewOtherNotes', 'previewOtherNotesDesc', 'otherNotes', 'otherNotesWrapper');


// ✅ Setup radio + textarea preview
document.addEventListener("DOMContentLoaded", function () {
    if (document.querySelector('input[name="training-time"]')) {
      setupRadioWithTextareaAndFixedPreview({
        radioName: "training-time",
        wrapperId: "training-time",
        previewTitleId: "previewTrainingTime",
        previewDescId: "previewTrainingTimeDesc",
        labelMap: {
          one: "One Time Training",
          multiple: "Multiple Times Training"
        }
      });
    }

    if (document.querySelector('input[name="shift-arrangement"]')) {
      setupRadioWithTextareaAndFixedPreview({
        radioName: "shift-arrangement",
        wrapperId: "shift-arrangement",
        previewTitleId: "previewShiftArrangement",
        previewDescId: "previewShiftArrangementDesc",
        labelMap: {
          flexible: "Fully Flexible",
          pool: "Shift Pool"
        }
      });
    }

    if (document.querySelector('input[name="transportation"]')) {
      setupRadioWithTextareaAndFixedPreview({
        radioName: "transportation",
        wrapperId: "transportation",
        previewTitleId: "previewTransportation",
        previewDescId: "previewTransportationDesc",
        labelMap: {
          full: "Transportation Fully Provided",
          partial: "Transportation Partial Provided Only"
        }
      });
    }
  });



  //this function is for the navigation, very long and yeah it is confusing
  //make sure to use it properly like a sigma
  const stepMap = {
  classify: 'first-form',
  write: 'second-form',
  pre: 'third-form',
  review: 'fourth-form'
};

function goToStep(step) {
  const current = document.querySelector('.form-section.active');
  if (current) {
    const requiredFields = current.querySelectorAll('[required]');
    let allValid = true;

    requiredFields.forEach(field => {
      const isRadioOrCheckbox = (field.type === 'radio' || field.type === 'checkbox');
      if (isRadioOrCheckbox) {
        const name = field.name;
        const anyChecked = current.querySelectorAll(`input[name="${name}"]:checked`).length > 0;
        if (!anyChecked) {
          allValid = false;
          field.classList.add('is-invalid');
        } else {
          field.classList.remove('is-invalid');
        }
      } else if (!field.value.trim()) {
        field.classList.add('is-invalid');
        allValid = false;
      } else {
        field.classList.remove('is-invalid');
      }
    });

    if (!allValid) {
      alert("Please fill all required fields before continuing.");
      return;
    }
  }

  // Hide all sections
  document.querySelectorAll('.form-section').forEach(el => el.classList.remove('active'));

  // Reset all nav button styles
  document.querySelectorAll('.top-header-nav-alt2, .top-header-nav-selected-alt2').forEach(btn => {
    btn.classList.remove('top-header-nav-selected-alt2');
    btn.classList.add('top-header-nav-alt2');
  });

  // Show selected section
  const targetId = stepMap[step];
  if (targetId) {
    document.getElementById(targetId).classList.add('active');
  }

  // Highlight selected nav button
  const navBtn = document.getElementById('nav-' + step);
  if (navBtn) {
    navBtn.classList.remove('top-header-nav-alt2');
    navBtn.classList.add('top-header-nav-selected-alt2');
  }
}

// Applicant List Filtering Functionality
document.addEventListener('DOMContentLoaded', function() {
  console.log('Applicant filtering script loaded');
  
  // Get filter elements
  const searchInput = document.getElementById('applicant-search');
  const jobFilter = document.getElementById('job-filter');
  const statusFilter = document.getElementById('status-filter');
  const clearFilterBtn = document.getElementById('clear-filters');
  const applicantCols = document.querySelectorAll('#applicant-layout .col');
  
  console.log('Found elements:', {
    searchInput: !!searchInput,
    jobFilter: !!jobFilter,
    statusFilter: !!statusFilter,
    clearFilterBtn: !!clearFilterBtn,
    applicantCols: applicantCols.length
  });
  
  // Sample applicant data (in real app, this would come from backend)
  const applicantData = [
    {
      id: 1,
      name: 'Sarah Johnson',
      position: 'Software Developer',
      status: 'new',
      location: 'Kuala Lumpur',
      appliedDate: '2 days ago',
      skills: ['JavaScript', 'React', 'Python', 'Django']
    },
    {
      id: 2,
      name: 'Michael Chen',
      position: 'Data Analyst',
      status: 'shortlisted',
      location: 'Petaling Jaya',
      appliedDate: '1 week ago',
      skills: ['Python', 'SQL', 'Tableau', 'R']
    },
    {
      id: 3,
      name: 'Emma Rodriguez',
      position: 'Marketing Assistant',
      status: 'review',
      location: 'Subang Jaya',
      appliedDate: '3 days ago',
      skills: ['Social Media', 'Content Creation', 'Google Analytics', 'Canva']
    },
    {
      id: 4,
      name: 'David Lee',
      position: 'Software Developer',
      status: 'rejected',
      location: 'Kuala Lumpur',
      appliedDate: '5 days ago',
      skills: ['Java', 'Spring', 'MySQL', 'Docker']
    },
    {
      id: 5,
      name: 'Lisa Wong',
      position: 'Data Analyst',
      status: 'new',
      location: 'Petaling Jaya',
      appliedDate: '1 day ago',
      skills: ['Python', 'Pandas', 'Matplotlib', 'Scikit-learn']
    }
  ];

  // Function to filter applicants
  function filterApplicants() {
    console.log('Filtering applicants...');
    
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    const selectedJob = jobFilter ? jobFilter.value : '';
    const selectedStatus = statusFilter ? statusFilter.value : '';
    
    console.log('Filter criteria:', { searchTerm, selectedJob, selectedStatus });
    
    applicantCols.forEach((col) => {
      // Get data from HTML data attributes
      const name = col.dataset.name || '';
      const position = col.dataset.position || '';
      const status = col.dataset.status || '';
      const location = col.dataset.location || '';
      const skills = col.dataset.skills || '';
      
      let shouldShow = true;
      
      // Search filter - search in name, position, location, and skills
      if (searchTerm) {
        const searchMatch = 
          name.toLowerCase().includes(searchTerm) ||
          position.toLowerCase().includes(searchTerm) ||
          location.toLowerCase().includes(searchTerm) ||
          skills.toLowerCase().includes(searchTerm);
        
        if (!searchMatch) {
          shouldShow = false;
        }
      }
      
      // Job filter
      if (selectedJob && selectedJob !== 'all') {
        if (position !== selectedJob) {
          shouldShow = false;
        }
      }
      
      // Status filter
      if (selectedStatus && selectedStatus !== 'all') {
        if (status !== selectedStatus) {
          shouldShow = false;
        }
      }
      
      // Show/hide col
      if (shouldShow) {
        col.classList.remove('hidden');
      } else {
        col.classList.add('hidden');
      }
    });
    
    // Update results count
    updateResultsCount();
  }
  
  // Function to update results count
  function updateResultsCount() {
    const visibleCols = document.querySelectorAll('#applicant-layout .col:not(.hidden)');
    const totalCols = applicantCols.length;
    const resultsElement = document.getElementById('results-count');
    
    console.log(`Visible cols: ${visibleCols.length}/${totalCols}`);
    
    if (resultsElement) {
      resultsElement.textContent = `Showing ${visibleCols.length} of ${totalCols} applicants`;
    }
  }
  
  // Function to clear all filters
  function clearFilters() {
    console.log('Clearing filters...');
    
    if (searchInput) searchInput.value = '';
    if (jobFilter) jobFilter.value = 'all';
    if (statusFilter) statusFilter.value = 'all';
    
    // Show all cols
    applicantCols.forEach(col => {
      col.classList.remove('hidden');
    });
    
    updateResultsCount();
  }
  
  // Add event listeners
  if (searchInput) {
    searchInput.addEventListener('input', filterApplicants);
    searchInput.addEventListener('keyup', filterApplicants);
    console.log('Added input and keyup listeners to search');
  }
  
  if (jobFilter) {
    jobFilter.addEventListener('change', filterApplicants);
    console.log('Added change listener to job filter');
  }
  
  if (statusFilter) {
    statusFilter.addEventListener('change', filterApplicants);
    console.log('Added change listener to status filter');
  }
  
  if (clearFilterBtn) {
    clearFilterBtn.addEventListener('click', clearFilters);
    console.log('Added click listener to clear button');
  }
  
  // Initialize results count
  updateResultsCount();
  console.log('Initialized applicant filtering');
  
  // Test function - you can call this in browser console to test
  window.testFilter = function() {
    console.log('Testing filter function...');
    if (searchInput) {
      searchInput.value = 'Sarah';
      filterApplicants();
    }
  };
});

// Applicant Management Functions
function updateStatus() {
    const statusSelect = document.getElementById('application_status');
    if (!statusSelect) return;
    
    const selectedStatus = statusSelect.value;
    const selectedText = statusSelect.options[statusSelect.selectedIndex].text;
    
    // Update the status badge immediately
    updateStatusBadge();
    
    // You can add AJAX call here to update the status in the database
    // Example:
    // fetch('/update-application-status/', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'X-CSRFToken': getCookie('csrftoken')
    //     },
    //     body: JSON.stringify({
    //         status: selectedStatus,
    //         applicant_id: '123' // Replace with actual applicant ID
    //     })
    // })
}

// Helper function to get CSRF token (if needed for AJAX)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to update status badge color
function updateStatusBadge() {
    const statusSelect = document.getElementById('application_status');
    const statusBadge = document.getElementById('status-badge');
    
    if (!statusSelect || !statusBadge) return;
    
    const selectedValue = statusSelect.value;
    const selectedText = statusSelect.options[statusSelect.selectedIndex].text;
    
    // Remove all previous status classes
    statusBadge.classList.remove('status-pending', 'status-shortlisted', 'status-accepted', 'status-rejected');
    
    // Add the new one
    statusBadge.classList.add(`status-${selectedValue}`);
    
    // Update the text
    statusBadge.textContent = selectedText;
}


// Verification file upload preview (handles upload, reupload, and delete)
function setupVerificationFilePreview() {
    const uploadInput = document.getElementById('verification-upload-input');
    const reuploadInput = document.getElementById('verification-reupload-input');
    const preview = document.getElementById('verification-file-preview');
    const previewImg = document.getElementById('verification-preview-img');
    const fileIcon = document.getElementById('verification-file-icon');
    const fileName = document.getElementById('verification-file-name');
    const deleteBtn = document.querySelector('button[name="delete_file"].verification-btn');

    if (!uploadInput || !reuploadInput || !preview || !previewImg || !fileIcon || !fileName || !deleteBtn) return;

    function showFilePreview(file) {
        if (!file) {
            preview.classList.remove('has-file');
            previewImg.classList.add('d-none');
            fileIcon.className = 'fa fa-file-o verification-file-icon';
            fileIcon.classList.remove('d-none');
            fileName.textContent = 'No file uploaded';
            return;
        }
        preview.classList.add('has-file');
        fileName.textContent = file.name;
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;
                previewImg.classList.remove('d-none');
                fileIcon.classList.add('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            previewImg.classList.add('d-none');
            fileIcon.classList.remove('d-none');
            if (file.type === 'application/pdf') {
                fileIcon.className = 'fa fa-file-pdf-o verification-file-icon';
            } else if (file.type === 'application/msword' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
                fileIcon.className = 'fa fa-file-word-o verification-file-icon';
            } else {
                fileIcon.className = 'fa fa-file-o verification-file-icon';
            }
        }
    }

    uploadInput.addEventListener('change', function() {
        const file = uploadInput.files && uploadInput.files[0];
        showFilePreview(file);
    });
    reuploadInput.addEventListener('change', function() {
        const file = reuploadInput.files && reuploadInput.files[0];
        showFilePreview(file);
    });
    deleteBtn.addEventListener('click', function(e) {
        // Prevent form submit if JS is handling
        e.preventDefault();
        // Clear both file inputs
        uploadInput.value = '';
        reuploadInput.value = '';
        showFilePreview(null);
    });
}

// Show/hide and require/unrequire other NGO fields
function setupOtherNgoFields() {
    const ngoSelect = document.getElementById('ngo');
    const otherFields = document.getElementById('other-ngo-fields');
    const otherName = document.getElementById('other_ngo_name');
    const otherEmail = document.getElementById('other_ngo_email');
    if (!ngoSelect || !otherFields || !otherName || !otherEmail) return;
    function toggleOtherFields() {
        if (ngoSelect.value === 'other') {
            otherFields.classList.remove('d-none');
            otherName.required = true;
            otherEmail.required = true;
        } else {
            otherFields.classList.add('d-none');
            otherName.required = false;
            otherEmail.required = false;
        }
    }
    ngoSelect.addEventListener('change', toggleOtherFields);
    // Initialize on page load
    toggleOtherFields();
}

document.addEventListener('DOMContentLoaded', function() {
    setupVerificationFilePreview();
    setupOtherNgoFields();
});

// --- Change Password Form Functions ---
function setupPasswordToggles() {
    const toggleBtns = document.querySelectorAll('.toggle-password');
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = btn.getAttribute('data-target');
            const input = document.getElementById(targetId);
            const icon = btn.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
}

function setupPasswordStrengthMeter() {
    const passwordInput = document.getElementById('id_new_password1');
    const strengthBar = document.getElementById('password-strength-bar');
    const strengthText = document.getElementById('password-strength-text');
    
    if (!passwordInput || !strengthBar || !strengthText) return;
    
    function getPasswordStrength(password) {
        let score = 0;
        if (!password) return 0;
        
        // Length check
        if (password.length >= 8) score++;
        
        // Character type checks
        if (/[A-Z]/.test(password)) score++;
        if (/[a-z]/.test(password)) score++;
        if (/[0-9]/.test(password)) score++;
        if (/[^A-Za-z0-9]/.test(password)) score++;
        
        return score;
    }
    
    function updateStrengthMeter() {
        const val = passwordInput.value;
        const score = getPasswordStrength(val);
        let percent = (score / 5) * 100;
        let color = '#dc3545';
        let text = 'Too weak';
        
        if (score === 1) { 
            color = '#dc3545'; 
            text = 'Very weak'; 
        }
        if (score === 2) { 
            color = '#fd7e14'; 
            text = 'Weak'; 
        }
        if (score === 3) { 
            color = '#ffc107'; 
            text = 'Moderate'; 
        }
        if (score === 4) { 
            color = '#0d6efd'; 
            text = 'Strong'; 
        }
        if (score === 5) { 
            color = '#198754'; 
            text = 'Very strong'; 
        }
        
        strengthBar.style.width = percent + '%';
        strengthBar.style.backgroundColor = color;
        strengthText.textContent = text;
        strengthText.style.color = color;
    }
    
    passwordInput.addEventListener('input', updateStrengthMeter);
    
    // Initialize on page load
    updateStrengthMeter();
}

function setupPasswordConfirmation() {
    const newPasswordInput = document.getElementById('id_new_password1');
    const confirmPasswordInput = document.getElementById('id_new_password2');
    const form = document.getElementById('change-password-form');
    
    if (!newPasswordInput || !confirmPasswordInput || !form) return;
    
    function checkPasswordMatch() {
        const newPassword = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        
        // Remove previous error styling
        confirmPasswordInput.classList.remove('is-invalid');
        confirmPasswordInput.classList.remove('is-valid');
        
        // Remove existing error message
        const existingError = confirmPasswordInput.parentNode.querySelector('.password-match-error');
        if (existingError) {
            existingError.remove();
        }
        
        if (confirmPassword) {
            if (newPassword !== confirmPassword) {
                // Add error styling
                confirmPasswordInput.classList.add('is-invalid');
                confirmPasswordInput.classList.remove('is-valid');
                
                // Create and show error message
                const errorDiv = document.createElement('div');
                errorDiv.className = 'password-match-error invalid-feedback d-block';
                errorDiv.textContent = 'Passwords do not match';
                confirmPasswordInput.parentNode.appendChild(errorDiv);
                
                // Set custom validity for form submission
                confirmPasswordInput.setCustomValidity('Passwords do not match');
            } else {
                // Add success styling
                confirmPasswordInput.classList.add('is-valid');
                confirmPasswordInput.classList.remove('is-invalid');
                
                // Clear custom validity
                confirmPasswordInput.setCustomValidity('');
            }
        } else {
            // No confirmation password entered yet, clear styling
            confirmPasswordInput.classList.remove('is-valid', 'is-invalid');
            confirmPasswordInput.setCustomValidity('');
        }
    }
    
    // Prevent form submission if passwords don't match
    form.addEventListener('submit', function(e) {
        const newPassword = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        
        if (confirmPassword && newPassword !== confirmPassword) {
            e.preventDefault();
            // Ensure error styling is applied
            checkPasswordMatch();
            // Focus on the confirm password field
            confirmPasswordInput.focus();
            return false;
        }
    });
    
    newPasswordInput.addEventListener('input', checkPasswordMatch);
    confirmPasswordInput.addEventListener('input', checkPasswordMatch);
    
    // Also check when new password field loses focus
    newPasswordInput.addEventListener('blur', checkPasswordMatch);
}

// Initialize change password form functionality
document.addEventListener('DOMContentLoaded', function() {
    setupPasswordToggles();
    setupPasswordStrengthMeter();
    setupPasswordConfirmation();
});
