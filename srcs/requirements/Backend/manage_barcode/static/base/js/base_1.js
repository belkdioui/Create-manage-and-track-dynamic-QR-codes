
const toastDetails = {
    timer: 5000,
    success: {
        icon: 'bi-check-circle-fill',
    },
    error: {
        icon: 'bi-x-circle-fill',
    },
    warning: {
        icon: 'bi-exclamation-triangle-fill',
    },
}

const removeToast = (toast) => {
    toast.classList.add("hide");
    if(toast.timeoutId) clearTimeout(toast.timeoutId);
    setTimeout(() => toast.remove(), 1000);
}

const createToast = (id, text) => {
    const { icon } = toastDetails[id];
    const toast = document.createElement("li");
    toast.className = `toast_1 ${id}`;
    toast.innerHTML = `<div class="column">
                         <i class="${icon}"></i>
                         <span>${text}</span>
                        </div>
                         <i class="bi-x-lg" onclick="removeToast(this.parentElement)"></i>
                        `;
                
    const notifications = document.querySelector(".notifications");
    notifications.appendChild(toast);
    toast.timeoutId = setTimeout(() => removeToast(toast), toastDetails.timer);
}

// buttons.forEach(btn => {
//     btn.addEventListener("click", () => createToast(btn.id, "herere"));
// });