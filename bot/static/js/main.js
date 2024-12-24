async function fetchProductDetails() {
    try {
        const response = await fetch('/games');
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

        // Основная разметка продукта
        productElement.innerHTML = `
            <div class="product-title">${product.title}</div>
            <div class="price">${product.price} TL</div>
            <div class="original-price">${product.original_price} TL</div>
            <div class="discount-info">${product.discount_info}</div>
            <div class="discount-descriptor">
                <button class="show-link-btn">Show More</button>
            </div>
            <div class="product-link" style="display: none;">
                <a href="${product.url}" target="_blank">View Product</a>
                <div class="discount-end-date">Discount ends: ${product.discount_descriptor}</div>
            </div>
        `;

        // Добавляем элемент в список
        productsListContainer.appendChild(productElement);
    });

    // Добавляем обработчики событий для кнопок "Show More"
    const showLinkButtons = document.querySelectorAll('.show-link-btn');
    showLinkButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            const productLink = document.querySelectorAll('.product-link')[index];

            // Переключение отображения ссылки и кнопки
            if (productLink.style.display === 'none') {
                productLink.style.display = 'block';
                button.textContent = 'Show Less';
            } else {
                productLink.style.display = 'none';
                button.textContent = 'Show More';
            }
        });
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

