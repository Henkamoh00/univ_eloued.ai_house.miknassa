window.onload = function () {
    var operation = document.getElementById('operation');
    var roleChanging = document.getElementById('roleChanging');
    var truckAdding = document.getElementById('truckAdding');

    // عرض نموذج تسجيل الدخول وإخفاء نموذج التسجيل عند تحميل الصفحة
    operation.style.display = 'block';
    roleChanging.style.display = 'none';
    truckAdding.style.display = 'none';
};



function toggleForm(formType) {
    var operation = document.getElementById('operation');
    var roleChanging = document.getElementById('roleChanging');
    var truckAdding = document.getElementById('truckAdding');

    if (formType === 'operation') {
        operation.style.display = 'block';
        roleChanging.style.display = 'none';
        truckAdding.style.display = 'none';
    } else if (formType === 'roleChanging') {
        operation.style.display = 'none';
        roleChanging.style.display = 'block';
        truckAdding.style.display = 'none';
    } else if (formType === 'truckAdding') {
        operation.style.display = 'none';
        roleChanging.style.display = 'none';
        truckAdding.style.display = 'block';
    }
}
