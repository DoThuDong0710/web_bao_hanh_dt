let navbar = document.querySelector('.navbar');
let searchForm = document.querySelector('.search-form');
let cartItem = document.querySelector('.cart-items-container');
let addoptions = document.querySelector('.add-options-container');

// Gán sự kiện click cho nút menu-btn
document.querySelector('#menu-btn').onclick = () =>{
    navbar.classList.toggle('active');
    // Đảm bảo các phần tử còn lại không có class active
    searchForm.classList.remove('active');
    cartItem.classList.remove('active');
    addoptions.classList.remove('active');
}

// Gán sự kiện click cho nút search-btn
document.querySelector('#search-btn').onclick = () =>{
    searchForm.classList.toggle('active');
    navbar.classList.remove('active');
    cartItem.classList.remove('active');
    addoptions.classList.remove('active');
}

document.querySelector('#add-btn').onclick = () =>{
    addoptions.classList.toggle('active');
    searchForm.classList.remove('active');
    navbar.classList.remove('active');
    cartItem.classList.remove('active');
}

// Gán sự kiện click cho nút settings-btn
document.querySelector('#settings-btn').onclick = () =>{
    cartItem.classList.toggle('active');
    navbar.classList.remove('active');
    searchForm.classList.remove('active');
    addoptions.classList.remove('active');
}

// Gán sự kiện scroll cho cửa sổ
window.onscroll = () =>{
    // Đảm bảo khi cuộn trang, không có phần tử nào có class active
    navbar.classList.remove('active');
    searchForm.classList.remove('active');
    cartItem.classList.remove('active');
    addoptions.classList.remove('active');
}