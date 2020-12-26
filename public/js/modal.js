var modalBtn = document.querySelector('.modal-btn')
var modalBg = document.querySelector('.modal-bg')
var modalClose = document.querySelector('.modal-close')

function showModal(val){
    modalBg.classList.add('bg-active');
    $("#modal-content").attr('src', '/-/view/' + val)
};

modalClose.addEventListener('click', function() {
    modalBg.classList.remove('bg-active');
});