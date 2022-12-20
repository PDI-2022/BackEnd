let page = 1;
let itensPerPage = 10;
window.onload = async function(){
    await auth()
    await getModels()
}

async function getModels(){
    $('#modal-comp').modal({
        show:true,
        backdrop: 'static',
        keyboard: false
    });  
    let url = setModelPagePerPage(page,itensPerPage)
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

function makeTable(models){
    const tbody = document.querySelectorAll(".modelTbody")
    tbody.forEach(t=>{
        t.remove()
    })
    const pagination = document.querySelector("custom-pagination")
    if(!!pagination){
        pagination.remove()
    }

    let table = document.querySelector("table")
    
    models.forEach(model => {
        let tbodyNew = document.createElement("tbody")
        tbodyNew.setAttribute("class","modelTbody")
        
        tbodyNew.innerHTML = `<td scope="row">${model.id}</td>
        <td title="${model.name}">${model.name}
        <td title="${model.description}">${model.description}
        </td>
        ${model.id != 1 ? 
            `<td>
                <img onclick="deleteModel('${model.id}')" 
                    class="deleteIcon"
                    src="./static/Assets/Icons/delete.svg">
            </td>`
            :   
            `<td>
            </td>`}
        `

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

async function deleteModel(modelId) {
    result = window.confirm("Tem certeza que deseja deletar esse modelo? essa ação não poderá ser desfeita")
    if(result){
        $('#modal-comp').modal({
            show:true,
            backdrop: 'static',
            keyboard: false
        });  
        let url = setModelId(modelId)
        let res = await fetch(url,{
            method: "DELETE"
        }).catch(err=>{
            window.alert("Modelo não encontrado")
            $('#modal-comp').modal('hide');
        })
        if(res.status != 200){
            window.alert("Modelo não encontrado")
        }
        else{
            await getModels()
        }
        $('#modal-comp').modal('hide');
    }

}

async function changePage(mode){
    if(page != 1 && mode == "dec") {
        page --
        await getModels() 
    }
    else if(mode == "inc") {
        page ++
        await getModels() 
    }
} 