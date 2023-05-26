function checkPassword() {
  // 获取用户名和密码输入框的值
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  // 在这里你可以通过 Ajax 请求将用户名和密码发送给后端进行验证
  // 这里为了简单起见，直接在前端进行密码验证
  if (username == "" || password == "") {
    alert("用户名或密码不能为空");
    return false;
  }
  let data = {
    username: username,
    password: password
  };
  fetch('/login/verify', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(function (response) {
      if (response.ok) {
        // 处理响应结果
        return response.json().then(function (data) {
          if (data.status == 0) {
            alert("登录成功！");
            submitForm();
          } else {
            alert("用户名或密码错误！");
          }
        });
      } else {
        throw new Error('请求失败：' + response.status);
      }
    })
    .catch(function (error) {
      alert(error.message);
    });
}
function submitForm() {
  document.getElementById("loginForm").submit();
}