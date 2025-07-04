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

  updatePreview();
}




// ✅ Setup checkbox-only preview
setupCheckboxPreview('repetitiveTask', 'previewRepetitiveTask');
setupCheckboxPreview('easyToPerform', 'previewEasyToPerform');
setupCheckboxPreview('easyToRemember', 'previewEasyToRemember');
setupCheckboxPreview('noInterview', 'previewNoInterview');
setupCheckboxPreview('lessNoisy', 'previewLessNoisy');
setupCheckboxPreview('lessStressful', 'previewLessStressful');

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

