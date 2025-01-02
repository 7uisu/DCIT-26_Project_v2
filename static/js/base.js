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
