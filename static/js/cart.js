const addToCartForm = document.querySelectorAll('.add-to-cart-form');

addToCartForm.forEach(form => {
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        event.stopPropagation();
        const formData = new FormData(event.target)
        
        const csrftoken = formData.get('csrfmiddlewaretoken');
        const item = formData.get('item');
        const variant = formData.get('variant');
        const modifiers = formData.getAll('modifiers') || [];
        const quantity = formData.get('quantity') || 1;

        const orderItem = {
            item: item,
            variant: variant,
            modifiers: modifiers,
            quantity: quantity
        };

        if (!isLoggedIn) {
            addNewCookieCartItem(orderItem);
        } else {
            const url = `/add_to_cart/${item}`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(orderItem)
            }).then(response => {
                return response.json();
            }).then(data => {
                location.href = '/';
            });
        }
    });
})

function addNewCookieCartItem(orderItem) {
    cart.push(orderItem);
    document.cookie = `cart=${JSON.stringify(cart)};domain=;path=/`;
    location.href = '/';    
}

const updateButtons = document.querySelectorAll('.update-cart');
const csrftoken = document.querySelector('#csrftoken input').value;

updateButtons.forEach(button => {
    button.addEventListener('click', function (event) {
        const index = this.dataset.index;
        const orderItem = this.dataset.item;
        const action = this.dataset.action;
        if (!isLoggedIn) {
            updateCookieCart(index, action)
        } else {
            const url = '/update_cart/';

            const body = {
                'orderItem': orderItem,
                'action': action
            };
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(body)
            }).then(response => {
                return response.json();
            }).then(data => {
                location.reload();
            });
        }
    });
});

function updateCookieCart(index, action) {
    if (index >= cart.length) {
        return;
    }
    if (action === 'add') {
        cart[index].quantity += 1
    } else if (action === 'remove') {
        cart[index].quantity -= 1
        if (cart[index].quantity <= 0) {
            cart.splice(index, 1);
        }
    }
    document.cookie = `cart=${JSON.stringify(cart)};domain=;path=/`;
    location.reload();
}