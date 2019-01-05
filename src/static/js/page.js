
// add row handle
// to keep track of the input item.
// var x = {{ values |length }};

// if (typeof x !== "undefined"){
//     console.log("we have values!");
//   }
//   else{
//     console.log("no values found!");
//   };

// $(document).ready(function(){
//     var max_fields = 10; //maximum input boxes allowed
//     var wrapper = $(".element-wrapper"); //Fields wrapper
//     var add_button = $(".btn-add-row"); //Add button ID

//     // var x = 1; //initlal text box count

//     // user click on add botton
//     // $(document).on("click", ".btn-add-row", function(){
//     $(add_button).click(function(e){ //on add input button click
//         e.preventDefault();
//         if (x < max_fields) {
//             x++;
//             $(".element-wrapper").append(
//                 '<div class="form-group">' +
//                 '<input class="form-control" type="text" placeholder="Your Choice" name="choice_' + x + '"/>' +
//                 '<button class="btn-remove-row" name="remove_' + x + '"> Remove row </button></div>');
//         }
//     });

//     //user click on remove field
//     $(wrapper).on("click",".btn-remove-row", function(e){
//         e.preventDefault(); $(this).parent('div').remove(); x--;
//         var index = $(".btn-remove-row").index(this);
//         console.log("removing row with index = ", index)
//         console.log("removing row with index = ", e.name)
//         console.log("removing row with index = ", this.getAttribute('class'))
//         console.log("removing row with index = ", this.getAttribute('name'))
//     });
// });

// when re-submit decision pressed
// $(function() {
//     $('.decision-button').click(function() {
//         $.ajax({
//             url: '/',
//             data: $(".form-control").serialize(),
//             type: 'POST',
//             success: function(response) {
//                 console.log(response);
//             },
//             error: function(error) {
//                 console.log(error);
//             }
//         });
//     });
// });


// $(function() {
//     $("div[data-toggle=fieldset]").each(function() {
//         var $this = $(this);

//         //Add new entry
//         $this.find("button[data-toggle=fieldset-add-row]").click(function() {
//             var target = $($(this).data("target"))
//             console.log("printing target",target);
//             var oldrow = target.find("[data-toggle=fieldset-entry]:last");
//             console.log("print oldrow", oldrow)
//             var row = oldrow.clone(true);
//             console.log("print row", row)
//             console.log("printing input",row.find(":input")[0]);
//             var elem_id = row.find(":input")[0].id;
//             var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
//             row.attr('data-id', elem_num);
//             row.find(":input").each(function() {
//                 console.log(this);
//                 var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
//                 $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
//             });
//             oldrow.after(row);
//         }); //End add new entry

//         //Remove row
//         $this.find("button[data-toggle=fieldset-remove-row]").click(function() {
//             if($this.find("[data-toggle=fieldset-entry]").length > 1) {
//                 var thisRow = $(this).closest("[data-toggle=fieldset-entry]");
//                 thisRow.remove();
//             }
//         }); //End remove row
//     });
// });
