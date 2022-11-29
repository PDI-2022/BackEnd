var csv
var arrayCsv = []

const state = {
    page: 1,
    perPage: 5,
    totalPages: 100
}

const html = {
    get(element) {
        return document.querySelector(element)
    }
}

async function paginacao () {
    let json = {
        "page": state.page,
        "itensPerPage": state.perPage
    }
    const url = new String("http://127.0.0.1:5000/api/v1/process/pagination");
    const Img = await fetch(url, {
        method:"POST", 
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(json)
    }).catch(err=>{
        console.error(err)
    })

    const response = await Img.json()
    response["externSeeds"]
    generateTable(response["externSeeds"],response["internSeeds"])
}

window.onload = async function(){
    if(localStorage.getItem("csv") == '' || !localStorage.getItem("csv"))
        window.location.href="/"
    
    else{
        await paginacao ()
    }
}

function generateTable(externSeeds,internSeeds) {
    arrayCsv = []

    const mainFooter = document.getElementsByTagName("footer")[0]
    const body = document.getElementsByTagName("body")[0]

    csv = localStorage.getItem("csv")
    var array = csv.split("\n")

    for(let i = 0; i < array.length; i++){
        arrayCsv.push(array[i].split(",")) 
    }
    
    clearScreenElement(body,mainFooter)
    let imgsContainer = fillTable(externSeeds,internSeeds,arrayCsv)

    for(let i = 0; i < imgsContainer.length; i++){
        body.appendChild(imgsContainer[i])
    }

    if(!document.getElementsByTagName("download-section")[0]){
        let pagination = document.createElement("custom-pagination")
        pagination.setAttribute("page",state.page)
        body.appendChild(pagination)
        let download = document.createElement("download-section");
        download.setAttribute("id","download-sectio+n")
        download.setAttribute("class","downloadButtonSection")
        body.appendChild(download)
    }

    body.appendChild(mainFooter)
    
}

async function changePage(action){
    let maxItem = arrayCsv.length - 2
    state.totalPages = maxItem / (2*state.perPage)

    switch (action){
        case 'inc':
            if(state.page != state.totalPages){
                state.page = state.page + 1
                await paginacao()
            }
            break;
        case 'dec':
            if(state.page > 1){
                state.page = state.page - 1
                await paginacao()
            }
            break
        case 'last':
            if(state.page != state.totalPages){
                state.page = state.totalPages
                await paginacao()
            }
            break;
        case 'first':
            if(state.page > 1){
                state.page = 1
                await paginacao()
            }
            break;
        default:
            break;
    }
}


function clearScreenElement(body,mainFooter){
    const mainNav = document.getElementsByTagName("header")[0]
    let imgContainer = document.querySelectorAll(".imgs-container")
    if(imgContainer.length > 0){
        imgContainer.forEach(img=>{
            body.removeChild(img)
        })
        let downloadSection = document.querySelector("download-section")
        body.removeChild(downloadSection)
        let pag = document.querySelector("custom-pagination")
        body.removeChild(pag)
    }

    body.appendChild(mainNav)
    mainFooter.remove()
}

function fillTable(externSeeds,internSeeds,arrayCsv){
    const initialValue = (((2*state.perPage)*(state.page-1))+1)
    const finalValue = ((state.perPage*state.page)+1)

    let hasClass = localStorage.getItem("hasClass")
    let maxNumberOffColumns = hasClass == "true" ? 9 : 8
    

    let imgsContainer = []

    for(let i=1;i<=internSeeds.length;i++){
        imgsContainer.push(makeTable(internSeeds[i-1], (initialValue+(2*i)-2), maxNumberOffColumns))
        imgsContainer.push(makeTable(externSeeds[i-1], (initialValue+(2*i)-1), maxNumberOffColumns))
    }

    return imgsContainer
}

function goBack(){
    window.location.href = "/"
}

function returnHome(){
    goBack()
}

function downloadCsv() {
    const csvString = csv;
    var blob = new Blob([csvString], { type: 'text/plain;charset=utf-8;' });
    var link = document.createElement("a");
    if (link.download !== undefined) {
        var url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", "Arquivo.csv");
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        goBack();
    }
}

// Converte o jsoncsv para um arquivo csv
function jsonToCsv(){
    var json = JSON.parse(localStorage.getItem('csv')).csv

    var fields = Object.keys(json[0])
    var replacer = function (key, value) { return value === null ? '' : value }
    var csv = json.map(function (row) {
        return fields.map(function (fieldName) {
            return JSON.stringify(row[fieldName], replacer)
        }).join(',')
    })
    csv.unshift(fields.join(','))
    csv = csv.join('\r\n');
    return csv
}

function makeTable(image, item, maxNumberOffColumns){
    let imgsContainer
   
    let a = image.slice(2,image.lastIndexOf("'"))
    let base64 = "data:image/jpg;base64,"+ a
    imgsContainer = document.createElement("div")

    imgsContainer.setAttribute("class","imgs-container")

    let img = document.createElement("img")
    img.setAttribute("src",base64)
    imgsContainer.appendChild(img)

    let tableWrapper = document.createElement("div")
    tableWrapper.setAttribute("class","table-responsive")

    let table = document.createElement("table")
    table.setAttribute("class","f1-table")

    let thead = document.createElement("thead")

    let tr = document.createElement("tr")
    for(let i = 0; i < maxNumberOffColumns; i++){
        let th = document.createElement("th")
        th.innerHTML= arrayCsv[0][i]
        tr.appendChild(th)
    }
    thead.appendChild(tr)
    table.appendChild(thead)

    let tbody = document.createElement("tbody")
    tr = document.createElement("tr")
    for(let i = 0; i < maxNumberOffColumns; i++){
        let td = document.createElement("td")
        td.innerHTML = arrayCsv[item][i]
        tr.appendChild(td)
    }
    tbody.appendChild(tr)
    table.appendChild(tbody)
    tableWrapper.appendChild(table)
    imgsContainer.appendChild(tableWrapper)
    return imgsContainer
}