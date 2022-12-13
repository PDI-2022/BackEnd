function clickHandleProcessing(){
    let seedsClassificationButton = document.querySelector("#processing-seeds-classification")
    seedsClassificationButton.addEventListener("change",()=>{
        let processingSupLimit = document.querySelector("#menu-processing-sup-limit")
        let processingInfLimit = document.querySelector("#menu-processing-inf-limit")
        processingSupLimit.style.display = seedsClassificationButton.checked ? "block" : "none" 
        processingInfLimit.style.display = seedsClassificationButton.checked ? "block" : "none" 
    })
}

function clickHandleModel(){
    let inputClass = document.querySelector("#InputClass")
    inputClass.addEventListener("change",()=>{
        let modelHolder = document.querySelector(".modelHolder")
        modelHolder.style.display = inputClass.checked ? "flex" : "none" 
        let menuClassificationSeedsClassNumber = document.querySelector("#menu-classification-seeds-class-number")
        menuClassificationSeedsClassNumber.style.display = InputClass.checked ? "block" : "none"
    })
}