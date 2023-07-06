let navbar = document.querySelector('.navbar');
document.querySelector('#menu-btn').addEventListener('click', () => {
    document.querySelector('#menu-btn').classList.toggle('fa-times');
    navbar.classList.toggle('active');
})

window.onscroll = () =>{
    document.querySelector('#menu-btn').classList.remove('fa-times');
    navbar.classList.remove('active');
}
