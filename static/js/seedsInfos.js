google.charts.load('current', {'packages':['corechart'],'language': 'pt'});


var csv
var arrayCsv = []
var bulletMap = [
    '- ID',
    '- Lado',
    '- % de Branco',
    '- % de Branco Leitoso',
    '- % de Vermelho Carmim Claro',
    '- % de Vermelho Carmim Escuro',
    '- Qtd. de Buracos',
    '- Área dos Buracos/Área da Semente'
]

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
    $('#modal-comp').modal({
        show:true,
        backdrop: 'static',
        keyboard: false
    });  
    let token = document.cookie
    token = token.split(`token=`)[1]

    const url = new String("http://127.0.0.1:5000/api/v1/process/pagination");
    const Img = await fetch(url, {
        method:"POST", 
        headers: {"Content-Type": "application/json","token":`${token}`},
        body: JSON.stringify(json)
    }).catch(err=>{
        console.error(err)
    })
    if(Img.status != 200){
        $('#modal-comp').modal('hide');
        window.alert("Ops, alguma coisa deu errado!")
    }
    const response = await Img.json()
    response["externSeeds"]
    $('#modal-comp').modal('hide');

    generateTable(response["externSeeds"],response["internSeeds"])
}

window.onload = async function () {
    await auth()
    if(localStorage.getItem("csv") == '' || !localStorage.getItem("csv"))
        window.location.href="/"
    
    else{
        if(localStorage.getItem("classificationYolo") == "true"){
            $('#modal-comp').modal({
                show:true,
                backdrop: 'static',
                keyboard: false
            });  
            let token = document.cookie
            token = token.split(`token=`)[1]
            let respEmbriao = await fetch("http://localhost:5000/api/v1/process/embriao", {
                method:"GET",
                headers:{
                    "token":`${token}`
                } 
            }).catch(err=>{
                console.error(err)
            })
            let csvembriao = await respEmbriao.text()
            localStorage.setItem("embriaoCsv",csvembriao)
            $('#modal-comp').modal('hide');
    
        }
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
    let hasVigorTable = document.querySelector("#vigorTable")
    clearScreenElement(body,mainFooter,hasVigorTable)
  
    if(localStorage.getItem("hasClass") == "true"){
        let vigorTable = makeVigorTable()
        body.appendChild(vigorTable)
    }
    let imgsContainer = fillTable(externSeeds,internSeeds,arrayCsv)

    let container = document.createElement("div")
    container.setAttribute("class","container")

    let pageTitle = document.createElement("h2")
    pageTitle.innerHTML = "Análise Individual por Semente"

    container.appendChild(pageTitle)

    body.appendChild(container)

    for(let i = 0; i < imgsContainer.length; i++){
        container.appendChild(imgsContainer[i])
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
    let hasClass = (localStorage.getItem("hasClass") == "true")
    let maxItem = hasClass ? arrayCsv.length - 5 : arrayCsv.length - 2
    state.totalPages = Math.ceil(maxItem / (2*state.perPage))

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


function clearScreenElement(body,mainFooter, hasVigorTable){
    const mainNav = document.getElementsByTagName("header")[0]
    if(!!hasVigorTable){
        body.removeChild(hasVigorTable)
    }
    let imgContainer = document.querySelectorAll(".seed-card")
    let container = document.querySelector(".container")


    if(imgContainer.length > 0){
        imgContainer.forEach(img=>{
            container.removeChild(img)
        })
        body.removeChild(container)
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
    if(hasClass){
        bulletMap.push("Classe")
    }
    let maxNumberOfColumns = hasClass == "true" ? 9 : 8
    

    let imgsContainer = []

    for(let i=1;i<=internSeeds.length;i++){
        imgsContainer.push(
            makeSeedCard(internSeeds[i-1], (initialValue+(2*i)-2), externSeeds[i-1], (initialValue+(2*i)-1), maxNumberOfColumns, hasClass == "true" ? true : false)
        )
    }

    return imgsContainer
}

function makeSeedCard(internSeedImage, internSeedDataIndex, externSeedImage, externSeedDataIndex, maxNumberOfColumns, hasClassification){
    let card = document.createElement("div")
    card.setAttribute("class","card mt-4 seed-card")

    let cardTitle = document.createElement("h4")

    cardTitle.setAttribute("class", "card-title m-3")
    cardTitle.innerHTML = "Semente " + arrayCsv[internSeedDataIndex][0]

    card.appendChild(cardTitle)

    if (hasClassification){
        let cardSubtitle = document.createElement("h6")
        cardSubtitle.setAttribute("class", "card-subtitle m-3")
        cardSubtitle.innerHTML = "Classe "+ arrayCsv[internSeedDataIndex][maxNumberOfColumns-1]

        card.appendChild(cardSubtitle)
    }

    let cardBody = document.createElement("div")
    cardBody.setAttribute("class","card-body")

    card.appendChild(cardBody)

    let outterRow = document.createElement("div")
    outterRow.setAttribute("class","row")

    cardBody.appendChild(outterRow)

    let leftColumn = document.createElement("div")
    leftColumn.setAttribute("class", "col-md-6")


    let rightColumn = document.createElement("div")
    rightColumn.setAttribute("class", "col-md-6")

    outterRow.appendChild(leftColumn)
    outterRow.appendChild(rightColumn)

    //left
    let leftTitle = document.createElement("h5")
    leftTitle.innerHTML = "Parte Externa"

    let leftInnerRow = document.createElement("div")
    leftInnerRow.setAttribute("class","row")

    leftColumn.appendChild(leftTitle)
    leftColumn.appendChild(leftInnerRow)

    let leftImgCol = document.createElement("div")
    leftImgCol.setAttribute("class","col-md-6")

    leftInnerRow.appendChild(leftImgCol)

    let leftImgData = externSeedImage.slice(2,externSeedImage.lastIndexOf("'"))
    let leftBase64 = "data:image/jpg;base64,"+ leftImgData
    let leftImg = document.createElement("img")

    leftImg.setAttribute("src",leftBase64)
    leftImg.setAttribute("style","width:100%")

    leftImgCol.appendChild(leftImg)

    let leftDataCol = document.createElement("div")
    leftDataCol.setAttribute("class","col-md-6")

    leftInnerRow.appendChild(leftDataCol)

    let leftList = document.createElement("ul")
    leftList.setAttribute("class", "list-group list-group-flush seed-details")

    for(let i = 2; i < maxNumberOfColumns; i++){
        let li = document.createElement("li")
        li.setAttribute("class","list-group-item")
        li.setAttribute("style","padding:4px")
        li.innerHTML = "<b>"+bulletMap[i]+": </b>" + arrayCsv[externSeedDataIndex][i]

        leftList.appendChild(li)

    }

    leftDataCol.appendChild(leftList)
    
    
    //right
    let rightTitle = document.createElement("h5")
    rightTitle.innerHTML = "Parte Interna"

    let rightInnerRow = document.createElement("div")
    rightInnerRow.setAttribute("class","row")

    rightColumn.appendChild(rightTitle)
    rightColumn.appendChild(rightInnerRow)

    let rightImgCol = document.createElement("div")
    rightImgCol.setAttribute("class","col-md-6")

    rightInnerRow.appendChild(rightImgCol)

    let rightImgData = internSeedImage.slice(2,internSeedImage.lastIndexOf("'"))
    let rightBase64 = "data:image/jpg;base64,"+ rightImgData
    let rightImg = document.createElement("img")

    rightImg.setAttribute("src",rightBase64)
    rightImg.setAttribute("style","width:100%")

    rightImgCol.appendChild(rightImg)

    let rightDataCol = document.createElement("div")
    rightDataCol.setAttribute("class","col-md-6")

    rightInnerRow.appendChild(rightDataCol)

    let rightList = document.createElement("ul")
    rightList.setAttribute("class", "list-group list-group-flush seed-details")

    for(let i = 2; i < maxNumberOfColumns; i++){
        let li = document.createElement("li")
        li.setAttribute("class","list-group-item")
        li.setAttribute("style","padding:4px")
        li.innerHTML = "<b>"+bulletMap[i]+": </b>" + arrayCsv[internSeedDataIndex][i]

        rightList.appendChild(li)

    }

    rightDataCol.appendChild(rightList)


    return card

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
        link.setAttribute("download", "Sementes.csv");
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    if(!!localStorage.getItem("embriaoCsv")){
        const csvString = localStorage.getItem("embriaoCsv");
        var blob = new Blob([csvString], { type: 'text/plain;charset=utf-8;' });
        var link = document.createElement("a");
        if (link.download !== undefined) {
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "Embriao.csv");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }  
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

function makeVigorTable(){

    let tableWrapper = document.createElement("div")
    tableWrapper.setAttribute("class","container")

    let h3 = document.createElement("h2")
    h3.innerHTML = "Resumo das Classes"
    tableWrapper.appendChild(h3)


    //

    let table = document.createElement("table");
    table.setAttribute("class","table table-striped");

    let thead = document.createElement("thead");
    let tr = document.createElement("tr");
    for(let i = 0; i < 9; i++){
        let th = document.createElement("th")
        th.setAttribute("scope","col")


        th.innerHTML= arrayCsv[arrayCsv.length-3][i]
        tr.appendChild(th)
    }

    thead.appendChild(tr);
    table.appendChild(thead);

    let tbody = document.createElement("tbody");
    let tbodytr = document.createElement("tr");
    for(let i = 0; i < 9; i++){
        let td = document.createElement("td")
        td.innerHTML = arrayCsv[arrayCsv.length-2][i]
        tbodytr.appendChild(td)
    }

    tbody.appendChild(tbodytr);
    table.appendChild(tbody);

    //
    
    // let table = document.createElement("table")
    // table.setAttribute("class","f1-table")

    // let thead = document.createElement("thead")

    // let tr = document.createElement("tr")
    // for(let i = 0; i < 9; i++){
    //     let th = document.createElement("th")
    //     th.innerHTML= arrayCsv[arrayCsv.length-3][i]
    //     tr.appendChild(th)
    // }
    // thead.appendChild(tr)
    // table.appendChild(thead)

    // let tbody = document.createElement("tbody")
    // tr = document.createElement("tr")

    // for(let i = 0; i < 9; i++){
    //     let td = document.createElement("td")
    //     td.innerHTML = arrayCsv[arrayCsv.length-2][i]
    //     tr.appendChild(td)
    // }
    // tbody.appendChild(tr)
    // table.appendChild(tbody)
    
    // tableWrapper.setAttribute("id","vigorTable")
    //

    let chartDiv = document.createElement("div")
    chartDiv.setAttribute("id","chart_div")

    
    tableWrapper.appendChild(table)
    tableWrapper.appendChild(chartDiv)
    
    //

    google.charts.setOnLoadCallback(drawChart);
    
    return tableWrapper
}

function drawChart(){
    let dataList = []

    dataList.push(['Classe','Porcentagem']);

    for(let i = 2; i < 9; i++){
        let rawPercentage = arrayCsv[arrayCsv.length-2][i];
        let percentage = rawPercentage.replace("%","");
        let percentageConverted = parseFloat(percentage);

        dataList.push(['Classe ' + (i-1), percentageConverted]);
    }

    console.log(dataList)

    let options = {
        title: 'Histograma da Distribuição das Sementes entre as Classes',
        backgroundColor:'#FAFAFA'
    };

    var data = google.visualization.arrayToDataTable(dataList)

    var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}