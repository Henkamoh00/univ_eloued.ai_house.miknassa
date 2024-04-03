// document.getElementById('loginForm').addEventListener('submit', function(event) {
//     // منع ارسال نموذج تسجيل الحساب
//     event.preventDefault();
//     alert('Hello!');
//     // إضافة المزيد من الشفرة لمعالجة تسجيل الدخول
//     // يمكنك إضافة الشفرة الخاصة بك هنا
// });

// $(document).ready(function () {
//     $("#trigger").change(function () {
//         var value = $(this).val();
//         $.ajax({
//             url: "/miknassa",
//             type: "POST",
//             contentType: "application/json",
//             data: JSON.stringify({ value: value }),
//             success: function (response) {
//                 $("#result").text(response.updated_content);
//             },
//         });
//     });
// });

// $(function(){
//     if ($("#wilayaId").load()){
//         alert("ddsds")
//     }
// });



// $("#wilayaId").change(function () {
//     var wilaya = document.getElementById("wilayaId");
//     var dayra = document.getElementById("dayraId");
//     var municipality = document.getElementById("municipalityId");
//     var id = wilaya.options[wilaya.selectedIndex].value;
//     // alert(id);
//     console.log(location)

//     var xhr = new XMLHttpRequest();
//     xhr.open('POST', '127.0.0.1:5000/miknassa', true);
//     xhr.onreadystatechange = function() {
//         if (this.readyState === 4 && this.status === 200) {
//             // تحميل المحتوى في عنصر معين
//             document.getElementById('iii').innerHTML = this.responseText;
//         }
//     };
//     xhr.send();

// });



