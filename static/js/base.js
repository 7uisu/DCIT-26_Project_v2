//Navbar
document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.querySelector(".dropdown");
    const dropdownContent = document.querySelector(".dropdown-content");

    dropdown.addEventListener("mouseenter", function () {
        dropdownContent.style.display = "block";
    });

    dropdown.addEventListener("mouseleave", function () {
        dropdownContent.style.display = "none";
    });
});


//home.html services section
document.addEventListener("DOMContentLoaded", function () {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const categorySections = document.querySelectorAll('.service-category-section');

    tabButtons.forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = this.getAttribute('data-category-id');

            // Hide all category sections
            categorySections.forEach(section => section.classList.add('hidden'));

            // Show the selected category section
            const activeSection = document.getElementById('category-' + categoryId);
            if (activeSection) {
                activeSection.classList.remove('hidden');
            }

            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
});

//home.html services Testimonials Carousel
    document.addEventListener('DOMContentLoaded', function () {
        // Get all testimonial items and buttons
        const testimonialItems = document.querySelectorAll('.testimonial-item');
        const prevButton = document.querySelector('.testimonial-prev-btn');
        const nextButton = document.querySelector('.testimonial-next-btn');

        let currentIndex = 0;

        // Set the first testimonial as active
        testimonialItems[currentIndex].classList.add('active');

        // Show the next testimonial when the next button is clicked
        nextButton.addEventListener('click', function () {
            // Remove 'active' class from current testimonial
            testimonialItems[currentIndex].classList.remove('active');

            // Move to the next testimonial
            currentIndex = (currentIndex + 1) % testimonialItems.length;

            // Add 'active' class to the next testimonial
            testimonialItems[currentIndex].classList.add('active');
        });

        // Show the previous testimonial when the previous button is clicked
        prevButton.addEventListener('click', function () {
            // Remove 'active' class from current testimonial
            testimonialItems[currentIndex].classList.remove('active');

            // Move to the previous testimonial
            currentIndex = (currentIndex - 1 + testimonialItems.length) % testimonialItems.length;

            // Add 'active' class to the previous testimonial
            testimonialItems[currentIndex].classList.add('active');
        });
    });


    function previewImage(event) {
        const input = event.target;
        const preview = document.getElementById('profile-preview');

        if (input.files && input.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
            };

            reader.readAsDataURL(input.files[0]);
        }
    }

// For the About Section Image movement
document.addEventListener("DOMContentLoaded", function() {
    // Hide loader and show content once the page is fully loaded
    window.addEventListener("load", function() {
        var loaderWrapper = document.getElementById("loader-wrapper");
        loaderWrapper.style.display = "none";

        var content = document.getElementById("content");
        content.style.display = "block";
    });
});
document.addEventListener("DOMContentLoaded", function () {
    // Correct the class selector to match the elements
    const tabs = document.querySelectorAll(".service-list-page-tab-btn");
    const sections = document.querySelectorAll(".service-list-page-category-section");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove("active"));
            // Add active class to clicked tab
            tab.classList.add("active");

            // Hide all sections
            sections.forEach(section => section.classList.add("hidden"));
            // Show the selected category section
            const activeSection = document.getElementById(`category-${tab.dataset.categoryId}`);
            if (activeSection) {
                activeSection.classList.remove("hidden");
            }
        });
    });
});

document.querySelector('.sidebar').addEventListener('mouseenter', function() {
    this.style.width = '250px'; // Expand sidebar
    document.querySelector('.sidebar-logo img').style.width = '120px'; // Expand logo

    // Show text inside sidebar items
    document.querySelectorAll('.sidebar-item span').forEach(span => {
        span.style.display = 'inline';
    });
});

document.querySelector('.sidebar').addEventListener('mouseleave', function() {
    this.style.width = '70px'; // Collapse sidebar
    document.querySelector('.sidebar-logo img').style.width = '40px'; // Shrink logo

    // Hide text inside sidebar items
    document.querySelectorAll('.sidebar-item span').forEach(span => {
        span.style.display = 'none';
    });
});
