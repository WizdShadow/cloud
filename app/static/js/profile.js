document.addEventListener("DOMContentLoaded", async() => {
    
    const response = await fetch("/check", {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    })
    const data = response.json()
    console.log(data);
    if (data.status === true) {
        alert("Вы успешно авторизовались")
    }else{
        window.location.href = "/"
    }
})