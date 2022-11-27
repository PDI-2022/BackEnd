var currentPage = 1
var itensPerPage 
const mainFooter = document.getElementsByTagName("footer")[0]
const body = document.getElementsByTagName("body")[0]
var csv
window.onload = function(){
    if(localStorage.getItem("csv") == '' || !localStorage.getItem("csv"))
        window.location.href="/"
    
    else
        generateTable()
}

function generateTable() {
    itensPerPage = JSON.parse(localStorage.getItem('csv')).internSeeds.length + JSON.parse(localStorage.getItem('csv')).externSeeds.length
    csv = jsonToCsv()

    console.log(csv)

    var array = csv.split("\n")

    var arrayCsv = []
    // -1 pois a ultima linha vem vazia
    for(let i = 0; i < array.length; i++){
        arrayCsv.push(array[i].split(",")) 
    }
    clearScreenElement(body)

    for(let w = itensPerPage*(currentPage-1)+1; w < (itensPerPage*currentPage)+1; w++){
        let imgsContainer = fillTable(arrayCsv,w)
        body.appendChild(imgsContainer)
    }

    //Gera o botão de download
    if(!document.getElementsByTagName("download-section")[0]){
        let download = document.createElement("download-section");
        download.setAttribute("id","download-sectio+n")
        download.setAttribute("class","downloadButtonSection")
        body.appendChild(download)
    }

    body.appendChild(mainFooter)
    arrayCsv = []
}

function clearScreenElement(){
    let body = document.getElementsByTagName("body")[0]

    const mainNav = document.getElementsByTagName("header")[0]
    body.appendChild(mainNav)
    mainFooter.remove()
}

function fillTable(arrayCsv,w){
    let index = w
    index = index < 51 ? index-1 : index-51
    // pega a imagem do localstorage
    let imgLocalStorage = w < 51 ? JSON.parse(localStorage.getItem('csv')).internSeeds : 
        JSON.parse(localStorage.getItem('csv')).externSeeds
    a = imgLocalStorage[index].blob.slice(2,imgLocalStorage[index].blob.lastIndexOf("'"))
    a = "data:image/jpg;base64,"+ a

    let imgsContainer = document.createElement("div")
    
    imgsContainer.setAttribute("class","imgs-container")

    // gera a imagem no html
    let img = document.createElement("img")
    img.setAttribute("src",a)
    imgsContainer.appendChild(img)


    // cria a tabela
    let tableWrapper = document.createElement("div")
    tableWrapper.setAttribute("class","table-responsive")

    let table = document.createElement("table")
    table.setAttribute("class","f1-table")

    let thead = document.createElement("thead")

    let tr = document.createElement("tr")
    for(let i = 0; i < 7; i++){
        let th = document.createElement("th")
        th.innerHTML= arrayCsv[0][i]
        tr.appendChild(th)
    }
    thead.appendChild(tr)
    table.appendChild(thead)


    let tbody = document.createElement("tbody")
    tr = document.createElement("tr")
    for(let i = 0; i < 7; i++){
        let td = document.createElement("td")
        td.innerHTML = arrayCsv[w][i]
        tr.appendChild(td)
    }
    tbody.appendChild(tr)
    table.appendChild(tbody)
    tableWrapper.appendChild(table)
    imgsContainer.appendChild(tableWrapper)

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