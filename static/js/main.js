document.addEventListener("DOMContentLoaded",function(){
    const deleteLinks = document.querySelectorAll('.delete-link');

    deleteLinks.forEach(function(link){
        link.addEventListener('click',function(e){
            if(!confirm('Are you want to delete this item?')){
                e.preventDefault();
            }
        });
    });
});