document.addEventListener("DOMContentLoaded", async() => {
    
    const response = await fetch("/check", {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    })
    const data = await response.json()
    console.log(data);
    if (data.status === true) {
        alert("Вы успешно авторизовались")
    }else{
        window.location.href = "/"
    }
})

document.getElementById("type").addEventListener("click", () => {
    const div = document.querySelector(".type_file")
    div.style.display = "block"
})

function but(e){
    const buts = e.textContent 
    const text = document.getElementById("type")
    text.textContent = buts
    console.log(text.value);
    
}