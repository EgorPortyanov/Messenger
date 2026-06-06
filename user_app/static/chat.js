const openBtn = document.getElementById('openModalBtn');
const closeBtn = document.getElementById('closeModalBtn');
const cancelBtn = document.getElementById('cancelModalBtn');
const cover = document.getElementById('cover');

if (openBtn) {
    openBtn.addEventListener('click', () => {
        cover.style.display = 'flex';
    });
}

if (closeBtn) {
    closeBtn.addEventListener('click', () => {
        cover.style.display = 'none';
    });
}

if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
        cover.style.display = 'none';
    });
}

if (cover) {
    cover.addEventListener('click', (event) => {
        if (event.target === cover) {
            cover.style.display = 'none';
        }
    });
}


const deleteBtn = document.querySelector('.icon-btn');
const deleteCover = document.getElementById('deleteCover');
const closeDeleteModalBtn = document.getElementById('closeDeleteModalBtn');
const cancelDeleteModalBtn = document.getElementById('cancelDeleteModalBtn');

if (deleteBtn) {
    deleteBtn.addEventListener('click', (event) => {
        event.preventDefault();
        deleteCover.style.display = 'flex';
    });
}

if (closeDeleteModalBtn) {
    closeDeleteModalBtn.addEventListener('click', () => {
        deleteCover.style.display = 'none';
    });
}

if (cancelDeleteModalBtn) {
    cancelDeleteModalBtn.addEventListener('click', () => {
        deleteCover.style.display = 'none';
    });
}

if (deleteCover) {
    deleteCover.addEventListener('click', (event) => {
        if (event.target === deleteCover) {
            deleteCover.style.display = 'none';
        }
    });
}