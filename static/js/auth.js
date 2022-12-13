async function auth(){
    let url = "http://localhost:5000/api/v1/authenticate"
    let token = sessionStorage.getItem("token")
    if(!!token){
        await fetch(url,{
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body:JSON.stringify({"token":token})
        }).then(response=>{
            if(!(response.status == 200))
                window.location.href = "login"
        }).catch(err=>{
            window.location.href = "login"
        })
    }
    else{
        window.location.href = "login"
    }
}
function logout(){
    sessionStorage.clear()
    window.location.href = "login"
}