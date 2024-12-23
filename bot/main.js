async function fetchProductDetails() {
    try {
        const response = await fetch('http://localhost:9000/games');
        const data = await response.json();
        const products = data.games;

        if (!Array.isArray(products)) {
            throw new Error('Expected an array but got something else');
        }

        // Сохраняем данные в глобальную переменную для фильтрации
        window.productsData = products;

        // Отображаем данные без фильтрации по умолчанию
        displayProducts(products);
    } catch (error) {
        console.error('Error fetching product data:', error);
    }
}

function displayProducts(products) {
    const productsListContainer = document.getElementById('products-list');
    productsListContainer.innerHTML = ''; // Очищаем контейнер

    products.forEach(product => {
        const productElement = document.createElement('div');
        productElement.classList.add('product');
        productElement.innerHTML = `
            <div class="product-title">
            <a href="${product.url}">${product.title}</a></div>
            <div class="price">$${product.price}</div>
            <div class="original-price">$${product.original_price}</div>
            <div class="discount-info">${product.discount_info}</div>
            <div class="discount-descriptor">Offer valid until: ${product.discount_descriptor}</div>
        `;
        productsListContainer.appendChild(productElement);
    });
}

// Функция фильтрации товаров по уровню скидки
function filterByDiscount(minDiscount) {
    if (!window.productsData) return;

    const filteredProducts = window.productsData.filter(product => {
        const discountPercentage = calculateDiscountPercentage(product.original_price, product.price);
        return discountPercentage >= minDiscount;
    });

    // Обновляем отображение
    displayProducts(filteredProducts);
}

// Функция для расчета процента скидки
function calculateDiscountPercentage(originalPrice, price) {
    if (!originalPrice || !price || originalPrice <= 0) return 0;
    return ((originalPrice - price) / originalPrice) * 100;
}

// Добавляем обработчик для кнопки фильтрации
document.getElementById('apply-filter').addEventListener('click', () => {
    const minDiscount = parseFloat(document.getElementById('discount-filter').value);
    filterByDiscount(minDiscount);
});

// Загружаем данные при загрузке страницы
window.onload = fetchProductDetails;

