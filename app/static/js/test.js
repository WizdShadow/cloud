async function updateFunc(){
    const token = localStorage.getItem("token")
    const l = document.querySelector(".l")
    const R = document.querySelector(".R")
    const username = document.querySelector(".user_name")
    if (token){
        token_new = token.split(".")[1]
        const name = atob(token_new)
        const news = name.replace(/\\/g, "")
        const obj = JSON.parse(news)
        console.log(obj.username);
        l.style.display = "none"
        R.style.display = "none"
        username.style.display = "block"
        username.textContent = obj.username

    }
    
}

document.querySelector(".l").addEventListener("click", () => {
    const div = document.querySelector(".d4")
    const overlay = document.querySelector(".overlay")
    div.style.display = "block"
    overlay.style.display = "block"
})

document.addEventListener("DOMContentLoaded", () =>{
    document.getElementById("login").value = ""
})

document.addEventListener("DOMContentLoaded", () =>{
    document.getElementById("password").value = ""
})

document.addEventListener("DOMContentLoaded", () =>{
    updateFunc()
})

document.addEventListener("click", event => {
    const overlay = document.querySelector(".overlay")
    const div = document.querySelector(".d4")

    if (overlay.contains(event.target)) {
        console.log("вы кликнули на overlay");
        overlay.style.display = "none"
        div.style.display = "none"
    }
});

document.querySelector(".log_button").addEventListener("click", async () => {
    const login = document.getElementById("login").value
    const password = document.getElementById("password").value
    const err = document.getElementById("error")
    const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: login,
                password: password
            })
        });
    
    const data = await response.json()
    if (data.result === false) {
        err.style.display = "block"
    }else{
        localStorage.setItem("token", data.token)
        console.log(localStorage.getItem("token"))
        await updateFunc()

    }
    
})
