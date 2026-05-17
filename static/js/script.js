document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('#navToggle');
    const navLinks = document.querySelector('#navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            const isOpen = navLinks.classList.toggle('open');
        }
        );
    }
});

//Form delete confirmation script - prompts user to confirm before deleting a record

const deleteForms = document.querySelectorAll('.delete-form');

deleteForms.forEach(form => {
    form.addEventListener('submit', (e) => {
        const confirmed = confirm('Are you sure you want to delete this record? This action cannot be undone.');
        if (!confirmed) {
            e.preventDefault();
        }
    });
});

//Filter for assignments page
//Based on - https://www.geeksforgeeks.org/javascript/how-to-create-a-filter-list-using-javascript/ and
//https://css-tricks.com/in-page-filtered-search-with-vanilla-javascript
const assignmentFilter =
    document.querySelector("#assignmentFilter");
const assignmentItems = document.querySelectorAll(".assignment-item");

if (assignmentFilter && assignmentItems.length > 0) {
    assignmentFilter.addEventListener("change", () => {
        const selectedStatus = assignmentFilter.value;

        assignmentItems.forEach((item) => {
            const itemStatus = item.dataset.status;

            if (selectedStatus === "all" || itemStatus === selectedStatus) {

                item.classList.remove("hidden");
            } else {
                item.classList.add("hidden")
            }
        });
    });
}






//Form data validation script - checks required fields before sending to Flask

const validateForms = document.querySelectorAll('form[data-validate="true"]');

validateForms.forEach(form => {
    form.addEventListener('submit', (e) => {
        const requiredFields = form.querySelectorAll("[required]");
        let formisValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                formisValid = false;
                field.classList.add('input-error');
            } else {
                field.classList.remove('input-error');
            }
        });

        if (!formisValid) {
            e.preventDefault();
            alert('Please fill in all required fields.');
        }
    });
});     


//TIMETable script - for popup and prefills

const timetableModal = document.querySelector('#timetableModal')
const openTimetableModal = document.querySelector('#openTimetableModal')
const closeTimetableModal = document.querySelector('#closeTimetableModal')
const cancelTimetableModal = document.querySelector('#cancelTimetableModal')
const calendarSlots = document.querySelectorAll ('.calendar-slot');
const dayInput = document.querySelector('#day_of_week')
const startInput = document.querySelector('#start_time')
const endInput = document.querySelector('#end_time')
const moduleInput = document.querySelector('#module_name')



function showTimetableModal() {
    if (timetableModal) {
    timetableModal.classList.add('open');
    timetableModal.setAttribute('aria-hidden', 'false');

}
    if (moduleInput) {
        moduleInput.focus();
    }
}


function hideTimetableModal() {
    if (timetableModal) {
    timetableModal.classList.remove('open');
    timetableModal.setAttribute('aria-hidden', 'true');

}
}


if (openTimetableModal) {
    openTimetableModal.addEventListener('click', () => {
        showTimetableModal();
    });
}

if (closeTimetableModal) {
    closeTimetableModal.addEventListener('click', hideTimetableModal);
    }


if (cancelTimetableModal) {
    cancelTimetableModal.addEventListener('click', hideTimetableModal);
    }

    calendarSlots.forEach(slot => {
        slot.addEventListener('click', () => {
            if (dayInput && startInput && endInput) {
                dayInput.value = slot.dataset.day;
                startInput.value = slot.dataset.start;
                endInput.value = slot.dataset.end;
        }

        showTimetableModal();
    });
    });

    //Easier user experience on click away

    if (timetableModal) {
        timetableModal.addEventListener('click', (event) => {
        if (event.target === timetableModal) {
            hideTimetableModal();
        }
        });
    }

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            hideTimetableModal();
        }
    });