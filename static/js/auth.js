async function auth(){
    let url = "http://localhost:5000/api/v1/authenticate"
    let token = sessionStorage.getItem("token")
    if(!!token){
        let response = await fetch(url,{
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