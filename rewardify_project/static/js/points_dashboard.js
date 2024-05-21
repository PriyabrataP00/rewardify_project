// points_dashboard.js

document.addEventListener("DOMContentLoaded", function() {
    const categoryPoints = JSON.parse(document.getElementById('categoryLabels').textContent);
    const categoryData = JSON.parse(document.getElementById('categoryData').textContent);

    const subCategoryPoints = JSON.parse(document.getElementById('subCategoryLabels').textContent);
    const subCategoryData = JSON.parse(document.getElementById('subCategoryData').textContent);

    const categoryLabels = categoryPoints.map(cp => cp.app__app_category__name);
    const categoryValues = categoryPoints.map(cp => cp.total);

    const subCategoryLabels = subCategoryPoints.map(scp => scp.app__sub_category__name);
    const subCategoryValues = subCategoryPoints.map(scp => scp.total);

    const categoryConfig = {
        type: 'bar',
        data: {
            labels: categoryLabels,
            datasets: [{
                label: 'Points by Category',
                data: categoryValues,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    const subCategoryConfig = {
        type: 'bar',
        data: {
            labels: subCategoryLabels,
            datasets: [{
                label: 'Points by SubCategory',
                data: subCategoryValues,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    const categoryChartCtx = document.getElementById('category-points-chart').getContext('2d');
    const subCategoryChartCtx = document.getElementById('subcategory-points-chart').getContext('2d');

    const categoryChart = new Chart(categoryChartCtx, categoryConfig);
    const subCategoryChart = new Chart(subCategoryChartCtx, subCategoryConfig);
});
