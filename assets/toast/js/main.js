function toast({title = '', message = '', type = 'info', duration = 3000}) {
    const main = document.getElementById('toast')
    if (main) {
        const toast = document.createElement('div');
        const icons = {
            success: 'bx bx-check-circle',
            info: 'bx bx-info-circle',
            error: 'bx bx-error-circle',
        };

        const autoRemoveId = setTimeout(function () {
            main.removeChild(toast);
        }, duration + 1000)

        toast.onclick = function (e) {
            if (e.target.closest('.toast__close')) {
                main.removeChild(toast);
                clearTimeout(autoRemoveId);
            }
        }
        const icon = icons[type];
        const delay = (duration / 1000).toFixed(2);

        toast.classList.add('toast', `toast--${type}`);
        toast.style.animation = `slideInLeft ease 1s, fadeOut linear 1s ${delay}s forwards`;
        toast.innerHTML = `<div class="toast__icon">
                            <i class="${icon}"></i>
                        </div>
                        <div class="toast__body">
                            <h3 class="toast__title">${title}</h3>
                            <p class="toast__msg">${message}</p>
                        </div>
                        <div class="toast__close">
                            <i class='bx bx-x-circle'></i>
                        </div>
                `;
        main.appendChild(toast);


    }
}


function showSuccessToastAddProDuct() {
    toast({
        title: 'Thêm thành công',
        message: 'Sản phẩm của bạn đã được thêm vào <a style="font-size: 2rem; line-height: 1.2em;" href="http://127.0.0.1:8000/basket">vỏ hàng</a>, mua tiếp <a style="font-size: 2rem; line-height: 1.2em;" href="http://127.0.0.1:8000/product/">tại đây</a>',
        type: 'success',
        duration: 5000
    })
}
function showSuccessToastEditProDuct() {
    toast({
        title: 'Thông báo',
        message: "Sản phẩm của bạn đã tồn tại trong vỏ hàng và được sửa đổi số lượng",
        type: 'success',
        duration: 3000
    })
}

function showSuccessToastLoadProDuct() {
    toast({
        title: 'Hoạt động',
        message: 'Đang xử lí ...',
        type: 'info',
        duration: 1000000
    })
}

function showSuccessToastUpdatePro() {
    toast({
        title: 'Thành công',
        message: 'Bạn đã chỉnh sửa sản phẩm thành công',
        type: 'success',
        duration: 3000

    })
}

function showSuccessToastDeletePro(){
    toast({
        title: 'Thành công',
        message: 'Bạn đã chỉnh xóa sản phẩm thành công',
        type: 'success',
        duration: 3000

    })
}

function showInfoToast() {
    toast({
        title: 'Thông báo',
        message: 'Bạn đã đăng kí thành công',
        type: 'info',
        duration: 5000

    })
}

function showErrorToast() {
    toast({
        title: 'Thất bại',
        message: 'Vui lòng liên hệ sau',
        type: 'error',
        duration: 5000

    })
}
