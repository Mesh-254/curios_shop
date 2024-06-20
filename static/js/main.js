document.addEventListener('DOMContentLoaded', function () {
    const menuIcon = document.getElementById('menu-icon');
    const dropdown = document.querySelector('.dropdown');

    menuIcon.addEventListener('click', function () {
        menuIcon.classList.toggle('active');
        dropdown.classList.toggle('show');
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const para = ['As a freelance writer with three teenagers at home, I really needed a quiet space to get\n' +
    '                                work done. Belonging to Jokamu CyberTech cafe lets me focus on my writing in a\n' +
    '                                productive, creative\n' +
    '                                atmosphere.', 'Jokamu offers everything you can think of when working with computers or searching for\n' +
    '                                something on the Internet. From the friendly &amp; cozy atmosphere to fast Internet,\n' +
    '                                there are lots of things that make this Cybercafe my #1 go-to place.', 'This internet cafe is a great place just to browse the Web with my\n' +
    '                                friends. Not all of us have high-speed Internet connection and that’s why Jokamu\n' +
    '                                CyberTech cafe is\n' +
    '                                the place for us. They also have the best services in the town'];
    const quotes = document.getElementsByClassName('quote-text');
    // for (let x in para) {
    //     setInterval(() =>{
    //
    //     }, 1000);
    // }
});