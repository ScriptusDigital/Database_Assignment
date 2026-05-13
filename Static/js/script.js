document.addEventListener ('DOMContentLoaded', () => {
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

//Filter for assignments
//Based on - https://www.geeksforgeeks.org/javascript/how-to-create-a-filter-list-using-javascript/
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