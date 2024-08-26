document.addEventListener('DOMContentLoaded', function () {
    var links = document.querySelectorAll('.nav-link');
    links.forEach(function(link) {
        link.addEventListener('click', function() {
            links.forEach(function(link) {
                link.parentElement.classList.remove('active');
            });
            this.parentElement.classList.add('active');
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const filterStudent = document.getElementById('filterStudent');
    const filterAdmin = document.getElementById('filterAdmin');
    const filterProfessor = document.getElementById('filterProfessor');
    const accountRows = document.querySelectorAll('.accountRow');

    function updateVisibility() {
        accountRows.forEach(row => {
            const isStudent = row.classList.contains('student');
            const isAdmin = row.classList.contains('admin');
            const isProfessor = row.classList.contains('professor');

            if ((filterStudent.checked && isStudent) ||
                (filterAdmin.checked && isAdmin) ||
                (filterProfessor.checked && isProfessor)) {
                row.style.display = 'table-row';
            } else {
                row.style.display = 'none';
            }
        });

        if (!filterStudent.checked && !filterAdmin.checked && !filterProfessor.checked) {
            accountRows.forEach(row => {
                row.style.display = 'table-row';
            });
        }
    }

    filterStudent.addEventListener('change', updateVisibility);
    filterAdmin.addEventListener('change', updateVisibility);
    filterProfessor.addEventListener('change', updateVisibility);

    updateVisibility();
});


 function toggleStudentFields() {
        var studentType = document.getElementById('student_type').value;
        var studentNumberField = document.getElementById('student_number_field');
        var yearLevelField = document.getElementById('year_level_field');
        var semesterField = document.getElementById('semester_field');

        if (studentType === 'old') {
            studentNumberField.style.display = 'block';
            yearLevelField.style.display = 'block';
            semesterField.style.display = 'block';
        } else {
            studentNumberField.style.display = 'none';
            yearLevelField.style.display = 'none';
            semesterField.style.display = 'none';
        }
    }