let page = 1;
let itensPerPage = 10;
window.onload = async function(){
    await getUsers()
    localStorage.removeItem("emailToUpdate")
}

async function getUsers(){
    $('#modal-comp').modal({
        show:true,
        backdrop: 'static',
        keyboard: false
    });  
    let url = setUserPagePerPage(page,itensPerPage)
    let res = await fetch(url,{
        method: "GET"
    })
    let json = await res.json()
    $('#modal-comp').modal('hide');
    if(json.results.length > 0)
        makeTable(json.results)
    else{
        window.alert("Você chegou na ultima página")
        page --
    }
}

function makeTable(users){
    const tbody = document.querySelectorAll(".userTbody")
    tbody.forEach(t=>{
        t.remove()
    })
    const pagination = document.querySelector("custom-pagination")
    if(!!pagination){
        pagination.remove()
    }

    let table = document.querySelector("table")
    
    users.forEach(user => {
        let tbodyNew = document.createElement("tbody")
        tbodyNew.setAttribute("class","userTbody")
        
        tbodyNew.innerHTML = `<td scope="row">${user.id}</td>
        <td title="${user.email}" id="email-${user.id}">${user.email}
        </td>
        <td title="${user.role}" id="role-${user.id}">${user.role}
        </td>
        <td style=" width: 128px;">
        <img onclick="updateUser('${user.id}')" 
            class="deleteIcon"
            src="./static/Assets/Icons/edit.svg" style="margin-right:12px;background:#007de3">
        <img onclick="deleteUser('${user.id}')" 
            class="deleteIcon"
            src="./static/Assets/Icons/delete.svg">
        </td>`

        table.appendChild(tbodyNew)
    });
    createPagination()

}
function createPagination(){
    let paginationNew = document.createElement("custom-pagination")
    paginationNew.setAttribute("page",page)
    let contentHolder = document.querySelector(".content-holder")
    contentHolder.appendChild(paginationNew)

    let last = document.querySelector(".last")
    last.remove()
    let first = document.querySelector(".first")
    first.remove()

    let prev = document.querySelector(".prev")
    prev.innerHTML = ""
    let imgPrev = document.createElement("img")
    imgPrev.setAttribute("src", "./static/Assets/Icons/navigate.svg")
    imgPrev.setAttribute("style","transform: rotate(180deg)")
    prev.appendChild(imgPrev)

    let next = document.querySelector(".next")
    next.innerHTML = ""
    let imgNext = document.createElement("img")
    imgNext.setAttribute("src", "./static/Assets/Icons/navigate.svg")
    next.appendChild(imgNext)

}
function updateUser(userId) {
   const email = document.querySelector(`#email-${userId}`).innerHTML
   localStorage.setItem("userToUpdate",JSON.stringify({email:email,id:userId}))
   $('#modal-redirecting').modal({
        show:true,
        backdrop: 'static',
        keyboard: false
    });  
   window.location.href = `/update-user`
   $('#modal-redirecting').modal('hide');
}
async function deleteUser(userId) {
    result = window.confirm("Tem certeza que deseja deletar esse usuário? essa ação não poderá ser desfeita")
    if(result){
        $('#modal-comp').modal({
            show:true,
            backdrop: 'static',
            keyboard: false
        });  
        let url = setUserId(userId)
        let res = await fetch(url,{
            method: "DELETE"
        }).catch(err=>{
            window.alert("Usuário não encontrado")
            $('#modal-comp').modal('hide');
        })
        if(res.status != 200){
            window.alert("Usuário não encontrado")
        }
        else{
            await getUsers()
        }
        $('#modal-comp').modal('hide');
    }
    
}

async function changePage(mode){
    if(page != 1 && mode == "dec") {
        page --
        await getUsers() 
    }
    else if(mode == "inc") {
        page ++
        await getUsers() 
    }

} 