window.onload = async function(){
    await auth()

}
async function deleteModel(modelId){
    const baseUrl = "http://localhost:5000"
    resultado = window.confirm("Tem certeza que deseja deletar esse modelo? essa ação não poderá ser desfeita")
    console.log(resultado)
    if(modelId != 1 && resultado){
        $('#modal-comp').modal({
            show:true,
            backdrop: 'static',
            keyboard: false
        });  
        await fetch(baseUrl+"/removeModel/"+modelId,{
            method:"DELETE"
        }).then(res=>{
            if(res.status == 204){
                $('#modal-redirecting').modal({
                    show:true,
                    backdrop: 'static',
                    keyboard: false
                })
                window.location.reload
            }
            else{
                $('#modal-erro').modal({
                    show:true,
                    backdrop: 'static',
                    keyboard: false
                }) 
            }

        }).catch(err=>{
            console.error(err)
            $('#modal-erro').modal({
                show:true,
                backdrop: 'static',
                keyboard: false
            })
        }).finally(()=>{
            $('#modal-comp').modal('hide');
        })
    }
}