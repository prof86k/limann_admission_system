// $('#bar').click(function(){
    // $(this).toggleClass('open');
    // $('#page-content-wrapper,#sidebar-wrapper').toggleClass('toggled');
// });

let education_type = document.querySelector("#education_type");
// hideFields = document.querySelectorAll("#graduated_class, #graduated_gpa, #certificate_file, #transcript_file");
hideLabels = document.querySelectorAll('#hide')
postgrad = document.querySelectorAll('.postgra')
education_type.addEventListener("change",function(){
    if (education_type.value == "highSchool"){
        // hideFields.forEach(element => {
            // element.type="hidden"      
        // });
        hideLabels.forEach(element=>{
            element.classList.add('hide-fields');
            element.classList.remove('show-fields');
        })
    }else{
        if (education_type.value != 'postgraduate'){
            hideLabels.forEach(element=>{
                element.classList.add('show-fields');
                element.classList.remove('hide-fields');
                postgrad.forEach(element=>{
                    element.classList.remove('show-fields');

                    element.classList.add('hide-fields');
                });
                });
        }else{
            postgrad.forEach(element=>{
                element.classList.add('show-fields');
                element.classList.remove('postgra');
                element.classList.remove('hide-fields');

            });
        }
    }        

})