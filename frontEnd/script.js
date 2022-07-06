document.getElementById('formData').addEventListener('submit', retrieveName)

function retrieveName(e) {
    e.preventDefault()

    let name = document.getElementById('name').value

    fetch(`http://localhost:5000/${name}`)
        .then((res) => res.json())
        .then((data) => {
            document.getElementById('output').innerHTML = `<li class="list-group-item">Name : ${data.name} price : ${data.price} Quantity : ${data.quantity}</li>`
        })
}

document.getElementById('postData').addEventListener('submit', postData)

function postData(e) {
    e.preventDefault()

    let name = document.getElementById('postName').value
    let price = document.getElementById('postPrice').value
    let quantity = document.getElementById('postQuantity').value

    fetch('http://localhost:5000/postData', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': name,
            'price': price,
            'quantity': quantity
        })
    })
        .then((response) => response.json())
        .then((data) => console.log(data))
}