// =====================================================
// ONLINE ATTENDANCE MANAGEMENT SYSTEM
// JavaScript
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    console.log(
        "Online Attendance Management System loaded."
    );


    // Password show/hide
    const password =
        document.getElementById("password");

    const togglePassword =
        document.getElementById("togglePassword");


    if (password && togglePassword) {

        togglePassword.addEventListener(
            "click",
            function () {

                if (password.type === "password") {

                    password.type = "text";

                    togglePassword.textContent = "Hide";

                } else {

                    password.type = "password";

                    togglePassword.textContent = "Show";
                }

            }
        );

    }


    // Faculty attendance form
    const attendanceForm =
        document.getElementById("attendanceForm");


    if (attendanceForm) {

        attendanceForm.addEventListener(
            "submit",
            function (event) {

                const student =
                    document.getElementById("student");

                const subject =
                    document.getElementById("subject");

                const classNumber =
                    document.getElementById("class_number");

                const status =
                    document.getElementById("status");


                if (!student.value) {

                    alert("Please select a student.");

                    event.preventDefault();

                    return;
                }


                if (!subject.value.trim()) {

                    alert("Please enter the subject.");

                    event.preventDefault();

                    return;
                }


                if (
                    !classNumber.value ||
                    classNumber.value < 1
                ) {

                    alert(
                        "Please enter a valid class number."
                    );

                    event.preventDefault();

                    return;
                }


                const confirmSave = confirm(
                    "Save attendance?\n\n" +
                    "Student: " +
                    student.value +
                    "\n" +
                    "Subject: " +
                    subject.value +
                    "\n" +
                    "Class: " +
                    classNumber.value +
                    "\n" +
                    "Status: " +
                    status.value
                );


                if (!confirmSave) {

                    event.preventDefault();

                }

            }
        );

    }


    // Logout confirmation
    const logoutButtons =
        document.querySelectorAll(".logout-button");


    logoutButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function (event) {

                const confirmLogout =
                    confirm(
                        "Are you sure you want to logout?"
                    );


                if (!confirmLogout) {

                    event.preventDefault();

                }

            }
        );

    });


    // Automatically hide messages
    setTimeout(function () {

        const messages =
            document.querySelectorAll(
                ".success-message, .error-message"
            );


        messages.forEach(function (message) {

            message.style.transition =
                "opacity 0.5s ease";

            message.style.opacity = "0";


            setTimeout(function () {

                message.style.display = "none";

            }, 500);

        });

    }, 5000);

});