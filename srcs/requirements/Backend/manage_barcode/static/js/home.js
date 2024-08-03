function check_if_disable(element) {
    if(element.classList.contains('disabled'))
    {
        createToast('warning', 'You need to buy ticket !')
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
  