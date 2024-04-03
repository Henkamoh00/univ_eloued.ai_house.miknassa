window.onload = function () {
  var loginForm = document.getElementById('loginForm');
  var joinForm = document.getElementById('joinForm');

  // عرض نموذج تسجيل الدخول وإخفاء نموذج التسجيل عند تحميل الصفحة
  loginForm.style.display = 'block';
  joinForm.style.display = 'none';
};



function toggleForm(formType) {
  var loginForm = document.getElementById('loginForm');
  var joinForm = document.getElementById('joinForm');

  if (formType === 'login') {
    loginForm.style.display = 'block';
    joinForm.style.display = 'none';
  } else if (formType === 'join') {
    loginForm.style.display = 'none';
    joinForm.style.display = 'block';
  }
}
