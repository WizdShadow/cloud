document.getElementById('loginform').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    const data = await response.json();
    console.log(data.token);
    if (data.result === true) {
        localStorage.setItem("token", data.token);
        fetch("/profile", {
    headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
});
    }else{
        alert("Неправильный логин или пароль");
    }

});