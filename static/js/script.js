const remoteCheckbox = document.getElementById('remote');
        const autismCheckbox = document.getElementById('autism-level-3-1');

        remoteCheckbox.addEventListener('change', function () {
            if (this.checked == false) {
                autismCheckbox.checked = false;
                autismCheckbox.disabled = true;
                console.log('Autism checkbox was unchecked and disabled');
            } else {
                autismCheckbox.disabled = false;
            }
        });



//okay yg ni untuk toggle preview, kalau tekan dia nanti dia akan display. tapi make sure dh ada checkbox dia punya id dengan preview id dia la
function setupCheckboxPreview(checkboxId, previewId) {
      const checkbox = document.getElementById(checkboxId);
      const preview = document.getElementById(previewId);
      checkbox.addEventListener('change', () => {
        preview.classList.toggle('d-none', !checkbox.checked);
      });
    }
//sokay ni call listing untuk setup checkbox tu
    setupCheckboxPreview('full-time','previewFullTime');
    setupCheckboxPreview('part-time','previewPartTime');
    setupCheckboxPreview('remote','previewRemote');

//okay this one untuk radio button, sama macam function atas tadi, beza dia ni dia ambik name instead of id so lets go little 
//jangan padam ni 
    function setupRadioPreview(radioName, previewId) {
      const radios = document.querySelectorAll(`input[name="${radioName}"]`);
      const preview = document.getElementById(previewId);
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
//these kita call balik function setupRadioPreview tu
    setupRadioPreview('job-category','previewJobCategory')


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
setupSimpleTextareaPreview('jobtitle','previewJobTitle');
setupSimpleTextareaPreview('state','previewState');
setupSimpleTextareaPreview('city','previewCity');
setupSimpleTextareaPreview('min-pay','previewMinSalary');
setupSimpleTextareaPreview('max-pay','previewMaxSalary');
setupSimpleTextareaPreview('question1','previewQuestion1');
setupSimpleTextareaPreview('question2','previewQuestion2');
setupSimpleTextareaPreview('question3','previewQuestion3');
setupSimpleTextareaPreview('maintask','previewMainTaskDesc');

// ✅ Setup checkbox-only preview
setupCheckboxPreview('repetitiveTask', 'previewRepetitiveTask');
setupCheckboxPreview('easyToPerform', 'previewEasyToPerform');
setupCheckboxPreview('easyToRemember', 'previewEasyToRemember');
setupCheckboxPreview('noInterview', 'previewNoInterview');
setupCheckboxPreview('lessNoisy', 'previewLessNoisy');
setupCheckboxPreview('lessStressful', 'previewLessStressful');
setupCheckboxPreview('autism-level-1', 'previewLevel1');
setupCheckboxPreview('autism-level-2', 'previewLevel2');
setupCheckboxPreview('autism-level-3-1', 'previewLevel3');
// ✅ Setup checkbox + textarea preview
setupTextareaTogglePreview('toggleSubtask', 'previewSubTask', 'previewSubTaskDesc', 'subtask', 'subtaskWrapper');
setupTextareaTogglePreview('toggleInteractionWithCustomer', 'previewInteractionWithCustomer', 'previewInteractionWithCustomerDesc', 'interactionWithCustomer', 'interactionWithCustomerWrapper');
setupTextareaTogglePreview('toggleVerbal', 'previewVerbal', 'previewVerbalDesc', 'verbal', 'verbalWrapper');
setupTextareaTogglePreview('toggleNonVerbal', 'previewNonVerbal', 'previewNonVerbalDesc', 'nonverbal', 'nonVerbalWrapper');
setupTextareaTogglePreview('toggleRepresentative', 'previewRepresentative', 'previewRepresentativeDesc', 'representative', 'representativeWrapper');
setupTextareaTogglePreview('toggleSpecialTraining', 'previewSpecialTraining', 'previewSpecialTrainingDesc', 'specialTraining', 'specialTrainingWrapper');
setupTextareaTogglePreview('toggleWorkBuddy', 'previewWorkBuddy', 'previewWorkBuddyDesc', 'workBuddy', 'workBuddyWrapper');
setupTextareaTogglePreview('toggleMentor', 'previewMentor', 'previewMentorDesc', 'mentor', 'mentorWrapper');
setupTextareaTogglePreview('toggleCalmingSpace', 'previewCalmingSpace', 'previewCalmingSpaceDesc', 'calmingSpace', 'calmingSpaceWrapper');
setupTextareaTogglePreview('toggleProgressUpdate', 'previewProgressUpdate', 'previewProgressUpdateDesc', 'progressUpdate', 'progressUpdateWrapper');
setupTextareaTogglePreview('toggleOtherNotes', 'previewOtherNotes', 'previewOtherNotesDesc', 'otherNotes', 'otherNotesWrapper');


// ✅ Setup radio + textarea preview
document.addEventListener("DOMContentLoaded", function () {
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
