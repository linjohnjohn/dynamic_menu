console.log('attached')
const addToCartForm = document.querySelectorAll('.add-to-cart-form');

addToCartForm.forEach(form => {
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        event.stopPropagation();
        const formData = new FormData(event.target)
        
        const item = formData.get('item');
        const variant = formData.get('variant');
        const modifiers = formData.getAll('modifiers') || [];
        const quantity = formData.get('quantity') || 1;

        const orderItem = {
            item: item,
            variant: variant,
            modifiers: modifiers,
            quantity: 1
        };

        addNewCookieCartItem(orderItem);
    });
})
function addNewCookieCartItem(orderItem) {
    cart.push(orderItem);
    document.cookie = `cart=${JSON.stringify(cart)};domain=;path=/`;
    location.href = '/menu';    
}

function updateCookieCart(orderItemNum, action) {
    if (cart.length > orderItemNum) {
        return;
    }
    if (action === 'add') {
        cart[orderItemNum].quantity += 1
    } else if (action === 'remove') {
        cart[orderItemNum].quantity -= 1
        if (cart[orderItemNum].quantity <= 0) {
            cart.splice(orderItemNum, 1);
        }
    }
    document.cookie = `cart=${JSON.stringify(cart)};domain=;path=/`;
    location.reload();
}