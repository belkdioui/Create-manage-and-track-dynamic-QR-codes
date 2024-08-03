
const toastDetails = {
    timer: 10000,
    success: {
        icon: 'bi-check-circle',
    },
    error: {
        icon: 'bi bi-x-circle',
    },
    warning: {
        icon: 'bi-exclamation-triangle',
    },
    info: {
        icon: 'fa-circle-info',
    }
}

const removeToast = (toast) => {
    toast.classList.add("hide");
    if(toast.timeoutId) clearTimeout(toast.timeoutId);
    setTimeout(() => toast.remove(), 10000);
}

const createToast = (id, text) => {
    const { icon } = toastDetails[id];
    const toast = document.createElement("li");
    toast.className = `toast_1 ${id}`;
    toast.innerHTML = `<div class="column">
                         <i class="${icon}"></i>
                         <span>${text}</span>
                         <i class="" onclick="removeToast(this.parentElement)"></i>
                      </div>
                        `;
                
    const notifications = document.querySelector(".notifications");
    console.log(notifications)
    notifications.appendChild(toast);
    toast.timeoutId = setTimeout(() => removeToast(toast), toastDetails.timer);
}

// buttons.forEach(btn => {
//     btn.addEventListener("click", () => createToast(btn.id, "herere"));
// });