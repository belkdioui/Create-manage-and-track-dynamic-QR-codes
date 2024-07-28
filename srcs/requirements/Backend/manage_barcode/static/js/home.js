function check_if_disable(element) {
    if(element.classList.contains('disabled'))
    {
        const iconContainer = element.previousElementSibling;
    
        if (!iconContainer || !iconContainer.classList.contains('icon_if_disable')) {
        console.log('Icon container not found next to the element.');
        return;
        }
    
        let icon = null;
        let existingIcon = iconContainer.querySelector('.bi-caret-up-fill');
        if (!existingIcon) {
        icon = document.createElement('i');
        icon.className = 'bi bi-caret-up-fill';
        iconContainer.appendChild(icon);
        } 
    
        setTimeout(() => {
        if (icon && iconContainer.contains(icon)) {
            iconContainer.removeChild(icon);
        }
        }, 2000);
    }
    else{
        let card = document.querySelector('.card-img-top');
        let btn = document.querySelector('.btn');
        if(card.style.filter != 'none'){
            card.style.filter = 'none';
            setTimeout(() => {
                    card.style.filter = 'blur(14px)';
                    btn.blur();
                }, 10000);
        }

    }
  }
  