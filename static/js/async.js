function print(content){
  let div = document.createElement("div")
  div.appendChild(document.createTextNode(content['data']))
  let current_div = document.getElementById('test_async')
  current_div.append(div)
}

async function fetchAsync(url, callback) {
    return await fetch(url)
        .then(response => response.text())
        .then(data => {
        let content = JSON.parse(data)
        // call back after done
        callback(content)
        }
    )
}

async function sendAsync(url, data, callback){
    await fetch(url, {
        method: 'POST', // or 'PUT'
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(data),
    })
    .then(response => response.text())
    .then(data => { 
      let content = JSON.parse(data)
      // call back after done
      callback(content)
    })
    .catch((error) => { 
      console.error('Error:', error)
      console.error('Current Data: ', data)
    });
}
