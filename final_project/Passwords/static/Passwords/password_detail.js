function test(e) {
  let passwords = document.getElementsByTagName("input");
  let enc_pass = passwords[0];
  let original_pass = passwords[1];
  if (enc_pass.style.display == "") {
    if (e.textContent == "visibility") {
      e.textContent += "_off";
      enc_pass.type = "text";
    } else {
      e.textContent = "visibility";
      enc_pass.type = "password";
    }
  } else {
    if (e.textContent == "visibility") {
      e.textContent += "_off";
      original_pass.type = "text";
    } else {
      e.textContent = "visibility";
      original_pass.type = "password";
    }
  }
}

function start() {
  let password = document.getElementById("my_private_data");
  let res = ts();
  print("init start");
  print(res);
  print(password.data - pass);
}

function decryption(e) {
  let passwords = document.getElementsByTagName("input");
  let enc_pass = passwords[0];
  let original_pass = passwords[1];

  if (enc_pass.style.display == "") {
    enc_pass.style.display = "none";
    original_pass.style.display = "";
    e.parentNode.innerHTML =
      "Your Password is encrypted and secured. <a href='#' id='decrypt' onclick='decryption(this)'><b>Click here</b></a> to view the Encrypted one";
  } else {
    enc_pass.style.display = "";
    original_pass.style.display = "none";
    e.parentNode.innerHTML =
      "Your Password is encrypted and secured. <a href='#' id='decrypt' onclick='decryption(this)'><b>Click here</b></a> to view the Original one";
  }
}

function qrcodeload() {
  $(".qrcodetitle").text("Generate QR Code");
  $("#cardinality").toggle(() => {
    let text =
      $(".qrcodetitle").text() == "Generate QR Code"
        ? "Hide QR Code"
        : "Generate QR Code";
    $(".qrcodetitle").text(text);
  });
}

console.log("hello world");
