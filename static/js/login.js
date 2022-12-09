var applicationBody

window.onload = function(){
    applicationBody = animationLoadFunction(applicationBody)
    document.cookie= "token="
}

async function login(){
    let body = formatBody()
    let url = "http://localhost:5000/api/v1/login"
    let response = await fetch(url,{
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body:body
    }).catch(err=>{
        console.error(err)
        window.alert("Usuário e/ou senha inválidos")
    })
    if(response.status != 200)
        window.alert("Usuário e/ou senha inválidos")
    else{
        let json = await response.json()
        if(!!json){
            sessionStorage.setItem("token",json.token)
            document.cookie = "token="+json.token
            window.location.href = "/"
        }
        else{
            window.alert("Usuário e/ou senha inválidos")
        }
    }

}

function formatBody(){
    let user = document.querySelector("#loginUserInput").value
    let password = document.querySelector("#loginPasswordInput").value
    return JSON.stringify({
        "user":user,
        "password":password
    })
}

// async function auth(){
//     let url = "http://localhost:5000/api/v1/authenticate"
//     let token = sessionStorage.getItem("token")
//     if(!!token){
//         let response = await fetch(url,{
//             method: "POST",
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body:JSON.stringify({"token":token})
//         }).then(response=>{
//             if(response.status == 401)
//                 window.location.href = "login"
//         }).catch(err=>{
//             window.location.href = "login"
//         })
//     }
//     else{
//         window.location.href = "login"
//     }
// }